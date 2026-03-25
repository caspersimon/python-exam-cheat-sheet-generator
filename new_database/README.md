# Python exam snippet bank — V2

> [!summary] What changed in V2
> V2 keeps the **final exam-focused dataset** as the base and adds the strongest missing material from the older dataset **in the same scheme**: new snippets for syntax fragments, aliasing/copies, numeric corner cases, loop control/iterators, pandas missing-value alignment, and OOP inheritance, plus several targeted add-on pieces in existing snippets.

## At a glance

- topics: **8**
- subtopics: **23**
- snippets: **51**
- pieces: **163**
- presets: **5**
- question bank coverage checked against: **168** questions
- trap slugs: **103**

## Package layout

```text
python_exam_snippet_bank_v2/
├── README.md
├── db/
│   └── snippet_bank.sqlite
├── content/
│   └── <topic>/<subtopic>/<snippet-slug>/
│       ├── README.md
│       ├── 01_<piece-slug>.md
│       └── ...
├── exports/
│   ├── topics.tsv
│   ├── subtopics.tsv
│   ├── snippets.tsv
│   ├── pieces.tsv
│   ├── question_taxonomy.tsv
│   ├── question_stress_test.tsv
│   ├── presets.tsv
│   ├── preset_items.tsv
│   ├── navigation_plan.tsv
│   └── ...
└── docs/
    ├── SNIPPETS_CATALOG.md
    ├── PRESETS.md
    ├── NAVIGATION_PLAN.md
    ├── STRESS_TEST_REPORT.md
    ├── LEGACY_INTEGRATION.md
    ├── CHANGELOG.md
    ├── SCHEMA.md
    └── HANDOFF.md
```

## Recommended entry points

- start with `docs/PRESETS.md` if you want the quickest overview
- open `docs/LEGACY_INTEGRATION.md` to see what the V2 pass imported from the old dataset
- open `docs/SNIPPETS_CATALOG.md` for the full human-readable bank
- use `db/snippet_bank.sqlite` or the TSV exports for implementation work

## Notes

> [!tip] Stress-test status
> The original final-bank dataset already cleared the threshold for all **168** bank questions.  
> V2 adds backup/reference coverage and a few trap clarifiers, so the stress-test export is carried forward unchanged as the baseline coverage record.

> [!info] Why SQLite + Markdown
> Metadata and relationships stay normalized in SQLite/TSV, while multi-line piece bodies live as standalone Markdown files so the frontend does not have to parse giant escaped JSON strings.
