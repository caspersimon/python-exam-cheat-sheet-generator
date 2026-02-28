from __future__ import annotations

import json
from typing import Any

from pipelines.shared import compact_text, extract_json_blob, run_gemini_cli, trim_lines

RETRY_LIMIT = 2


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _gemini_json(prompt: str, *, model: str, timeout_seconds: int = 240) -> Any:
    last_error: Exception | None = None
    for _ in range(RETRY_LIMIT + 1):
        try:
            raw = run_gemini_cli(
                prompt,
                model=model,
                timeout_seconds=timeout_seconds,
                stderr_clip=600,
            )
            blob = extract_json_blob(raw)
            return json.loads(blob)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise RuntimeError(f"Gemini curation failed after retries: {last_error}")


def _lecture_context(payload: dict[str, Any]) -> dict[str, Any]:
    concepts = []
    for idx, concept in enumerate(payload["lecture"]["concepts"], start=1):
        code_examples = []
        for code_ex in _safe_list(concept.get("code_examples"))[:3]:
            if not isinstance(code_ex, dict):
                continue
            code = trim_lines(_safe_str(code_ex.get("code")), 10)
            if not code:
                continue
            code_examples.append(
                {
                    "description": compact_text(_safe_str(code_ex.get("description")), 100),
                    "code": code,
                }
            )
        concepts.append(
            {
                "id": f"c{idx}",
                "topic": compact_text(_safe_str(concept.get("topic")), 110),
                "explanation": compact_text(_safe_str(concept.get("explanation")), 360),
                "code_examples": code_examples,
            }
        )

    questions = []
    for idx, question in enumerate(payload["lecture"]["lecture_questions"], start=1):
        questions.append(
            {
                "id": f"q{idx}",
                "topic": compact_text(_safe_str(question.get("topic")), 110),
                "question": compact_text(_safe_str(question.get("question")), 320),
                "options": question.get("options", {}),
                "correct": question.get("correct"),
                "explanation": compact_text(_safe_str(question.get("explanation")), 220),
            }
        )
    return {"concepts": concepts, "lecture_questions": questions}


def curate_lecture_with_ai(payload: dict[str, Any], *, model: str) -> tuple[dict[str, Any], dict[str, Any]]:
    context = _lecture_context(payload)
    prompt = f"""
You are curating course material for an Intro to Python exam database.
Return ONE JSON object with this exact schema:
{{
  "topics": ["clean topic labels"],
  "concepts": [
    {{
      "topic": "string",
      "explanation": "short, exam-relevant explanation",
      "code_examples": [{{"description":"string","code":"python code"}}]
    }}
  ],
  "lecture_questions": [
    {{
      "topic": "string",
      "question": "question text",
      "options": {{"a":"..","b":"..","c":"..","d":".."}},
      "correct": "a/b/c/d",
      "explanation": "concise reasoning"
    }}
  ],
  "quality_notes": ["specific quality risks or missing details"]
}}

Rules:
- Keep only high-value exam-relevant concepts/questions.
- Remove duplicates and vague filler.
- Keep code examples syntactically valid and <= 10 lines.
- Do not invent advanced topics not present in input.
- Return ONLY JSON.

Input week material:
{json.dumps(context, ensure_ascii=False, indent=2)}
""".strip()

    data = _gemini_json(prompt, model=model)
    if not isinstance(data, dict):
        raise ValueError("Lecture curation output must be a JSON object.")

    curated = {
        "topics": [str(topic).strip() for topic in _safe_list(data.get("topics")) if str(topic).strip()],
        "concepts": [item for item in _safe_list(data.get("concepts")) if isinstance(item, dict)],
        "lecture_questions": [item for item in _safe_list(data.get("lecture_questions")) if isinstance(item, dict)],
    }
    notes = {
        "quality_notes": [str(note).strip() for note in _safe_list(data.get("quality_notes")) if str(note).strip()]
    }
    return curated, notes


def _notebook_context_cells(cells: list[dict[str, Any]]) -> list[dict[str, Any]]:
    context = []
    for cell in cells:
        context.append(
            {
                "cell_index": cell.get("cell_index"),
                "cell_type": _safe_str(cell.get("cell_type")) or "code",
                "topic": compact_text(_safe_str(cell.get("topic")), 80),
                "is_advanced_optional": bool(cell.get("is_advanced_optional")),
                "source": trim_lines(_safe_str(cell.get("source")), 12),
                "outputs": [compact_text(_safe_str(out), 140) for out in _safe_list(cell.get("outputs"))[:2]],
            }
        )
    return context


def curate_notebook_chunk_with_ai(cells: list[dict[str, Any]], *, model: str) -> list[dict[str, Any]]:
    prompt = f"""
You are curating notebook cells for an Intro to Python exam study database.
Return ONLY a JSON array with one object per input cell:
[
  {{
    "cell_index": 12,
    "keep": true,
    "topic": "short topic label",
    "is_advanced_optional": false,
    "source": "cleaned source text",
    "outputs": ["optional cleaned outputs"],
    "score": 1,
    "reason": "short reason"
  }}
]

Rules:
- Keep high-signal exam-relevant cells; drop low-value noise.
- Preserve core code/markdown meaning, only clean formatting.
- `score` must be an integer 1-5 (5 highest quality).
- Keep the same number of returned objects as input.
- Return only JSON.

Input cells:
{json.dumps(_notebook_context_cells(cells), ensure_ascii=False, indent=2)}
""".strip()

    curated = _gemini_json(prompt, model=model)
    if not isinstance(curated, list):
        raise ValueError("Notebook curation output must be a JSON array.")
    return [item for item in curated if isinstance(item, dict)]
