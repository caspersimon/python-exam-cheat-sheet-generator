#!/usr/bin/env python3
import json
import re
import subprocess
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CARDS_FILE = ROOT / "topic_cards.json"
MODEL = "gemini-2.5-flash"
CHUNK_SIZE = 8
RETRY_LIMIT = 2


def compact(text: str, limit: int = 260) -> str:
    value = (text or "").strip()
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def trim_lines(text: str, max_lines: int = 6) -> str:
    lines = (text or "").splitlines()
    if len(lines) <= max_lines:
        return "\n".join(lines)
    return "\n".join(lines[:max_lines]) + "\n# ..."


def normalize_newlines(text: str) -> str:
    return str(text or "").replace("\r\n", "\n").replace("\r", "\n")


def snippet_candidates(card: dict[str, Any]) -> list[dict[str, str]]:
    sections = card.get("sections", {})
    out: list[dict[str, str]] = []

    for snippet in sections.get("exam_questions", [])[:14]:
        out.append(
            {
                "id": snippet.get("id", ""),
                "source": "exam",
                "title": f"Q{snippet.get('number','?')} {snippet.get('exam_label','')}",
                "summary": compact(snippet.get("question", ""), 320),
                "correct": str(snippet.get("correct", "")),
            }
        )

    for snippet in sections.get("lecture_snippets", [])[:12]:
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

    for snippet in sections.get("notebook_snippets", [])[:12]:
        out.append(
            {
                "id": snippet.get("id", ""),
                "source": "notebook",
                "title": f"{snippet.get('topic','Notebook')} W{snippet.get('week','?')} cell {snippet.get('cell_index','?')}",
                "summary": compact(trim_lines(snippet.get("source", ""), 6), 340),
            }
        )

    return [x for x in out if x.get("id")]


def extract_json_blob(text: str) -> str:
    raw = (text or "").strip()
    if not raw:
        raise ValueError("Empty model output")

    if raw.startswith("```"):
        raw = re.sub(r"^```[a-zA-Z0-9_-]*\n", "", raw)
        raw = re.sub(r"\n```$", "", raw).strip()

    starts = [idx for idx in [raw.find("["), raw.find("{")] if idx != -1]
    if not starts:
        raise ValueError("No JSON start token found")

    start = min(starts)
    stack = []
    in_string = False
    escape = False

    for i in range(start, len(raw)):
        ch = raw[i]
        if in_string:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == '"':
                in_string = False
            continue

        if ch == '"':
            in_string = True
            continue

        if ch in "[{":
            stack.append(ch)
        elif ch in "]}":
            if not stack:
                continue
            open_ch = stack.pop()
            if (open_ch == "[" and ch != "]") or (open_ch == "{" and ch != "}"):
                raise ValueError("Mismatched JSON brackets")
            if not stack:
                return raw[start : i + 1]

    raise ValueError("JSON closing token not found")


