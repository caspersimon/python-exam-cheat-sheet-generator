#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import (
    SMART_GEMINI_AGENT,
    STUDY_DB_FILE,
    flatten_study_db_for_pipeline,
    load_study_db,
    recompute_topic_analysis,
    write_study_db,
)
from pipelines.study_database import (
    WeekCurationError,
    analyze_week_payload,
    curate_week_payload,
    missing_source_paths,
    normalize_week_payload,
)

DEFAULT_REPORT_DIR = ROOT / "data" / "curation_reports"
DEFAULT_MODEL = SMART_GEMINI_AGENT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Add one week of material into the canonical study database with AI-first curation."
    )
    parser.add_argument(
        "--week-file",
        type=Path,
        required=True,
        help="Path to a week payload JSON file (see data/templates/week_template.json).",
    )
    parser.add_argument(
        "--skip-ai-curation",
        action="store_true",
        help="Bypass Gemini curation and integrate normalized input directly.",
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Gemini model for curation (default: {DEFAULT_MODEL}).",
    )
    parser.add_argument(
        "--replace-existing",
        action="store_true",
        help="Replace existing material if the same week already exists.",
    )
    parser.add_argument(
        "--no-recompute-topic-analysis",
        action="store_true",
        help="Keep existing topic_analysis unchanged.",
    )
    parser.add_argument(
        "--report-file",
        type=Path,
        default=None,
        help="Optional explicit path for curation report JSON.",
    )
    parser.add_argument(
        "--allow-missing-sources",
        action="store_true",
        help="Allow integration even if one or more source paths listed in the payload do not exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run curation+integration checks but do not write the canonical database.",
    )
    return parser.parse_args()


def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _report_path(week: int, explicit: Path | None, *, dry_run: bool) -> Path:
    if explicit is not None:
        explicit.parent.mkdir(parents=True, exist_ok=True)
        return explicit
    DEFAULT_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    suffix = "_dry_run" if dry_run else ""
    return DEFAULT_REPORT_DIR / f"week_{week:02d}_curation_report{suffix}.json"


def _upsert_week(db: dict[str, Any], week_payload: dict[str, Any], *, replace_existing: bool) -> str:
    weeks = [item for item in _safe_list(db.get("weeks")) if isinstance(item, dict)]
    db["weeks"] = weeks

    week = int(week_payload["week"])
    for index, existing in enumerate(weeks):
        if int(existing.get("week") or 0) != week:
            continue
        if not replace_existing:
            raise WeekCurationError(
                f"Week {week} already exists. Re-run with --replace-existing to overwrite this week."
            )
        weeks[index] = week_payload
        weeks.sort(key=lambda item: int(item.get("week") or 9999))
        return "replaced"

    weeks.append(week_payload)
    weeks.sort(key=lambda item: int(item.get("week") or 9999))
    return "added"


