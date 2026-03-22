# Materials Layout

This folder now has two layers:

- the original canonical source paths used by the data pipeline and live dataset
- a non-breaking organized index under `materials/by_week/`

## Canonical Source Paths

The canonical files stay where they were so existing references in `data/study_db.json`, `topic_cards.json`, scripts, and tests do not break.

Examples:

- `materials/lectures/`
- `materials/notebooks/`
- `materials/post_midterm/`
- `materials/exams/`

## Organized Week View

Use `materials/by_week/` when you want a cleaner human-facing overview of the official course files.

- `week-01` through `week-06` group lecture, notebook, exercise, solution, and helper files by week
- `shared-assessments/` groups official exams and cross-week assessment material that does not belong to a single week

These entries are symlinks that point back to the canonical originals.

## Notes

- Week 4-6 lecture decks also exist under `materials/lectures/`, but the organized view points to the `materials/post_midterm/` copies because those are the paths used by the live dataset.
- `OOP.py` is grouped under `week-06` because the repo already classifies it as week 6 material.
- External comparison PDFs stay in `materials/example_cheat_sheets/` and are not part of the official week index.
