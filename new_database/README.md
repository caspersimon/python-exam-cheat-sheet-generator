# Python exam snippet bank — review package

> [!summary] What this package contains
> This release is the **step 7 review package**: the manual close-reading, taxonomy, exam cookbook, and snippet dataset are done; the stress-test pass against every question (**step 8**) is intentionally **not** done yet because the workflow has a human review gate here.

## At a glance

- **Topics:** 8
- **Subtopics:** 20
- **Snippets:** 46
- **Pieces:** 134
- **Trap slugs:** 75
- **Questions mapped:** 168
- **Exams in source bank:** 7
- **Deduped exam families used for pattern analysis:** 5

## Why the dataset is shaped this way

> [!info] Design choice
> The authoritative release format is **SQLite + plain Markdown files**.
>
> - SQLite stores structured metadata, relations, and queryable links between snippets, pieces, traps, topics, and past questions.
> - The actual snippet/piece bodies live as plain `.md` files in `content/`.
> - This avoids the “giant JSON blob with escaped newlines and code fences” problem while staying portable.

## Folder guide

- `db/snippet_bank.sqlite` — authoritative structured dataset
- `content/` — one folder per snippet, with raw markdown piece files
- `exports/` — TSV exports for quick inspection / non-SQL workflows
- `docs/EXAM_COOKBOOK.md` — exam-maker manual
- `docs/QUESTION_TAXONOMY.md` — topic + question-form analysis
- `docs/SNIPPETS_CATALOG.md` — human-readable full catalog of snippets and pieces
- `docs/WORKSPACE_NOTES.md` — process notes and step checklist
- `docs/SCHEMA.md` — data model and file layout
- `docs/HANDOFF.md` — notes for the future frontend agent
- `notes/question_digest.md` — full question digest used during manual inspection

## Recommended read order

1. `docs/WORKSPACE_NOTES.md`
2. `docs/QUESTION_TAXONOMY.md`
3. `docs/EXAM_COOKBOOK.md`
4. `docs/SNIPPETS_CATALOG.md`
5. `docs/HANDOFF.md`

## Not done yet

> [!warning] Review gate
> This package stops at the mandatory human review checkpoint.
>
> That means:
> - no final preset packs yet
> - no full question-by-question stress-test scoring yet
> - no final navigation curation pass yet

Those are best done **after** your feedback on this package.
