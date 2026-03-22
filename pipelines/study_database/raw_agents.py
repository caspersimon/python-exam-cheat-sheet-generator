from __future__ import annotations

import json
from typing import Any

from pipelines.shared import SMART_GEMINI_AGENT, extract_json_blob, run_gemini_cli, trim_lines

from .raw_sources import RawSourceRecord

RAW_TIMEOUT_SECONDS = 900
RAW_STDERR_CLIP = 1200
DEFAULT_MODEL = SMART_GEMINI_AGENT
RETRY_LIMIT = 2


def _records_payload(records: list[RawSourceRecord]) -> list[dict[str, Any]]:
    return [
        {
            "path": record.relative_path,
            "kind": record.kind,
            "role": record.role,
            "week": record.week,
            "text": trim_lines(record.text, 220),
        }
        for record in records
    ]


def run_json_agent(prompt: str, *, model: str = DEFAULT_MODEL, timeout_seconds: int = RAW_TIMEOUT_SECONDS) -> Any:
    last_error: Exception | None = None
    for _ in range(RETRY_LIMIT + 1):
        try:
            raw = run_gemini_cli(prompt, model=model, timeout_seconds=timeout_seconds, stderr_clip=RAW_STDERR_CLIP)
            blob = extract_json_blob(raw)
            return json.loads(blob)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
    raise RuntimeError(f"Raw ingestion agent failed after retries: {last_error}")


def build_week_prompt(week: int, records: list[RawSourceRecord], *, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "week": week,
        "source_files": _records_payload(records),
    }
    return f"""
You are extracting one week of Intro to Python course material into a canonical study-database JSON object.
Return ONLY valid JSON with this exact schema:
{{
  "week": {week},
  "topics": ["short topic labels"],
  "lecture": {{
    "concepts": [
      {{
        "topic": "string",
        "explanation": "exam-focused explanation",
        "code_examples": [
          {{
            "description": "string",
            "code": "python code"
          }}
        ]
      }}
    ],
    "lecture_questions": [
      {{
        "topic": "string",
        "question": "string",
        "options": {{"a":"...","b":"...","c":"...","d":"..."}},
        "correct": "a|b|c|d",
        "explanation": "string"
      }}
    ]
  }},
  "notebook_cells": [
    {{
      "cell_index": 1,
      "cell_type": "code|markdown|raw",
      "topic": "string",
      "is_advanced_optional": false,
      "source": "cleaned notebook or exercise snippet",
      "outputs": ["optional output"]
    }}
  ],
  "sources": ["relative/path"]
}}

Rules:
- Use the lecture deck, notebook, exercise files, and solution files together.
- Pair matching exercise and solution files when they belong together.
- Include only study-relevant content, but do not invent facts not present in the sources.
- Keep code examples syntactically valid Python.
- Return only JSON.

Raw input:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


def build_assessment_prompt(record: RawSourceRecord, *, model: str = DEFAULT_MODEL) -> str:
    payload = {
        "source_file": record.relative_path,
        "kind": record.kind,
        "text": trim_lines(record.text, 260),
    }
    return f"""
You are extracting one exam or practice-exam PDF into a canonical assessment JSON object.
Return ONLY valid JSON with this exact schema:
{{
  "exam_label": "short stable label",
  "source": "relative/path/to/pdf",
  "year": "year or unknown",
  "questions": [
    {{
      "number": 1,
      "topic": "string",
      "question": "string",
      "options": {{"a":"...","b":"...","c":"...","d":"..."}},
      "correct": "a|b|c|d",
      "explanation": "string",
      "code_context": "optional python snippet or empty string"
    }}
  ],
  "notes": ["short review notes"]
}}

Rules:
- Preserve the answer options exactly when they are shown in the PDF.
- Clean up weird formatting, but do not rewrite the meaning.
- Keep code context as valid Python when the PDF contains code.
- Return only JSON.

Raw input:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()


def build_unassigned_prompt(records: list[RawSourceRecord]) -> str:
    payload = {
        "unassigned_files": _records_payload(records),
    }
    return f"""
You are classifying a few raw course files that do not have a week number in their file name.
Return ONLY valid JSON with this exact schema:
{{
  "assignments": [
    {{
      "path": "relative/path",
      "bucket": "week|assessment|ignore",
      "week": 6,
      "role": "lecture|notebook|exercise|solution|supporting",
      "reason": "short reason"
    }}
  ],
  "notes": ["short review notes"]
}}

Rules:
- Prefer the week that best matches the file's actual content.
- Use "ignore" only for true noise.
- Return only JSON.

Raw input:
{json.dumps(payload, ensure_ascii=False, indent=2)}
""".strip()
