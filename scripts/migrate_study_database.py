#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data" / "study_db.json"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.shared import build_study_db_from_monolith, write_study_db


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Migrate the old monolithic study_data.json into the canonical study_db format."
    )
    parser.add_argument("--input", type=Path, required=True, help="Monolithic study_data.json path.")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Structured study_db.json path.")
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file if it already exists.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.input.exists():
        raise FileNotFoundError(f"Monolithic input file not found: {args.input}")
    if args.output.exists() and not args.force:
        raise FileExistsError(f"Output already exists: {args.output}. Use --force to overwrite.")

    monolith = json.loads(args.input.read_text(encoding="utf-8"))
    structured = build_study_db_from_monolith(monolith)
    write_study_db(structured, args.output)

    weeks = structured.get("weeks", [])
    exams = structured.get("assessments", {}).get("exams", [])
    print(
        f"Migrated {args.input} -> {args.output} | weeks={len(weeks)} exams={len(exams)} "
        f"schema={structured.get('meta', {}).get('schema_version', 'unknown')}"
    )


if __name__ == "__main__":
    main()
