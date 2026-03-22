#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import SMART_GEMINI_AGENT
from pipelines.study_database.raw_ingestion import ingest_raw_materials


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Agent-driven raw-material ingestion for post-midterm course files.")
    parser.add_argument("--source-dir", type=Path, required=True, help="Folder containing raw source materials.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory where canonical payloads and review artifacts should be written.",
    )
    parser.add_argument(
        "--report-file",
        type=Path,
        default=None,
        help="Optional explicit path for the combined ingestion report JSON.",
    )
    parser.add_argument(
        "--model",
        default=SMART_GEMINI_AGENT,
        help=f"Gemini model for raw ingestion (default: {SMART_GEMINI_AGENT}).",
    )
    parser.add_argument(
        "--no-payload-write",
        action="store_true",
        help="Write only review artifacts and the combined report, not the payload JSON files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {args.source_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    report = ingest_raw_materials(
        args.source_dir,
        output_dir=args.output_dir,
        model=args.model,
        write_payloads=not args.no_payload_write,
    )

    report_path = args.report_file or (args.output_dir / "raw_ingestion_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(
        "Raw ingestion complete: "
        f"weeks={report['summary']['week_count']}, "
        f"assessments={report['summary']['assessment_count']}, "
        f"artifacts={report['summary']['artifact_count']}"
    )


if __name__ == "__main__":
    main()
