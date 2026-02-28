import json
import re
import time
from pathlib import Path
from typing import Any

from pipelines.shared import (
    FAST_GEMINI_AGENT,
    chunked,
    compact_text,
    extract_json_blob,
    normalize_newlines,
    normalize_space,
    run_gemini_cli,
    trim_lines as shared_trim_lines,
)

ROOT = Path(__file__).resolve().parents[2]
CARDS_FILE = ROOT / "topic_cards.json"
MODEL = FAST_GEMINI_AGENT
CHUNK_SIZE = 3
RETRY_LIMIT = 2
MAX_KEY_POINT_CHARS = 220
FILTER_AUDIT_FILE = ROOT / "data" / "quality" / "key_point_filter_audit.json"

BANNED_KEY_POINT_START_RE = re.compile(
    r"^(understand|remember|know|be aware|make sure|it is important|always)\b",
    re.IGNORECASE,
)

LOW_VALUE_KEY_POINT_RE = re.compile(
    r"^(watch for this exam pattern|pay attention to this|this is important|exam pattern)\b",
    re.IGNORECASE,
)

CONCRETE_KEYWORD_RE = re.compile(
    r"\b("
    r"list|dict|set|tuple|str|string|int|float|bool|none|true|false|"
    r"mutable|immutable|slice|slicing|index|loop|range|for|while|if|elif|else|"
    r"break|continue|pass|return|lambda|append|extend|insert|pop|sort|sorted|"
    r"reverse|len|type|print|enumerate|zip|in|not"
    r")\b",
    re.IGNORECASE,
)


def compact(text: str, limit: int = 260) -> str:
    return compact_text(text, limit)


def trim_lines(text: str, max_lines: int = 6) -> str:
    return shared_trim_lines(text, max_lines)


def normalize_key_point_text(text: Any) -> str:
    value = normalize_space(str(text or ""))
    value = re.sub(r"^[\-\*\u2022\d\.\)\(]+\s*", "", value)
    return compact(value, MAX_KEY_POINT_CHARS).strip()


def has_concrete_signal(text: str) -> bool:
    if not text:
        return False
    if "`" in text:
        return True
    if re.search(r"\b\d+\b", text):
        return True
    if re.search(r"(->|=>|==|!=|<=|>=|\[|\]|\(|\)|\{|\}|:|\|)", text):
        return True
    return bool(CONCRETE_KEYWORD_RE.search(text))


def key_point_rejection_reason(text: str) -> str | None:
    value = normalize_space(text)
    if not value:
        return "empty"
    if len(value.split()) < 5:
        return "too_short"
    if "?" in value:
        return "question_style"
    if BANNED_KEY_POINT_START_RE.match(value):
        return "banned_starter"
    if LOW_VALUE_KEY_POINT_RE.match(value):
        return "generic_prefix"
    if not has_concrete_signal(value):
        return "no_concrete_signal"
    return None


def is_low_value_key_point(text: str) -> bool:
    return key_point_rejection_reason(text) is not None


def init_filter_audit() -> dict[str, Any]:
    return {
        "model": MODEL,
        "rules": {
            "max_chars": MAX_KEY_POINT_CHARS,
            "min_words": 5,
            "banned_starter_regex": BANNED_KEY_POINT_START_RE.pattern,
            "low_value_prefix_regex": LOW_VALUE_KEY_POINT_RE.pattern,
        },
        "summary": {
            "total_candidates": 0,
            "kept": 0,
            "rejected": 0,
            "cards_with_rejections": 0,
            "cards_using_fallback_points": 0,
        },
        "rejections_by_reason": {},
        "sample_rejections": [],
    }


def record_filter_decisions(
    audit: dict[str, Any],
    *,
    card_id: str,
    topic: str,
    source: str,
    kept: list[str],
    rejected: list[dict[str, str]],
) -> None:
    summary = audit["summary"]
    summary["total_candidates"] += len(kept) + len(rejected)
    summary["kept"] += len(kept)
    summary["rejected"] += len(rejected)

    for item in rejected:
        reason = item["reason"]
        audit["rejections_by_reason"][reason] = audit["rejections_by_reason"].get(reason, 0) + 1
        if len(audit["sample_rejections"]) < 200:
            audit["sample_rejections"].append(
                {
                    "card_id": card_id,
                    "topic": topic,
                    "source": source,
                    "reason": reason,
                    "text": item["text"],
                }
            )


