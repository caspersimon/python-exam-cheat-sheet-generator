from __future__ import annotations

import ast
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .raw_agents import build_assessment_prompt, build_unassigned_prompt, build_week_prompt, run_json_agent
from .raw_sources import RawSourceRecord, collect_raw_source_records
from .curation import normalize_week_payload
from .validators import analyze_assessment_payload, analyze_week_payload, normalize_assessment_payload


@dataclass(slots=True)
class IngestionArtifact:
    source: str
    payload_file: str
    review_file: str
    payload_type: str
    warnings: list[str]
    errors: list[str]


def _slug(value: str) -> str:
    text = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return text or "item"


def _validate_python_code_blocks(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []

    for concept_index, concept in enumerate(payload.get("lecture", {}).get("concepts", []), start=1):
        for example_index, example in enumerate(concept.get("code_examples") or [], start=1):
            code = str(example.get("code") or "").strip()
            if not code:
                continue
            try:
                ast.parse(code)
            except SyntaxError as exc:
                errors.append(
                    f"lecture.concepts[{concept_index}].code_examples[{example_index}] failed syntax check: {exc.msg}"
                )

    for cell_index, cell in enumerate(payload.get("notebook_cells", []), start=1):
        code = str(cell.get("source") or "").strip()
        cell_type = str(cell.get("cell_type") or "").strip().lower()
        if cell_type != "code" or not code:
            continue
        try:
            ast.parse(code)
        except SyntaxError as exc:
            errors.append(f"notebook_cells[{cell_index}] failed syntax check: {exc.msg}")

    return errors


def _validate_assessment_code_blocks(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for index, question in enumerate(payload.get("questions", []), start=1):
        code = str(question.get("code_context") or "").strip()
        if not code:
            continue
        try:
            ast.parse(code)
        except SyntaxError as exc:
            errors.append(f"questions[{index}].code_context failed syntax check: {exc.msg}")
    return errors


def _group_records(records: list[RawSourceRecord]) -> tuple[dict[int, list[RawSourceRecord]], list[RawSourceRecord], list[RawSourceRecord]]:
    weeks: dict[int, list[RawSourceRecord]] = {}
    assessments: list[RawSourceRecord] = []
    unassigned: list[RawSourceRecord] = []

    for record in records:
        if record.kind == "pdf":
            assessments.append(record)
            continue
        if record.week is not None:
            weeks.setdefault(record.week, []).append(record)
            continue
        unassigned.append(record)
    return weeks, assessments, unassigned


def _apply_unassigned_assignments(
    weeks: dict[int, list[RawSourceRecord]],
    assessments: list[RawSourceRecord],
    unassigned: list[RawSourceRecord],
    assignments: list[dict[str, Any]],
) -> list[str]:
    notes: list[str] = []
    lookup = {record.relative_path: record for record in unassigned}
    for assignment in assignments:
        path = str(assignment.get("path") or "").strip()
        bucket = str(assignment.get("bucket") or "").strip().lower()
        record = lookup.get(path)
        if not record:
            continue
        if bucket == "week":
            week = assignment.get("week")
            if isinstance(week, int) and week > 0:
                weeks.setdefault(week, []).append(record)
                notes.append(f"Assigned {path} to week {week}")
            continue
        if bucket == "assessment":
            assessments.append(record)
            notes.append(f"Assigned {path} to assessments")
            continue
        notes.append(f"Ignored {path}")
    return notes


def _write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _artifacts_dir(output_dir: Path, label: str) -> Path:
    return output_dir / _slug(label)


def ingest_raw_materials(
    source_dir: Path,
    *,
    output_dir: Path,
    model: str,
    write_payloads: bool = True,
) -> dict[str, Any]:
    records = collect_raw_source_records(source_dir)
    weeks, assessments, unassigned = _group_records(records)

    review: dict[str, Any] = {
        "source_dir": str(source_dir),
        "model": model,
        "source_count": len(records),
        "week_sources": {},
        "assessment_sources": [],
        "unassigned_sources": [record.relative_path for record in unassigned],
        "artifacts": [],
        "warnings": [],
    }

    if unassigned:
        unassigned_payload = run_json_agent(build_unassigned_prompt(unassigned), model=model)
        if not isinstance(unassigned_payload, dict):
            raise ValueError("Unassigned-file agent output must be a JSON object.")
        assignments = [item for item in (unassigned_payload.get("assignments") or []) if isinstance(item, dict)]
        review["warnings"].extend([str(note).strip() for note in (unassigned_payload.get("notes") or []) if str(note).strip()])
        review["warnings"].extend(_apply_unassigned_assignments(weeks, assessments, unassigned, assignments))

    for week in sorted(weeks):
        week_records = sorted(weeks[week], key=lambda item: item.relative_path)
        prompt = build_week_prompt(week, week_records, model=model)
        payload = run_json_agent(prompt, model=model)
        if not isinstance(payload, dict):
            raise ValueError("Week agent output must be a JSON object.")
        normalized = normalize_week_payload(payload)
        shape = analyze_week_payload(normalized)
        syntax_errors = _validate_python_code_blocks(normalized)
        report = {
            "week": week,
            "source_files": [record.relative_path for record in week_records],
            "validation": shape,
            "syntax_errors": syntax_errors,
            "review_notes": [str(note).strip() for note in (payload.get("review_notes") or []) if str(note).strip()],
        }
        label = f"week-{week:02d}"
        bundle_dir = _artifacts_dir(output_dir, label)
        payload_path = bundle_dir / "payload.json"
        review_path = bundle_dir / "review.json"
        if write_payloads:
            _write_json(payload_path, normalized)
        _write_json(review_path, report)
        review["week_sources"][str(week)] = [record.relative_path for record in week_records]
        review["artifacts"].append(
            asdict(
                IngestionArtifact(
                source=f"week {week}",
                payload_file=str(payload_path),
                review_file=str(review_path),
                payload_type="week",
                warnings=list(shape["warnings"]) + syntax_errors,
                errors=list(shape["errors"]),
                )
            )
        )
        review["warnings"].extend(shape["warnings"])
        review["warnings"].extend(syntax_errors)

    for assessment in sorted(assessments, key=lambda item: item.relative_path):
        prompt = build_assessment_prompt(assessment, model=model)
        payload = run_json_agent(prompt, model=model)
        if not isinstance(payload, dict):
            raise ValueError("Assessment agent output must be a JSON object.")
        normalized = normalize_assessment_payload(payload)
        shape = analyze_assessment_payload(normalized)
        syntax_errors = _validate_assessment_code_blocks(normalized)
        report = {
            "source_file": assessment.relative_path,
            "validation": shape,
            "syntax_errors": syntax_errors,
            "review_notes": [str(note).strip() for note in (payload.get("notes") or []) if str(note).strip()],
        }
        label = _slug(Path(assessment.relative_path).stem)
        bundle_dir = _artifacts_dir(output_dir, f"assessment-{label}")
        payload_path = bundle_dir / "payload.json"
        review_path = bundle_dir / "review.json"
        if write_payloads:
            _write_json(payload_path, normalized)
        _write_json(review_path, report)
        review["assessment_sources"].append(assessment.relative_path)
        review["artifacts"].append(
            asdict(
                IngestionArtifact(
                source=assessment.relative_path,
                payload_file=str(payload_path),
                review_file=str(review_path),
                payload_type="assessment",
                warnings=list(shape["warnings"]) + syntax_errors,
                errors=list(shape["errors"]),
                )
            )
        )
        review["warnings"].extend(shape["warnings"])
        review["warnings"].extend(syntax_errors)

    review["summary"] = {
        "week_count": len(review["week_sources"]),
        "assessment_count": len(review["assessment_sources"]),
        "artifact_count": len(review["artifacts"]),
        "warning_count": len(review["warnings"]),
    }
    return review