def run_gemini(prompt: str) -> str:
    result = subprocess.run(
        ["gemini", "-m", MODEL, "-p", prompt],
        text=True,
        capture_output=True,
        timeout=180,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Gemini failed ({result.returncode}): {result.stderr.strip()[:400]}")
    return result.stdout.strip()


def fallback_result(card: dict[str, Any]) -> dict[str, Any]:
    sections = card.get("sections", {})
    traps = card.get("trap_patterns", [])
    bullets = sections.get("ai_common_questions", {}).get("bullets", [])
    fallback_points = []

    for trap in traps[:3]:
        if trap.get("trap"):
            fallback_points.append(compact(str(trap["trap"]), 170))

    for b in bullets[:4]:
        fallback_points.append(compact(f"Watch for this exam pattern: {b}", 170))

    if not fallback_points:
        fallback_points = [
            f"Trace {card.get('topic', 'the topic')} step by step and verify the exact output.",
            "Check object mutation vs new-object creation before choosing an answer.",
            "Confirm loop bounds and condition order before evaluating outputs.",
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
    cleaned = []
    for point in points:
        text = compact(str(point), 190).strip()
        if not text:
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
    return uniq[:8]


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


def chunked(seq: list[Any], size: int) -> list[list[Any]]:
    return [seq[i : i + size] for i in range(0, len(seq), size)]


def generate_chunk(chunk: list[dict[str, Any]]) -> list[dict[str, Any]]:
    prompt = f"""
You are helping produce exam-focused cheat sheet selections for an Intro Python midterm.
For EACH item in input, return one object with schema:
{{
  "id": "same id",
  "key_points_to_remember": ["3-7 short high-yield pitfalls/tricks that are actually tested"],
  "recommended_ids": ["IDs from source_candidates that should be included in Recommended for cheat sheet"]
}}

Selection rules:
- Prefer snippets that generalize to many exam questions.
- Prefer exam snippets that show common traps/output reasoning.
- Keep recommended_ids between 3 and 8 when possible.
- key_points should be concise, concrete, and exam-oriented.
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


def main() -> None:
    data = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    cards = data.get("cards", [])

    contexts = [context_for_card(card) for card in cards]
    chunks = chunked(contexts, CHUNK_SIZE)

    generated: dict[str, dict[str, Any]] = {}

    for idx, chunk in enumerate(chunks, start=1):
        print(f"Generating recommendations chunk {idx}/{len(chunks)} ({len(chunk)} topics)...", flush=True)
        try:
            out = generate_chunk(chunk)
            if len(out) != len(chunk):
                raise RuntimeError(f"Length mismatch expected {len(chunk)} got {len(out)}")

            for ctx, raw in zip(chunk, out):
                card = next((c for c in cards if c.get("id") == ctx["id"]), None)
                if not card or not isinstance(raw, dict):
                    continue

                valid_ids = {c.get("id") for c in ctx["source_candidates"] if c.get("id")}
                fallback = fallback_result(card)

                key_points = sanitize_key_points(raw.get("key_points_to_remember", []))
                if len(key_points) < 3:
                    key_points = sanitize_key_points(fallback["key_points_to_remember"])

                rec_ids = sanitize_recommended_ids(raw.get("recommended_ids", []), valid_ids)
                if len(rec_ids) < 2:
                    rec_ids = sanitize_recommended_ids(fallback["recommended_ids"], valid_ids)

                generated[ctx["id"]] = {
                    "key_points_to_remember": key_points,
                    "recommended_ids": rec_ids,
                }

        except Exception as exc:  # noqa: BLE001
            print(f"Chunk {idx} failed ({exc}). Using fallback for this chunk.", flush=True)
            for ctx in chunk:
                card = next((c for c in cards if c.get("id") == ctx["id"]), None)
                if not card:
                    continue
                fb = fallback_result(card)
                valid_ids = {c.get("id") for c in ctx["source_candidates"] if c.get("id")}
                generated[ctx["id"]] = {
                    "key_points_to_remember": sanitize_key_points(fb["key_points_to_remember"]),
                    "recommended_ids": sanitize_recommended_ids(fb["recommended_ids"], valid_ids),
                }

        time.sleep(0.5)

    for card in cards:
        cid = card.get("id")
        sections = card.setdefault("sections", {})
        bundle = generated.get(cid) or fallback_result(card)

        points = sanitize_key_points(bundle.get("key_points_to_remember", []))
        sections["key_points_to_remember"] = [
            {
                "id": f"kp-{i+1}",
                "text": p,
                "status": "generated",
                "model": MODEL,
                "generator": "gemini-cli",
            }
            for i, p in enumerate(points)
        ]

        valid_ids = {c.get("id") for c in snippet_candidates(card) if c.get("id")}
        rec_ids = sanitize_recommended_ids(bundle.get("recommended_ids", []), valid_ids)
        sections["recommended_ids"] = rec_ids

    notes = data.setdefault("meta", {}).setdefault("notes", [])
    notes.append("Generated key_points_to_remember and recommended_ids via gemini-cli.")

    CARDS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Updated {CARDS_FILE} with key points and recommendation splits for {len(cards)} cards.")


if __name__ == "__main__":
    main()
