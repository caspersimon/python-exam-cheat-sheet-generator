from __future__ import annotations

import ast
from copy import deepcopy
from typing import Any

from pipelines.shared import SMART_GEMINI_AGENT, chunked
from .ai_helpers import curate_lecture_with_ai, curate_notebook_chunk_with_ai

MODEL_DEFAULT = SMART_GEMINI_AGENT
NOTEBOOK_CHUNK_SIZE = 30


class WeekCurationError(RuntimeError):
    pass


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _to_week(value: Any) -> int:
    try:
        week = int(value)
    except (TypeError, ValueError) as exc:
        raise WeekCurationError(f"Invalid week value: {value!r}") from exc
    if week <= 0:
        raise WeekCurationError(f"Week must be positive, got: {week}")
    return week


def normalize_week_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw_payload, dict):
        raise WeekCurationError("Week payload must be a JSON object.")

    week = _to_week(raw_payload.get("week"))
    lecture = raw_payload.get("lecture") if isinstance(raw_payload.get("lecture"), dict) else {}

    concepts = _safe_list(lecture.get("concepts"))
    lecture_questions = _safe_list(lecture.get("lecture_questions"))
    notebook_cells = _safe_list(raw_payload.get("notebook_cells"))

    normalized = {
        "week": week,
        "topics": [str(topic).strip() for topic in _safe_list(raw_payload.get("topics")) if str(topic).strip()],
        "lecture": {
            "concepts": [deepcopy(item) for item in concepts if isinstance(item, dict)],
            "lecture_questions": [deepcopy(item) for item in lecture_questions if isinstance(item, dict)],
        },
        "notebook_cells": [deepcopy(item) for item in notebook_cells if isinstance(item, dict)],
        "sources": [str(source).strip() for source in _safe_list(raw_payload.get("sources")) if str(source).strip()],
    }

    for concept in normalized["lecture"]["concepts"]:
        concept.setdefault("week", week)
    for question in normalized["lecture"]["lecture_questions"]:
        question.setdefault("week", week)
    for cell in normalized["notebook_cells"]:
        cell["week"] = week
        cell.setdefault("topic", "")
        cell.setdefault("cell_type", "code")
        cell.setdefault("outputs", [])
        cell.setdefault("is_advanced_optional", False)

    if not normalized["lecture"]["concepts"] and not normalized["notebook_cells"]:
        raise WeekCurationError("Week payload is empty: provide at least lecture concepts or notebook cells.")

    return normalized


def _python_parse_ok(code: str) -> bool:
    text = _safe_str(code)
    if not text:
        return True
    try:
        ast.parse(text)
        return True
    except SyntaxError:
        return False


def _curate_notebooks(payload: dict[str, Any], *, model: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    original_cells = payload["notebook_cells"]
    if not original_cells:
        return [], {"total_cells": 0, "kept_cells": 0, "dropped_cells": 0, "invalid_code_cells": []}

    by_index = {cell.get("cell_index"): cell for cell in original_cells}
    kept: list[dict[str, Any]] = []
    dropped = 0
    invalid_code_cells: list[int] = []

    for chunk_cells in chunked(original_cells, NOTEBOOK_CHUNK_SIZE):
        curated_chunk = curate_notebook_chunk_with_ai(chunk_cells, model=model)
        if len(curated_chunk) != len(chunk_cells):
            raise WeekCurationError(
                f"Notebook curation length mismatch: expected {len(chunk_cells)}, got {len(curated_chunk)}"
            )
        for item in curated_chunk:
            cell_index = item.get("cell_index")
            original = by_index.get(cell_index)
            if not isinstance(original, dict):
                dropped += 1
                continue

            keep = bool(item.get("keep"))
            score = int(item.get("score") or 0)
            if not keep or score < 3:
                dropped += 1
                continue

            materialized = deepcopy(original)
            materialized["topic"] = _safe_str(item.get("topic")) or _safe_str(original.get("topic"))
            materialized["is_advanced_optional"] = bool(item.get("is_advanced_optional"))
            materialized["source"] = _safe_str(item.get("source")) or _safe_str(original.get("source"))
            materialized["outputs"] = [str(out) for out in _safe_list(item.get("outputs")) if str(out).strip()]
            materialized["curation"] = {
                "score": score,
                "reason": _safe_str(item.get("reason")),
                "generator": "gemini-cli",
                "model": model,
            }

            if _safe_str(materialized.get("cell_type")).lower() == "code" and not _python_parse_ok(materialized["source"]):
                invalid_code_cells.append(int(materialized.get("cell_index") or 0))

            kept.append(materialized)

    kept.sort(key=lambda cell: int(cell.get("cell_index") or 0))
    report = {
        "total_cells": len(original_cells),
        "kept_cells": len(kept),
        "dropped_cells": dropped,
        "invalid_code_cells": sorted([idx for idx in invalid_code_cells if idx]),
    }
    return kept, report


def curate_week_payload(payload: dict[str, Any], *, model: str = MODEL_DEFAULT) -> tuple[dict[str, Any], dict[str, Any]]:
    normalized = normalize_week_payload(payload)
    try:
        lecture_curated, lecture_report = curate_lecture_with_ai(normalized, model=model)
        notebook_curated, notebook_report = _curate_notebooks(normalized, model=model)
    except Exception as exc:  # noqa: BLE001
        raise WeekCurationError(f"AI curation failed: {exc}") from exc

    week = normalized["week"]
    curated = {
        "week": week,
        "topics": lecture_curated["topics"] or normalized["topics"],
        "lecture": {
            "concepts": lecture_curated["concepts"],
            "lecture_questions": lecture_curated["lecture_questions"],
        },
        "notebook_cells": notebook_curated,
        "sources": normalized["sources"],
        "curation_meta": {
            "generator": "gemini-cli",
            "model": model,
        },
    }

    for concept in curated["lecture"]["concepts"]:
        concept["week"] = week
    for question in curated["lecture"]["lecture_questions"]:
        question["week"] = week
    for cell in curated["notebook_cells"]:
        cell["week"] = week

    report = {
        "week": week,
        "generator": "gemini-cli",
        "model": model,
        "lecture": {
            "input_concepts": len(normalized["lecture"]["concepts"]),
            "curated_concepts": len(curated["lecture"]["concepts"]),
            "input_lecture_questions": len(normalized["lecture"]["lecture_questions"]),
            "curated_lecture_questions": len(curated["lecture"]["lecture_questions"]),
            "quality_notes": lecture_report["quality_notes"],
        },
        "notebooks": notebook_report,
    }
    return curated, report
