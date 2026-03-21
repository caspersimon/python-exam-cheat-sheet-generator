#!/usr/bin/env python3

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _positive_int(value: Any) -> int | None:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed > 0 else None


def _append_error(errors: list[str], prefix: str, message: str) -> None:
    errors.append(f"{prefix}: {message}" if prefix else message)


def _check_python_code(
    code: Any,
    *,
    prefix: str,
    errors: list[str],
    warnings: list[str],
) -> None:
    text = _safe_str(code)
    if not text:
        _append_error(errors, prefix, "missing Python code")
        return
    try:
        ast.parse(text)
    except SyntaxError as exc:
        _append_error(errors, prefix, f"invalid Python syntax: {exc.msg}")
        return

    if len(text.splitlines()) > 120:
        warnings.append(f"{prefix}: code block is very long ({len(text.splitlines())} lines)")


def validate_week_payload(payload: dict[str, Any]) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return {"errors": ["Week payload must be a JSON object."], "warnings": []}

    week = _positive_int(payload.get("week"))
    if week is None:
        _append_error(errors, "week", "must be a positive integer")

    topics = [str(item).strip() for item in _safe_list(payload.get("topics")) if str(item).strip()]
    if not topics:
        warnings.append("topics: empty topic list")
    if len(topics) != len(set(topic.lower() for topic in topics)):
        warnings.append("topics: duplicate topic labels detected")

    lecture = payload.get("lecture")
    if lecture is not None and not isinstance(lecture, dict):
        _append_error(errors, "lecture", "must be an object")
        lecture = {}
    lecture = lecture or {}

    concepts = _safe_list(lecture.get("concepts"))
    if not concepts:
        warnings.append("lecture.concepts: empty concept list")
    for index, concept in enumerate(concepts, start=1):
        prefix = f"lecture.concepts[{index}]"
        if not isinstance(concept, dict):
            _append_error(errors, prefix, "must be an object")
            continue
        topic = _safe_str(concept.get("topic"))
        explanation = _safe_str(concept.get("explanation"))
        code_examples = [item for item in _safe_list(concept.get("code_examples")) if isinstance(item, dict)]
        if not topic:
            _append_error(errors, prefix, "topic is required")
        if not explanation and not code_examples:
            warnings.append(f"{prefix}: has neither explanation nor code examples")
        for code_index, code_example in enumerate(code_examples, start=1):
            code_prefix = f"{prefix}.code_examples[{code_index}]"
            if not _safe_str(code_example.get("code")):
                _append_error(errors, code_prefix, "code is required")
                continue
            _check_python_code(code_example.get("code"), prefix=code_prefix, errors=errors, warnings=warnings)

    lecture_questions = _safe_list(lecture.get("lecture_questions"))
    if not lecture_questions:
        warnings.append("lecture.lecture_questions: empty question list")
    for index, question in enumerate(lecture_questions, start=1):
        prefix = f"lecture.lecture_questions[{index}]"
        if not isinstance(question, dict):
            _append_error(errors, prefix, "must be an object")
            continue
        question_text = _safe_str(question.get("question"))
        options = question.get("options")
        correct = _safe_str(question.get("correct")).lower()
        if not question_text:
            _append_error(errors, prefix, "question text is required")
        if not isinstance(options, dict) or not options:
            _append_error(errors, prefix, "options must be a non-empty object")
            continue
        valid_keys = {str(key).strip().lower() for key, value in options.items() if _safe_str(value)}
        if len(valid_keys) < 2:
            warnings.append(f"{prefix}: fewer than two non-empty options")
        if correct and correct not in valid_keys:
            _append_error(errors, prefix, f"correct={correct!r} is not present in options")

    notebook_cells = _safe_list(payload.get("notebook_cells"))
    if not notebook_cells:
        warnings.append("notebook_cells: empty notebook cell list")
    seen_indexes: set[int] = set()
    for index, cell in enumerate(notebook_cells, start=1):
        prefix = f"notebook_cells[{index}]"
        if not isinstance(cell, dict):
            _append_error(errors, prefix, "must be an object")
            continue
        cell_index = _positive_int(cell.get("cell_index"))
        if cell_index is None:
            _append_error(errors, prefix, "cell_index must be a positive integer")
            continue
        if cell_index in seen_indexes:
            _append_error(errors, prefix, f"duplicate cell_index {cell_index}")
        seen_indexes.add(cell_index)

        cell_type = _safe_str(cell.get("cell_type")).lower() or "code"
        if cell_type not in {"code", "markdown", "raw"}:
            warnings.append(f"{prefix}: unusual cell_type {cell_type!r}")

        if cell_type == "code":
            _check_python_code(cell.get("source"), prefix=f"{prefix}.source", errors=errors, warnings=warnings)

    sources = [_safe_str(item) for item in _safe_list(payload.get("sources")) if _safe_str(item)]
    if sources and len(sources) != len({item.lower() for item in sources}):
        warnings.append("sources: duplicate source path detected")

    return {"errors": errors, "warnings": warnings}


