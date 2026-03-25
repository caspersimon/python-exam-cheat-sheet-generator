# Python exam snippet bank — final package

> [!summary] What this package contains
> This is the **final post-review package**.
> Steps **8** and **9** are complete:
> - the snippet bank was revised after human feedback
> - every question in the source bank was stress-tested against the snippets
> - presets and navigation curation were added
> - the release now includes the promised `content/` markdown files, not just metadata

## At a glance

- **Topics:** 8
- **Subtopics:** 20
- **Snippets:** 45
- **Pieces:** 137
- **Trap slugs:** 75
- **Questions stress-tested:** 168
- **Preset packs:** 4
- **Exams in source bank:** 7
- **Deduped exam families used for pattern analysis:** 5

## What changed after review

> [!info] Review-to-final changes
> The final pass incorporated the review feedback and then propagated the same style improvements through the rest of the bank.

- removed the dedicated meta-options snippet because it was more about reading than Python
- rewrote several method-heavy pieces to use realistic call syntax and concrete outputs
- split the scope/name-error example into its own piece
- added clarity pieces for OOP average ratings, numbered-report dictionaries, and list-of-dicts printing
- polished later snippets to better match the same style: more context, more output-first examples, less code-writing advice

## Stress-test result

> [!success] Coverage threshold passed
> Every one of the **168** questions now clears the required step-8 threshold.
>
> - `cross_off_score = 3` for **168 / 168** questions
> - `select_score >= 2` for **168 / 168** questions
> - `select_score = 3` for **163 / 168** questions
> - questions that triggered snippet edits during the stress test: **3**
> - questions still failing the threshold: **0**

## Why the dataset is shaped this way

> [!info] Design choice
> The authoritative release format is **SQLite + plain Markdown files**.
>
> - SQLite stores structured metadata and relations between topics, subtopics, snippets, pieces, traps, past questions, presets, and stress-test results.
> - The actual snippet/piece bodies live as plain `.md` files in `content/`.
> - TSV exports mirror the key tables for easy inspection and non-SQL workflows.
>
> This avoids the giant-JSON-with-escaped-newlines problem while staying portable.

## Folder guide

- `db/snippet_bank.sqlite` — authoritative structured dataset
- `content/` — one folder per snippet, with raw markdown piece files
- `exports/` — TSV mirrors of the main tables
- `docs/EXAM_COOKBOOK.md` — exam-maker manual
- `docs/QUESTION_TAXONOMY.md` — topic + question-form analysis
- `docs/SNIPPETS_CATALOG.md` — human-readable full catalog of snippets and pieces
- `docs/STRESS_TEST_REPORT.md` — question-by-question coverage report summary
- `docs/PRESETS.md` — ready-made starter packs
- `docs/NAVIGATION_PLAN.md` — recommended topic/subtopic/snippet grouping for the frontend
- `docs/HANDOFF.md` — final notes for the future frontend agent
- `docs/SCHEMA.md` — data model and file layout
- `docs/WORKSPACE_NOTES.md` — process notes and what changed between review and final
- `docs/CHANGELOG.md` — concise change summary
- `notes/question_digest.md` — full question digest used during manual inspection

## Presets included

|   # | Preset              | Slug                |   Snippets |   Pieces |   Char count | Best for                                                               |
|----:|:--------------------|:--------------------|-----------:|---------:|-------------:|:-----------------------------------------------------------------------|
|   1 | Balanced default    | balanced-default    |         40 |       90 |        21342 | minimal prior knowledge, wants broad coverage                          |
|   2 | Post-midterm tilted | post-midterm-tilted |         31 |       73 |        17737 | expects the final to skew toward later-course material                 |
|   3 | Ultra-dense core    | ultra-dense-core    |         21 |       43 |        10354 | very limited space, wants maximum points per line                      |
|   4 | Trap hunter         | trap-hunter         |         20 |       46 |        11504 | knows the material somewhat, mainly loses points to subtle distractors |

## Recommended read order

1. `docs/HANDOFF.md`
2. `docs/PRESETS.md`
3. `docs/NAVIGATION_PLAN.md`
4. `docs/STRESS_TEST_REPORT.md`
5. `docs/SNIPPETS_CATALOG.md`

## Default recommendation

> [!tip] Start-here preset
> For a student with very little prior knowledge, start from **Balanced default**.
> It is the broadest preset and intentionally over-includes.
> The point is to start with safe coverage, then remove what the student already knows by heart.
