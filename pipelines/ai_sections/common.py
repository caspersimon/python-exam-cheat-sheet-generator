import json
import time
from pathlib import Path
from typing import Any

from pipelines.shared import chunked, compact_text, extract_json_blob, run_gemini_cli, trim_lines

ROOT = Path(__file__).resolve().parents[2]
CARDS_FILE = ROOT / "topic_cards.json"
MODEL = "gemini-2.5-pro"
CHUNK_SIZE = 6
RETRY_LIMIT = 2

def sanitize_topic_context(card: dict[str, Any]) -> dict[str, Any]:
    sections = card.get("sections", {})

    lecture_context = []
    for snippet in sections.get("lecture_snippets", [])[:2]:
        row = {
            "topic": snippet.get("topic", ""),
            "explanation": compact_text(snippet.get("explanation", ""), 280),
            "code_examples": [
                {
                    "description": ex.get("description", ""),
                    "code": trim_lines(ex.get("code", ""), 8),
                }
                for ex in (snippet.get("code_examples") or [])[:2]
                if ex.get("code")
            ],
        }
        if row["topic"] or row["explanation"] or row["code_examples"]:
            lecture_context.append(row)

    exam_context = []
    for q in sections.get("exam_questions", [])[:3]:
        exam_context.append(
            {
                "label": q.get("exam_label", ""),
                "number": q.get("number", ""),
                "question": compact_text(q.get("question", ""), 280),
                "correct": q.get("correct", ""),
                "explanation": compact_text(q.get("explanation", ""), 220),
            }
        )

    notebook_context = []
    for snippet in sections.get("notebook_snippets", [])[:2]:
        notebook_context.append(
            {
                "topic": snippet.get("topic", ""),
                "source": trim_lines(snippet.get("source", ""), 8),
                "outputs": [compact_text(out, 160) for out in (snippet.get("outputs") or [])[:2]],
            }
        )

    traps = []
    for trap in card.get("trap_patterns", [])[:3]:
        traps.append(
            {
                "pattern": trap.get("pattern", ""),
                "trap": compact_text(trap.get("trap", ""), 220),
            }
        )

    return {
        "id": card.get("id"),
        "topic": card.get("topic"),
        "canonical_topic": card.get("canonical_topic"),
        "weeks": card.get("weeks", []),
        "exam_hits": card.get("exam_stats", {}).get("total_hits", 0),
        "exam_sources": card.get("exam_stats", {}).get("by_exam", {}),
        "related_topics": (card.get("related_topics") or [])[:10],
        "lecture_context": lecture_context,
        "exam_context": exam_context,
        "notebook_context": notebook_context,
        "trap_patterns": traps,
    }

def safe_list(value: Any) -> list:
    if isinstance(value, list):
        return value
    return []


def fallback_ai_bundle(card: dict[str, Any]) -> dict[str, Any]:
    topic = card.get("topic", "this topic")
    traps = card.get("trap_patterns", [])
    trap_text = traps[0].get("trap") if traps else "Pay attention to object mutability, scope, and slicing boundaries."

    summary = (
        f"This topic focuses on how Python evaluates and executes '{topic}' behavior in code. "
        f"For midterm-style questions, trace values step by step and verify what is printed, returned, or mutated."
    )

    questions = [
        f"Can you predict the exact output for a short '{topic}' code fragment?",
        "Which lines mutate existing objects versus create new objects?",
        "What trap appears when operator precedence or argument passing is misread?",
        f"What is the most likely wrong answer choice and why? Hint: {compact_text(trap_text, 100)}",
    ]

    examples = [
        {
            "kind": "correct",
            "title": f"Correct: basic {topic} usage",
            "code": "def demo(x):\n    return x\n\nprint(demo(3))",
            "why": "Defines a function and returns the expected value clearly.",
        },
        {
            "kind": "correct",
            "title": f"Correct: explicit check for {topic}",
            "code": "value = [1, 2, 3]\nif len(value) > 0:\n    print(value[0])",
            "why": "Uses explicit control flow and avoids hidden assumptions.",
        },
        {
            "kind": "incorrect",
            "title": f"Incorrect: ambiguous {topic} assumption",
            "code": "value = [1, 2, 3]\nprint(value[3])",
            "why": "Raises IndexError because index 3 is out of range.",
        },
        {
            "kind": "incorrect",
            "title": f"Incorrect: forgotten return in {topic}",
            "code": "def demo(x):\n    x + 1\n\nprint(demo(3))",
            "why": "Prints None because the function does not return a value.",
        },
    ]

    return {
        "summary": summary,
        "common_questions": questions,
        "examples": examples,
    }