def snippet_candidates(card: dict[str, Any]) -> list[dict[str, str]]:
    sections = card.get("sections", {})
    out: list[dict[str, str]] = []

    for snippet in sections.get("exam_questions", [])[:10]:
        out.append(
            {
                "id": snippet.get("id", ""),
                "source": "exam",
                "title": f"Q{snippet.get('number','?')} {snippet.get('exam_label','')}",
                "summary": compact(snippet.get("question", ""), 320),
                "correct": str(snippet.get("correct", "")),
            }
        )

    for snippet in sections.get("lecture_snippets", [])[:8]:
        code_lines = []
        for ex in (snippet.get("code_examples") or [])[:2]:
            code_lines.append(trim_lines(ex.get("code", ""), 5))
        out.append(
            {
                "id": snippet.get("id", ""),
                "source": "lecture",
                "title": f"{snippet.get('topic','Lecture')} W{snippet.get('week','?')}",
                "summary": compact(snippet.get("explanation", ""), 260),
                "code": compact("\n\n".join([x for x in code_lines if x]), 380),
            }
        )

    for snippet in sections.get("notebook_snippets", [])[:8]:
        out.append(
            {
                "id": snippet.get("id", ""),
                "source": "notebook",
                "title": f"{snippet.get('topic','Notebook')} W{snippet.get('week','?')} cell {snippet.get('cell_index','?')}",
                "summary": compact(trim_lines(snippet.get("source", ""), 6), 340),
            }
        )

    return [x for x in out if x.get("id")]


def run_gemini(prompt: str) -> str:
    return run_gemini_cli(
        prompt,
        model=MODEL,
        timeout_seconds=180,
        stderr_clip=400,
    )


def fallback_result(card: dict[str, Any]) -> dict[str, Any]:
    traps = card.get("trap_patterns", [])
    topic_lower = normalize_space(str(card.get("topic", ""))).lower()
    fallback_points = []

    for trap in traps[:3]:
        trap_text = normalize_space(str(trap.get("trap", "")))
        pattern_text = normalize_space(str(trap.get("pattern", "")))
        if trap_text and pattern_text:
            fallback_points.append(compact(f"{pattern_text}: {trap_text}", MAX_KEY_POINT_CHARS))
        elif trap_text:
            fallback_points.append(compact(f"Exam trap: {trap_text}", MAX_KEY_POINT_CHARS))

    if not fallback_points:
        if topic_lower == "scope":
            fallback_points = [
                "Assignment inside a function (e.g., `x = 10`) makes `x` local unless `global x` or `nonlocal x` is declared.",
                "Reading a global name is allowed inside a function; rebinding that name requires `global name`.",
                "`UnboundLocalError` occurs when Python marks a name local due to assignment, then that name is read before assignment.",
                "Parameters are local names: changing `param` inside the function does not rebind the caller's variable name.",
                "LEGB lookup order: Local -> Enclosing -> Global -> Builtins; closest scope wins for name resolution.",
            ]
        elif topic_lower == "exam question types":
            fallback_points = [
                "Output-tracing workflow: annotate each executed line as `(line -> variable updates -> printed text)`.",
                "For loop questions, count iterations first: `range(n)` executes `n` times with values `0..n-1`.",
                "For nested loops, total inner executions are cumulative/multiplicative; compute counts before evaluating output.",
                "Type-check trap: `'3' + 2` raises `TypeError`, while `'3' * 2` repeats to `'33'`.",
                "Method trap: in-place methods (e.g., `list.sort()`) return `None`; value-returning alternatives (e.g., `sorted(lst)`) return new objects.",
            ]
        elif topic_lower == "python execution model":
            fallback_points = [
                "Execution order is sequential: `line_n` must finish before Python runs `line_n+1`.",
                "An uncaught exception (`NameError`, `TypeError`, etc.) stops execution immediately; later lines do not run.",
                "`def name(...):` creates a function object now; the function body executes only when `name(...)` is called.",
                "Name resolution follows LEGB order: Local -> Enclosing -> Global -> Builtins.",
                "`if`/`while` evaluate the condition before running the body; a falsy condition skips the body.",
            ]
        else:
            fallback_points = [
                "Mutation check: `list.sort()` / `append()` mutate and return `None`; `sorted(lst)` or slicing create a new object.",
                "Mini reference: `break` -> exit loop; `continue` -> skip current iteration; `pass` -> no-op placeholder.",
                "Slicing rule: `[start:stop:step]` includes `start`, excludes `stop`; negative `step` iterates right-to-left.",
                "Boolean precedence: `not` runs before `and`, and `and` runs before `or` unless parentheses override.",
                "Trace loops with a tiny table `(iteration, key vars, output)` to catch off-by-one and stale-variable mistakes.",
            ]

    candidates = snippet_candidates(card)
    exam_ids = [c["id"] for c in candidates if c.get("source") == "exam"]
    lecture_ids = [c["id"] for c in candidates if c.get("source") == "lecture"]
    notebook_ids = [c["id"] for c in candidates if c.get("source") == "notebook"]
    recommended = (exam_ids[:4] + lecture_ids[:2] + notebook_ids[:1])[:8]

    return {
        "key_points_to_remember": fallback_points[:6],
        "recommended_ids": recommended,
    }


