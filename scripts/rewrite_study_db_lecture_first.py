#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "study_db.json"
DEFAULT_REPORT = ROOT / "data" / "curation_reports" / "lecture_first_migration_report.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import write_study_db
from pipelines.study_database import migrate_study_db_to_v3


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Rewrite study_db.json into the lecture-first schema v3.")
    parser.add_argument("--input", type=Path, default=DEFAULT_DB, help="Existing study_db.json path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_DB, help="Destination path for the v3 database.")
    parser.add_argument("--report-file", type=Path, default=DEFAULT_REPORT, help="Migration report JSON path.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    db = json.loads(args.input.read_text(encoding="utf-8"))
    migrated, report = migrate_study_db_to_v3(db)
    write_study_db(migrated, args.output)
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Rewrote {args.input} -> {args.output} | weeks={report['summary']['weeks']} "
        f"unassigned={report['summary']['unassigned_snippets']} merges={report['summary']['merged_snippet_decisions']}"
    )


if __name__ == "__main__":
    main()