def normalize_examples(raw_examples: list[Any], topic: str) -> list[dict[str, str]]:
    examples = []
    for item in raw_examples:
        if not isinstance(item, dict):
            continue
        kind = (item.get("kind") or "").strip().lower()
        if kind not in {"correct", "incorrect"}:
            kind = "correct" if len(examples) < 2 else "incorrect"
        title = compact_text(str(item.get("title") or f"{kind.title()} example for {topic}"), 90)
        code = trim_lines(str(item.get("code") or ""), 10).strip()
        why = compact_text(str(item.get("why") or "No explanation provided."), 220)
        if not code:
            continue
        examples.append({"kind": kind, "title": title, "code": code, "why": why})

    if len(examples) < 4:
        needed = 4 - len(examples)
        fallback = fallback_ai_bundle({"topic": topic})["examples"]
        for item in fallback[:needed]:
            examples.append(item)

    examples = examples[:4]

    # Force at least two correct and two incorrect labels.
    for idx, item in enumerate(examples):
        item["kind"] = "correct" if idx < 2 else "incorrect"

    return examples


def normalize_generated_entry(raw: dict[str, Any], card: dict[str, Any]) -> dict[str, Any]:
    fallback = fallback_ai_bundle(card)

    summary = compact_text(str(raw.get("ai_summary") or raw.get("summary") or fallback["summary"]), 420)

    common = safe_list(raw.get("ai_common_questions") or raw.get("common_questions"))
    common = [compact_text(str(x), 180) for x in common if str(x).strip()]
    if len(common) < 4:
        for item in fallback["common_questions"]:
            if len(common) >= 4:
                break
            common.append(item)
    common = common[:6]

    examples = normalize_examples(safe_list(raw.get("ai_examples") or raw.get("examples")), card.get("topic", "topic"))

    return {
        "summary": summary,
        "common_questions": common,
        "examples": examples,
    }

def generate_for_chunk(contexts: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompt = f"""
You are creating concise AI study aids for an Introduction to Python midterm cheat-sheet app.
For EACH topic context below, return one JSON object with this exact schema:
{{
  "id": "<same id>",
  "ai_summary": "2-4 concise sentences about what the code/topic does and what to track in output questions.",
  "ai_common_questions": ["4-6 brief bullets with common exam asks/traps"],
  "ai_examples": [
    {{"kind":"correct","title":"...","code":"...","why":"..."}},
    {{"kind":"correct","title":"...","code":"...","why":"..."}},
    {{"kind":"incorrect","title":"...","code":"...","why":"..."}},
    {{"kind":"incorrect","title":"...","code":"...","why":"..."}}
  ]
}}

Rules:
- Return ONLY a JSON array, in the same order as input.
- Keep each code example <= 8 lines and based on Python built-ins taught in intro courses.
- Incorrect examples must be realistic midterm mistakes.
- Be specific and practical; no generic fluff.

Input topic contexts:
{json.dumps(contexts, ensure_ascii=False, indent=2)}
""".strip()

    last_error = None
    for attempt in range(RETRY_LIMIT + 1):
        try:
            output = run_gemini_cli(
                prompt,
                model=MODEL,
                timeout_seconds=240,
                stderr_clip=500,
            )
            blob = extract_json_blob(output)
            data = json.loads(blob)
            if not isinstance(data, list):
                raise ValueError("Model output is not a JSON array")
            return data
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            time.sleep(1.2 + attempt)

    raise RuntimeError(f"Failed to generate chunk after retries: {last_error}")


def apply_generated(data: dict[str, Any], generated_by_id: dict[str, dict[str, Any]]) -> None:
    cards = data.get("cards", [])
    for card in cards:
        card_id = card.get("id")
        generated = generated_by_id.get(card_id)
        if not generated:
            generated = fallback_ai_bundle(card)

        sections = card.setdefault("sections", {})
        sections["ai_summary"] = {
            "status": "generated",
            "content": generated["summary"],
            "generator": "gemini-cli",
            "model": MODEL,
        }
        sections["ai_common_questions"] = {
            "status": "generated",
            "bullets": generated["common_questions"],
            "generator": "gemini-cli",
            "model": MODEL,
        }

        examples = []
        for idx, item in enumerate(generated["examples"], start=1):
            examples.append(
                {
                    "id": f"ai-example-{idx}",
                    "kind": item["kind"],
                    "title": item["title"],
                    "code": item["code"],
                    "why": item["why"],
                    "status": "generated",
                }
            )
        sections["ai_examples"] = examples

        # Remove superseded placeholders from old app versions if present.
        sections.pop("ai_explanation", None)
        sections.pop("ai_code_snippets", None)


def validate_ai_fields(data: dict[str, Any]) -> None:
    cards = data.get("cards", [])
    missing = []
    for card in cards:
        sections = card.get("sections", {})
        summary = sections.get("ai_summary", {}).get("content", "").strip()
        bullets = sections.get("ai_common_questions", {}).get("bullets", [])
        examples = sections.get("ai_examples", [])

        ok = bool(summary) and isinstance(bullets, list) and len(bullets) >= 4 and isinstance(examples, list) and len(examples) >= 4
        if not ok:
            missing.append(card.get("id", "unknown"))

    if missing:
        raise RuntimeError(f"AI validation failed for {len(missing)} cards: {missing[:10]}")