def _validate_exam_question(question: dict[str, Any], *, prefix: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    question_text = _safe_str(question.get("question"))
    options = question.get("options")
    correct = _safe_str(question.get("correct")).lower()
    if not question_text:
        _append_error(errors, prefix, "question text is required")
    if not isinstance(options, dict) or not options:
        _append_error(errors, prefix, "options must be a non-empty object")
    else:
        valid_keys = {str(key).strip().lower() for key, value in options.items() if _safe_str(value)}
        if len(valid_keys) < 2:
            warnings.append(f"{prefix}: fewer than two non-empty options")
        if correct and correct not in valid_keys:
            _append_error(errors, prefix, f"correct={correct!r} is not present in options")

    for field in ["code_context", "solution", "code", "answer_code"]:
        value = _safe_str(question.get(field))
        if value:
            _check_python_code(value, prefix=f"{prefix}.{field}", errors=errors, warnings=warnings)

    explanation = _safe_str(question.get("explanation"))
    if not explanation:
        warnings.append(f"{prefix}: missing explanation")

    return errors, warnings


def validate_exam_payload(payload: dict[str, Any]) -> dict[str, list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(payload, dict):
        return {"errors": ["Exam payload must be a JSON object."], "warnings": []}

    exams = _safe_list(payload.get("exams"))
    if not exams and _safe_list(payload.get("questions")):
        exams = [{"questions": _safe_list(payload.get("questions")), "exam_label": payload.get("exam_label", "exam")}]  # type: ignore[list-item]
    if not exams:
        _append_error(errors, "exams", "must be a non-empty list or payload must provide questions")
        return {"errors": errors, "warnings": warnings}

    for exam_index, exam in enumerate(exams, start=1):
        prefix = f"exams[{exam_index}]"
        if not isinstance(exam, dict):
            _append_error(errors, prefix, "must be an object")
            continue

        exam_label = _safe_str(exam.get("exam_label") or exam.get("label") or exam.get("source") or f"exam-{exam_index}")
        if not exam_label:
            _append_error(errors, prefix, "exam_label is required")

        questions = _safe_list(exam.get("questions"))
        if not questions:
            _append_error(errors, prefix, "questions must be a non-empty list")
            continue

        for question_index, question in enumerate(questions, start=1):
            question_prefix = f"{prefix}.questions[{question_index}]"
            if not isinstance(question, dict):
                _append_error(errors, question_prefix, "must be an object")
                continue
            q_errors, q_warnings = _validate_exam_question(question, prefix=question_prefix)
            errors.extend(q_errors)
            warnings.extend(q_warnings)

    return {"errors": errors, "warnings": warnings}


def validate_payload(payload: dict[str, Any], *, kind: str) -> dict[str, list[str]]:
    kind = kind.lower()
    if kind == "week":
        return validate_week_payload(payload)
    if kind == "exam":
        return validate_exam_payload(payload)
    if kind != "bundle":
        return {"errors": [f"Unknown extraction kind: {kind}"], "warnings": []}

    errors: list[str] = []
    warnings: list[str] = []

    if "week" in payload or "lecture" in payload or "notebook_cells" in payload:
        week_report = validate_week_payload(payload)
        errors.extend(week_report["errors"])
        warnings.extend(week_report["warnings"])

    if "exams" in payload or "questions" in payload:
        exam_report = validate_exam_payload(payload)
        errors.extend(exam_report["errors"])
        warnings.extend(exam_report["warnings"])

    if not errors and not warnings and not any(key in payload for key in ("week", "lecture", "notebook_cells", "exams", "questions")):
        warnings.append("bundle payload has no recognized extraction sections")

    return {"errors": errors, "warnings": warnings}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate extracted raw course material before canonical ingestion.")
    parser.add_argument("--input", type=Path, required=True, help="Path to an extracted material JSON file.")
    parser.add_argument(
        "--kind",
        choices=["week", "exam", "bundle"],
        default="bundle",
        help="Which extraction contract to validate.",
    )
    parser.add_argument("--report-file", type=Path, default=None, help="Optional JSON report destination.")
    return parser.parse_args()


def _report_path(explicit: Path | None) -> Path | None:
    if explicit is None:
        return None
    explicit.parent.mkdir(parents=True, exist_ok=True)
    return explicit


def main() -> None:
    args = parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise SystemExit("Input JSON must be an object.")

    report = validate_payload(payload, kind=args.kind)
    report.update(
        {
            "kind": args.kind,
            "input_file": str(args.input),
            "status": "fail" if report["errors"] else "pass",
        }
    )

    report_path = _report_path(args.report_file)
    if report_path is not None:
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    if report["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
