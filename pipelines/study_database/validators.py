from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _as_positive_int(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    if parsed <= 0:
        return None
    return parsed


def analyze_week_payload(payload: dict[str, Any]) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return {
            "errors": ["Week payload must be a JSON object."],
            "warnings": [],
        }

    week = _as_positive_int(payload.get("week"))
    if week is None:
        errors.append("`week` must be a positive integer.")

    topics = [str(topic).strip() for topic in _safe_list(payload.get("topics")) if str(topic).strip()]
    if topics and isinstance(_safe_list(payload.get("topics"))[0], dict):
        return analyze_v3_week_payload(payload)

    seen_topics: set[str] = set()
    for topic in topics:
        normalized = topic.lower()
        if normalized in seen_topics:
            warnings.append(f"Duplicate topic label detected: {topic!r}")
            continue
        seen_topics.add(normalized)

    lecture = payload.get("lecture")
    if lecture is not None and not isinstance(lecture, dict):
        errors.append("`lecture` must be an object when provided.")
        lecture = {}
    lecture = lecture or {}

    concepts = _safe_list(lecture.get("concepts"))
    for index, concept in enumerate(concepts, start=1):
        if not isinstance(concept, dict):
            errors.append(f"`lecture.concepts[{index}]` must be an object.")
            continue
        topic = _safe_str(concept.get("topic"))
        explanation = _safe_str(concept.get("explanation"))
        code_examples = [item for item in _safe_list(concept.get("code_examples")) if isinstance(item, dict)]

        if not topic:
            warnings.append(f"`lecture.concepts[{index}]` has no topic label.")
        if not explanation and not code_examples:
            warnings.append(f"`lecture.concepts[{index}]` has neither explanation nor code examples.")

    lecture_questions = _safe_list(lecture.get("lecture_questions"))
    for index, question in enumerate(lecture_questions, start=1):
        if not isinstance(question, dict):
            errors.append(f"`lecture.lecture_questions[{index}]` must be an object.")
            continue
        question_text = _safe_str(question.get("question"))
        options = question.get("options")
        if not question_text:
            warnings.append(f"`lecture.lecture_questions[{index}]` has empty question text.")
        if not isinstance(options, dict) or not options:
            errors.append(f"`lecture.lecture_questions[{index}].options` must be a non-empty object.")
            continue
        valid_keys = {str(key).strip().lower() for key, value in options.items() if _safe_str(value)}
        if len(valid_keys) < 2:
            warnings.append(f"`lecture.lecture_questions[{index}]` has fewer than 2 non-empty options.")
        correct = _safe_str(question.get("correct")).lower()
        if correct and correct not in valid_keys:
            errors.append(
                f"`lecture.lecture_questions[{index}].correct={correct!r}` is not present in options: {sorted(valid_keys)}"
            )

    def bucket_label(bucket: str) -> str:
        return bucket.replace("_cells", " cell")

    def validate_cells(bucket: str, cells: list[Any]) -> None:
        seen_cell_indexes: set[int] = set()
        for index, cell in enumerate(cells, start=1):
            if not isinstance(cell, dict):
                errors.append(f"`{bucket}[{index}]` must be an object.")
                continue
            cell_index = _as_positive_int(cell.get("cell_index"))
            if cell_index is None:
                errors.append(f"`{bucket}[{index}].cell_index` must be a positive integer.")
                continue
            if cell_index in seen_cell_indexes:
                errors.append(f"Duplicate {bucket_label(bucket)}_index found: {cell_index}")
            seen_cell_indexes.add(cell_index)

            cell_type = _safe_str(cell.get("cell_type")).lower()
            if cell_type and cell_type not in {"code", "markdown", "raw"}:
                warnings.append(
                    f"`{bucket}[{index}].cell_type={cell_type!r}` is unusual (expected code/markdown/raw)."
                )

    notebook_cells = _safe_list(payload.get("notebook_cells"))
    validate_cells("notebook_cells", notebook_cells)

    homework_cells = _safe_list(payload.get("homework_cells"))
    validate_cells("homework_cells", homework_cells)

    sources = [str(source).strip() for source in _safe_list(payload.get("sources")) if str(source).strip()]
    seen_sources: set[str] = set()
    for source in sources:
        normalized = source.lower()
        if normalized in seen_sources:
            warnings.append(f"Duplicate source path detected: {source}")
            continue
        seen_sources.add(normalized)

    if not concepts and not notebook_cells and not homework_cells:
        errors.append("Payload must include at least one lecture concept, notebook cell, or homework cell.")

    return {
        "errors": errors,
        "warnings": warnings,
    }


def analyze_v3_week_payload(payload: dict[str, Any]) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    week = _as_positive_int(payload.get("week"))
    if week is None:
        errors.append("`week` must be a positive integer.")

    topics = _safe_list(payload.get("topics"))
    if not topics:
        errors.append("`topics` must contain at least one topic object.")

    seen_topic_ids: set[str] = set()
    seen_subtopic_ids: set[str] = set()
    seen_snippet_ids: set[str] = set()

    for topic_index, topic in enumerate(topics, start=1):
        if not isinstance(topic, dict):
            errors.append(f"`topics[{topic_index}]` must be an object.")
            continue
        topic_id = _safe_str(topic.get("id"))
        if not topic_id:
            errors.append(f"`topics[{topic_index}].id` must be a non-empty string.")
        elif topic_id in seen_topic_ids:
            errors.append(f"Duplicate topic id found: {topic_id}")
        else:
            seen_topic_ids.add(topic_id)

        if not _safe_str(topic.get("title")):
            warnings.append(f"`topics[{topic_index}].title` is empty.")

        subtopics = _safe_list(topic.get("subtopics"))
        if not subtopics:
            warnings.append(f"`topics[{topic_index}]` has no subtopics.")

        for subtopic_index, subtopic in enumerate(subtopics, start=1):
            if not isinstance(subtopic, dict):
                errors.append(f"`topics[{topic_index}].subtopics[{subtopic_index}]` must be an object.")
                continue
            subtopic_id = _safe_str(subtopic.get("id"))
            if not subtopic_id:
                errors.append(f"`topics[{topic_index}].subtopics[{subtopic_index}].id` must be a non-empty string.")
            elif subtopic_id in seen_subtopic_ids:
                errors.append(f"Duplicate subtopic id found: {subtopic_id}")
            else:
                seen_subtopic_ids.add(subtopic_id)

            if not _safe_str(subtopic.get("title")):
                warnings.append(f"`topics[{topic_index}].subtopics[{subtopic_index}].title` is empty.")

            for bucket_name in ["knowledge_snippets", "code_snippets", "question_snippets"]:
                bucket = _safe_list(subtopic.get(bucket_name))
                for snippet_index, snippet in enumerate(bucket, start=1):
                    if not isinstance(snippet, dict):
                        errors.append(
                            f"`topics[{topic_index}].subtopics[{subtopic_index}].{bucket_name}[{snippet_index}]` must be an object."
                        )
                        continue
                    snippet_id = _safe_str(snippet.get("id"))
                    if not snippet_id:
                        errors.append(
                            f"`topics[{topic_index}].subtopics[{subtopic_index}].{bucket_name}[{snippet_index}].id` must be a non-empty string."
                        )
                    elif snippet_id in seen_snippet_ids:
                        errors.append(f"Duplicate snippet id found: {snippet_id}")
                    else:
                        seen_snippet_ids.add(snippet_id)
                    if not _safe_str(snippet.get("kind")):
                        warnings.append(
                            f"`topics[{topic_index}].subtopics[{subtopic_index}].{bucket_name}[{snippet_index}].kind` is empty."
                        )
                    if not _safe_str(snippet.get("content")):
                        warnings.append(
                            f"`topics[{topic_index}].subtopics[{subtopic_index}].{bucket_name}[{snippet_index}].content` is empty."
                        )
                    if not isinstance(snippet.get("source_refs"), list) or not snippet.get("source_refs"):
                        errors.append(
                            f"`topics[{topic_index}].subtopics[{subtopic_index}].{bucket_name}[{snippet_index}].source_refs` must be a non-empty list."
                        )
                    if not isinstance(snippet.get("curation_meta"), dict):
                        errors.append(
                            f"`topics[{topic_index}].subtopics[{subtopic_index}].{bucket_name}[{snippet_index}].curation_meta` must be an object."
                        )

    sources = [str(source).strip() for source in _safe_list(payload.get("sources")) if str(source).strip()]
    seen_sources: set[str] = set()
    for source in sources:
        normalized = source.lower()
        if normalized in seen_sources:
            warnings.append(f"Duplicate source path detected: {source}")
            continue
        seen_sources.add(normalized)

    return {"errors": errors, "warnings": warnings}


def normalize_assessment_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw_payload, dict):
        raise ValueError("Assessment payload must be a JSON object.")

    questions = [deepcopy(item) for item in _safe_list(raw_payload.get("questions")) if isinstance(item, dict)]
    return {
        "exam_label": _safe_str(raw_payload.get("exam_label")),
        "source": _safe_str(raw_payload.get("source")),
        "year": _safe_str(raw_payload.get("year")) or "unknown",
        "questions": questions,
        "notes": [str(note).strip() for note in _safe_list(raw_payload.get("notes")) if str(note).strip()],
        "ignored": bool(raw_payload.get("ignored")),
    }