def sanitize_key_points(points: list[Any]) -> list[str]:
    cleaned, _ = sanitize_key_points_with_audit(points)
    return cleaned


def sanitize_key_points_with_audit(points: list[Any]) -> tuple[list[str], list[dict[str, str]]]:
    cleaned = []
    rejected: list[dict[str, str]] = []
    for point in points:
        text = normalize_key_point_text(point)
        reason = key_point_rejection_reason(text)
        if reason:
            rejected.append({"text": text, "reason": reason})
            continue
        cleaned.append(text)
    uniq = []
    seen = set()
    for item in cleaned:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        uniq.append(item)
    return uniq[:8], rejected


def normalize_key_points_no_filter(points: list[Any]) -> list[str]:
    out: list[str] = []
    seen = set()
    for point in points:
        text = normalize_key_point_text(point)
        if not text:
            continue
        key = text.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(text)
    return out[:8]


def sanitize_recommended_ids(ids: list[Any], valid_ids: set[str]) -> list[str]:
    out = []
    for raw in ids:
        val = str(raw).strip()
        if not val or val not in valid_ids:
            continue
        if val not in out:
            out.append(val)
    return out


def context_for_card(card: dict[str, Any]) -> dict[str, Any]:
    sections = card.get("sections", {})
    return {
        "id": card.get("id"),
        "topic": card.get("topic"),
        "weeks": card.get("weeks", []),
        "exam_hits": card.get("exam_stats", {}).get("total_hits", 0),
        "exam_breakdown": card.get("exam_stats", {}).get("by_exam", {}),
        "ai_common_questions": sections.get("ai_common_questions", {}).get("bullets", [])[:6],
        "trap_patterns": [
            {
                "pattern": compact(tp.get("pattern", ""), 80),
                "trap": compact(tp.get("trap", ""), 160),
            }
            for tp in card.get("trap_patterns", [])[:4]
        ],
        "source_candidates": snippet_candidates(card),
    }


def generate_chunk(chunk: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompt = f"""
You are helping produce exam-focused cheat sheet selections for an Intro Python midterm.
For EACH item in input, return one object with schema:
{{
  "id": "same id",
  "key_points_to_remember": ["3-7 concise reference lines for fast exam lookup"],
  "recommended_ids": ["IDs from source_candidates that should be included in Recommended for cheat sheet"]
}}

Selection rules:
- Prefer snippets that generalize to many exam questions.
- Prefer exam snippets that show common traps/output reasoning.
- Keep recommended_ids between 3 and 8 when possible.
- key_points must be concrete reference content, not reminders.
- Every key point must include an actionable rule/contrast/check with Python detail.
- Do NOT start a key point with words like "Remember", "Understand", or "Know".
- Keep each key point short (single sentence or compact "mini reference" line).
- Good style examples:
  - "`list.sort()` mutates in place and returns `None`; `sorted(lst)` returns a new list."
  - "Mutable vs immutable: `list/dict/set` can mutate; `str/tuple/int` operations create new objects."
  - "Mini reference: `break` -> exit loop; `continue` -> next iteration; `pass` -> no-op."
- Bad style examples:
  - "Understand how loops work."
  - "Remember to be careful with variables."
- Return ONLY JSON array in the same order as input.

Input:
{json.dumps(chunk, ensure_ascii=False, indent=2)}
""".strip()

    last_error = None
    for attempt in range(RETRY_LIMIT + 1):
        try:
            raw = run_gemini(prompt)
            blob = extract_json_blob(raw)
            data = json.loads(blob)
            if not isinstance(data, list):
                raise ValueError("Model output is not a JSON array")
            return data
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.2 + attempt)

    raise RuntimeError(f"Chunk generation failed: {last_error}")
