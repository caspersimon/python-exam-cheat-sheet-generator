from __future__ import annotations

from pipelines.shared import STUDY_DB_FILE, load_study_db

from .lecture_first import OUTPUT_FILE, build_output, write_output


def main() -> None:
    db = load_study_db()
    output = build_output(db, STUDY_DB_FILE)
    write_output(output)
    print(f"Wrote {OUTPUT_FILE} with {output['meta']['total_cards']} cards")