def analyze_assessment_payload(payload: dict[str, Any]) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return {
            "errors": ["Assessment payload must be a JSON object."],
            "warnings": [],
        }

    if payload.get("ignored"):
        if not _safe_str(payload.get("exam_label")):
            errors.append("Ignored assessment payloads still need a stable `exam_label`.")
        if not _safe_str(payload.get("source")):
            errors.append("Ignored assessment payloads still need a non-empty `source`.")
        return {"errors": errors, "warnings": warnings}

    exam_label = _safe_str(payload.get("exam_label"))
    source = _safe_str(payload.get("source"))
    year = _safe_str(payload.get("year"))

    if not exam_label:
        errors.append("`exam_label` must be a non-empty string.")
    if not source:
        errors.append("`source` must be a non-empty string.")
    if not year:
        warnings.append("`year` is empty; use `unknown` when no year is known.")

    questions = _safe_list(payload.get("questions"))
    if not questions:
        errors.append("Assessment payload must include at least one question.")

    seen_numbers: set[int] = set()
    for index, question in enumerate(questions, start=1):
        if not isinstance(question, dict):
            errors.append(f"`questions[{index}]` must be an object.")
            continue

        number = _as_positive_int(question.get("number"))
        if number is not None:
            if number in seen_numbers:
                errors.append(f"Duplicate assessment question number found: {number}")
            seen_numbers.add(number)
        elif question.get("number") is not None:
            warnings.append(f"`questions[{index}].number` is not a positive integer.")

        question_text = _safe_str(question.get("question"))
        if not question_text:
            warnings.append(f"`questions[{index}]` has empty question text.")

        options = question.get("options")
        if not isinstance(options, dict) or not options:
            errors.append(f"`questions[{index}].options` must be a non-empty object.")
            continue

        valid_keys = {str(key).strip().lower() for key, value in options.items() if _safe_str(value)}
        if len(valid_keys) < 2:
            warnings.append(f"`questions[{index}]` has fewer than 2 non-empty options.")

        correct = _safe_str(question.get("correct")).lower()
        if correct and correct not in valid_keys:
            errors.append(
                f"`questions[{index}].correct={correct!r}` is not present in options: {sorted(valid_keys)}"
            )

    return {
        "errors": errors,
        "warnings": warnings,
    }


def missing_source_paths(payload: dict[str, Any], *, root_dir: Path) -> list[str]:
    missing: list[str] = []
    for source in _safe_list(payload.get("sources")):
        source_path = _safe_str(source)
        if not source_path:
            continue
        candidate = Path(source_path)
        if not candidate.is_absolute():
            candidate = root_dir / source_path
        if not candidate.exists():
            missing.append(source_path)
    return missing
