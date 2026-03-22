#!/usr/bin/env python3

from __future__ import annotations

import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import flatten_study_db_for_pipeline, load_study_db, recompute_topic_analysis, write_study_db
from pipelines.study_database import analyze_assessment_payload, analyze_week_payload


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Import extracted week and assessment payloads into study_db.json.")
    parser.add_argument(
        "--payload-dir",
        type=Path,
        required=True,
        help="Directory produced by scripts/ingest_raw_materials.py containing */payload.json files.",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Replace existing weeks/exams when matching by week number or source path.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and summarize imports without writing data/study_db.json.",
    )
    return parser.parse_args()


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _normalize_repo_relative_path(raw_path: Any) -> str:
    path_text = str(raw_path or "").strip()
    if not path_text:
        return ""

    candidate = ROOT / path_text
    if candidate.exists():
        return path_text

    if not path_text.startswith("materials/"):
        prefixed = Path("materials/post_midterm") / path_text
        if (ROOT / prefixed).exists():
            return prefixed.as_posix()

    return path_text


def _normalize_import_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = deepcopy(payload)

    if isinstance(normalized, dict) and "lecture" in normalized and "notebook_cells" in normalized:
        normalized["sources"] = [
            path for path in (_normalize_repo_relative_path(source) for source in _safe_list(normalized.get("sources"))) if path
        ]
        return normalized

    if isinstance(normalized, dict) and "questions" in normalized and "exam_label" in normalized:
        normalized["source"] = _normalize_repo_relative_path(normalized.get("source"))
        if "notes" not in normalized and str(normalized.get("note") or "").strip():
            normalized["notes"] = [str(normalized["note"]).strip()]
        elif "notes" in normalized:
            normalized["notes"] = [str(note).strip() for note in _safe_list(normalized.get("notes")) if str(note).strip()]
        normalized["ignored"] = bool(normalized.get("ignored"))
        return normalized

    return normalized


def _load_payloads(payload_dir: Path) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    week_payloads: list[dict[str, Any]] = []
    assessment_payloads: list[dict[str, Any]] = []

    candidate_paths = sorted(payload_dir.glob("*/payload.json")) + sorted(payload_dir.glob("*.json"))
    for payload_path in candidate_paths:
        payload = _normalize_import_payload(json.loads(payload_path.read_text(encoding="utf-8")))
        if isinstance(payload, dict) and "lecture" in payload and "notebook_cells" in payload:
            week_payloads.append(payload)
            continue
        if isinstance(payload, dict) and "questions" in payload and "exam_label" in payload:
            assessment_payloads.append(payload)
    return week_payloads, assessment_payloads


def _upsert_week(db: dict[str, Any], payload: dict[str, Any], *, replace_existing: bool) -> str:
    weeks = [item for item in _safe_list(db.get("weeks")) if isinstance(item, dict)]
    db["weeks"] = weeks
    week_value = int(payload["week"])

    for index, existing in enumerate(weeks):
        if int(existing.get("week") or 0) != week_value:
            continue
        if not replace_existing:
            raise RuntimeError(f"Week {week_value} already exists. Re-run with --replace-existing to overwrite it.")
        weeks[index] = payload
        weeks.sort(key=lambda item: int(item.get("week") or 9999))
        return "replaced"

    weeks.append(payload)
    weeks.sort(key=lambda item: int(item.get("week") or 9999))
    return "added"


def _upsert_assessment(db: dict[str, Any], payload: dict[str, Any], *, replace_existing: bool) -> str:
    assessments = db.setdefault("assessments", {})
    exams = [item for item in _safe_list(assessments.get("exams")) if isinstance(item, dict)]
    assessments["exams"] = exams
    source = str(payload.get("source") or "").strip()
    label = str(payload.get("exam_label") or "").strip()

    for index, existing in enumerate(exams):
        same_source = source and str(existing.get("source") or "").strip() == source
        same_label = label and str(existing.get("exam_label") or "").strip() == label
        if not (same_source or same_label):
            continue
        if not replace_existing:
            raise RuntimeError(f"Assessment already exists for source={source!r} label={label!r}.")
        exams[index] = payload
        return "replaced"

    exams.append(payload)
    return "added"


def _refresh_meta(db: dict[str, Any]) -> None:
    meta = db.setdefault("meta", {})
    weeks = [item for item in _safe_list(db.get("weeks")) if isinstance(item, dict)]
    meta["weeks_covered"] = sorted(int(item.get("week")) for item in weeks if str(item.get("week", "")).isdigit())

    sources: list[str] = []
    for week in weeks:
        for source in _safe_list(week.get("sources")):
            if isinstance(source, str) and source not in sources:
                sources.append(source)

    assessments = db.get("assessments", {})
    for exam in _safe_list(assessments.get("exams")):
        if not isinstance(exam, dict):
            continue
        source = exam.get("source")
        if isinstance(source, str) and source not in sources:
            sources.append(source)

    meta["sources"] = sources


def main() -> None:
    args = parse_args()
    if not args.payload_dir.exists():
        raise FileNotFoundError(f"Payload directory not found: {args.payload_dir}")

    week_payloads, assessment_payloads = _load_payloads(args.payload_dir)
    if not week_payloads and not assessment_payloads:
        raise RuntimeError(f"No importable payload.json files found under {args.payload_dir}")

    db = load_study_db()
    summary = {"weeks": [], "assessments": []}

    for payload in week_payloads:
        issues = analyze_week_payload(payload)
        if issues["errors"]:
            raise RuntimeError(f"Week {payload.get('week')} failed validation: {issues['errors']}")
        action = _upsert_week(db, payload, replace_existing=args.replace_existing)
        summary["weeks"].append({"week": payload["week"], "action": action, "warnings": issues["warnings"]})

    for payload in assessment_payloads:
        if payload.get("ignored"):
            summary["assessments"].append(
                {
                    "exam_label": payload["exam_label"],
                    "action": "skipped",
                    "warnings": ["ignored assessment payload"],
                }
            )
            continue
        issues = analyze_assessment_payload(payload)
        if issues["errors"]:
            raise RuntimeError(f"Assessment {payload.get('exam_label')} failed validation: {issues['errors']}")
        action = _upsert_assessment(db, payload, replace_existing=args.replace_existing)
        summary["assessments"].append(
            {"exam_label": payload["exam_label"], "action": action, "warnings": issues["warnings"]}
        )

    _refresh_meta(db)
    materialized = flatten_study_db_for_pipeline(db)
    db.setdefault("knowledge", {})["topic_analysis"] = recompute_topic_analysis(materialized)

    if args.dry_run:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
        return

    write_study_db(db)
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