def _update_meta(db: dict[str, Any]) -> None:
    meta = db.setdefault("meta", {})
    meta.setdefault("schema_version", "2.0")
    meta["last_updated"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"

    weeks_covered = sorted(
        {
            int(item.get("week"))
            for item in _safe_list(db.get("weeks"))
            if isinstance(item, dict) and str(item.get("week", "")).isdigit()
        }
    )
    meta["weeks_covered"] = weeks_covered

    sources = [source for source in _safe_list(meta.get("sources")) if isinstance(source, str)]
    for week in _safe_list(db.get("weeks")):
        if not isinstance(week, dict):
            continue
        for source in _safe_list(week.get("sources")):
            if isinstance(source, str) and source not in sources:
                sources.append(source)

    for exam in _safe_list(db.get("assessments", {}).get("exams")):
        if not isinstance(exam, dict):
            continue
        source = exam.get("source")
        if isinstance(source, str) and source not in sources:
            sources.append(source)

    meta["sources"] = sources


def _load_week_payload(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Week input file not found: {path}")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise WeekCurationError("Week input must contain a JSON object.")
    return payload


def _print_issues(issues: dict[str, list[str]]) -> None:
    for warning in issues.get("warnings", []):
        print(f"Warning: {warning}")


def _clone_db(db: dict[str, Any]) -> dict[str, Any]:
    return json.loads(json.dumps(db))


def main() -> None:
    args = parse_args()
    try:
        db = load_study_db()
    except FileNotFoundError as exc:
        raise FileNotFoundError(
            f"{exc}\nInitialize it first with: "
            "python3 scripts/migrate_study_database.py --input <old-study-data.json> --output data/study_db.json"
        ) from exc
    raw_week_payload = _load_week_payload(args.week_file)
    preflight = analyze_week_payload(raw_week_payload)
    if preflight["errors"]:
        issues = "\n- ".join(preflight["errors"])
        raise WeekCurationError(f"Week payload preflight failed:\n- {issues}")
    _print_issues(preflight)

    missing_sources = missing_source_paths(raw_week_payload, root_dir=ROOT)
    if missing_sources and not args.allow_missing_sources:
        paths = "\n- ".join(missing_sources)
        raise WeekCurationError(
            "Some payload `sources` files do not exist. Fix these paths or re-run with --allow-missing-sources:\n"
            f"- {paths}"
        )
    if missing_sources:
        print(f"Warning: continuing with {len(missing_sources)} missing source path(s).")

    if args.skip_ai_curation:
        curated_week = normalize_week_payload(raw_week_payload)
        curation_report = {
            "week": curated_week["week"],
            "generator": "none",
            "model": None,
            "note": "AI curation skipped by user flag.",
            "lecture": {
                "input_concepts": len(curated_week["lecture"]["concepts"]),
                "curated_concepts": len(curated_week["lecture"]["concepts"]),
                "input_lecture_questions": len(curated_week["lecture"]["lecture_questions"]),
                "curated_lecture_questions": len(curated_week["lecture"]["lecture_questions"]),
                "quality_notes": [],
            },
            "notebooks": {
                "total_cells": len(curated_week["notebook_cells"]),
                "kept_cells": len(curated_week["notebook_cells"]),
                "dropped_cells": 0,
                "invalid_code_cells": [],
            },
        }
    else:
        curated_week, curation_report = curate_week_payload(raw_week_payload, model=args.model)

    post_curation = analyze_week_payload(curated_week)
    if post_curation["errors"]:
        issues = "\n- ".join(post_curation["errors"])
        raise WeekCurationError(f"Curated week payload failed validation:\n- {issues}")
    _print_issues(post_curation)

    updated_db = _clone_db(db)
    integration_action = _upsert_week(updated_db, curated_week, replace_existing=args.replace_existing)
    _update_meta(updated_db)
    if not args.no_recompute_topic_analysis:
        knowledge = updated_db.setdefault("knowledge", {})
        knowledge["topic_analysis"] = recompute_topic_analysis(flatten_study_db_for_pipeline(updated_db))

    if not args.dry_run:
        write_study_db(updated_db)

    report_path = _report_path(int(curated_week["week"]), args.report_file, dry_run=args.dry_run)
    report_payload = {
        "timestamp_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "dry_run": bool(args.dry_run),
        "integration_action": integration_action,
        "week_file": str(args.week_file),
        "curation": curation_report,
        "validation": {
            "preflight_warnings": preflight["warnings"],
            "post_curation_warnings": post_curation["warnings"],
            "missing_sources": missing_sources,
        },
        "recomputed_topic_analysis": not args.no_recompute_topic_analysis,
        "manual_review_required": True,
        "review_checklist": [
            "Confirm curated lecture concepts are exam-relevant and not over-generalized.",
            "Spot-check curated notebook cells, especially any rewritten code snippets.",
            "Resolve any invalid_code_cells listed in the report before regenerating topic cards.",
        ],
    }
    report_path.write_text(json.dumps(report_payload, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        f"Week {curated_week['week']} {integration_action}. "
        f"curated_concepts={len(curated_week['lecture']['concepts'])}, "
        f"curated_questions={len(curated_week['lecture']['lecture_questions'])}, "
        f"curated_notebook_cells={len(curated_week['notebook_cells'])}"
    )
    if args.dry_run:
        print("Dry run only: canonical database was not modified.")
    else:
        print(f"Wrote canonical database: {STUDY_DB_FILE}")
    print(f"Wrote curation report: {report_path}")


if __name__ == "__main__":
    main()
