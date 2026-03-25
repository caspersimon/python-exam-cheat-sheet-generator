# Schema and file layout

> [!summary] Authoritative format
> The release uses **SQLite for metadata/relations** and **plain Markdown files for content bodies**.

This solves two practical problems at once:

1. metadata stays queryable and normalized
2. code-heavy multi-line content does **not** get trapped inside escaped JSON strings

## 1. Directory layout

```text
python_exam_snippet_bank_final/
├── README.md
├── db/
│   └── snippet_bank.sqlite
├── content/
│   └── <topic>/<subtopic>/<snippet-slug>/
│       ├── README.md
│       ├── 01_<piece-slug>.md
│       ├── 02_<piece-slug>.md
│       └── ...
├── exports/
│   ├── topics.tsv
│   ├── subtopics.tsv
│   ├── snippets.tsv
│   ├── pieces.tsv
│   ├── question_taxonomy.tsv
│   ├── question_secondary_snippets.tsv
│   ├── snippet_keywords.tsv
│   ├── snippet_question_refs.tsv
│   ├── snippet_traps.tsv
│   ├── trap_catalog.tsv
│   ├── question_stress_test.tsv
│   ├── presets.tsv
│   ├── preset_items.tsv
│   ├── navigation_plan.tsv
│   └── ...
├── docs/
│   ├── WORKSPACE_NOTES.md
│   ├── QUESTION_TAXONOMY.md
│   ├── EXAM_COOKBOOK.md
│   ├── SNIPPETS_CATALOG.md
│   ├── STRESS_TEST_REPORT.md
│   ├── PRESETS.md
│   ├── NAVIGATION_PLAN.md
│   ├── CHANGELOG.md
│   ├── SCHEMA.md
│   └── HANDOFF.md
└── notes/
    ├── question_digest.md
    └── SOURCE_BANK_NOTES.md
```

## 2. Content model

### Topic → subtopic → snippet → piece

This matches the website model closely:

- **topic**: sidebar level
- **subtopic**: openable subsection inside a topic
- **snippet**: grid card shown inside a subtopic
- **piece**: smallest selectable unit

### Why piece bodies are files

A piece body can contain:

- markdown tables
- fenced code blocks
- inline backticks
- multiple paragraphs
- compact comments inside code

Keeping piece bodies in standalone `.md` files means the frontend can:

- fetch/render them directly
- precompile them
- diff them cleanly
- avoid the newline / escape-character issues that happen with giant JSON fields

## 3. Main SQLite tables

### `topics`
One row per top-level topic.

Key fields:

- `topic_slug`
- `title`
- `sort_order`
- `description`
- `snippet_count`

### `subtopics`
One row per subtopic.

Key fields:

- `subtopic_slug`
- `topic_slug`
- `title`
- `sort_order`
- `description`
- `snippet_count`

### `snippets`
One row per snippet card.

Key fields:

- `snippet_slug`
- `topic_slug`
- `subtopic_slug`
- `title`
- `summary`
- `why`
- `default_priority`
- `difficulty`
- `course_phase`
- `recurrence_level`
- `exam_family_count`
- `question_ref_count`
- `piece_count`
- `default_piece_count`
- `default_char_count`
- `total_char_count`
- `trap_count`
- `keyword_count`
- `is_trap_heavy`
- `ui_section_slug`
- `ui_section_title`
- `ui_section_sort_order`
- `ui_card_order`
- `readme_path`
- `content_dir`

### `pieces`
One row per piece.

Key fields:

- `piece_id`
- `snippet_slug`
- `piece_slug`
- `sort_order`
- `title`
- `kind` (`table`, `rules`, `example`, `template`, `checklist`)
- `role` (`core`, `trap`, `clarifier`)
- `default_selected` (`0` / `1`)
- `body_path`
- `char_count`
- `question_ref_count`

### `question_taxonomy`
Question-level manual coding.

Key fields:

- `question_id`
- `exam_id`
- `exam_title`
- `exam_family`
- `question_number`
- `raw_topic`
- `first_line`
- `main_topic`
- `subtopic`
- `course_phase`
- `question_form`
- `question_form_title`
- `primary_snippet_slug`
- `primary_snippet_title`
- `secondary_snippet_slugs`
- `secondary_snippet_titles`

### Relation tables

- `snippet_keywords`
- `snippet_question_refs`
- `snippet_traps`
- `question_secondary_snippets`
- `piece_question_refs` (currently sparse by design)
- `piece_traps` (currently sparse by design)

### Source-analysis tables

- `trap_catalog`
- `exam_families`
- `exams`
- `source_notes`

### Finalization tables

- `question_stress_test`
- `presets`
- `preset_items`

## 4. Important metadata conventions

### `default_priority`

A rough 3–5 priority scale for future presets.

- `5` = strong candidate for a default starter pack
- `4` = valuable but a bit more situational
- `3` = useful, but less universal or more niche

### `default_selected`

Piece-level default.

- `1` = should probably be selected in a balanced default pack
- `0` = optional clarifier / expansion piece

### `ui_section_*`

These fields are frontend helpers for grouping snippet cards inside a subtopic.

Current sections:

- `start-here`
- `add-next`
- `edge-cases`

Recommended rendering behavior:

1. group by `ui_section_title`
2. order groups by `ui_section_sort_order`
3. order cards inside a group by `ui_card_order`

### `recurrence_level`

Current levels:

- `signature`
- `very-common`
- `common`
- `occasional`
- `rare`

### `question_refs`

Question references are strongest at the **snippet** level.
Many pieces are synthesized from several past questions rather than copied from one option from one exam.

That is intentional.

## 5. Preset model

### `presets`
One row per preset pack.

Key fields:

- `preset_id`
- `title`
- `summary`
- `target_user`
- `notes`
- `sort_order`
- `snippet_count`
- `piece_count`
- `char_count`

### `preset_items`
One row per included piece in a preset.

Key fields:

- `preset_id`
- `rank`
- `snippet_slug`
- `piece_id`

## 6. Stress-test model

### `question_stress_test`
One row per exam question.

Key fields:

- `question_id`
- `exam_id`
- `exam_title`
- `question_number`
- `cross_off_score`
- `select_score`
- `change_action`
- `change_notes`
- `primary_snippet_slug`
- `primary_snippet_title`

Scoring semantics:

- `cross_off_score`: how many wrong answers the snippets let you confidently eliminate (`0`–`3`)
- `select_score`: how confidently the snippets let you identify the correct answer (`0`–`3`)

## 7. Suggested import strategy for a frontend

### Minimal strategy

1. query `topics` and `subtopics` for navigation
2. query `snippets` for card metadata
3. group snippet cards by `ui_section_title`
4. query `pieces` for the selected snippet
5. read the markdown file pointed to by `body_path`
6. render markdown with code fences + tables enabled

### Better strategy

Precompile a lightweight frontend bundle that:

- inlines the markdown bodies during build
- keeps SQLite/TSV as the editable source of truth
- derives search indexes from `title`, `summary`, `keywords`, and trap labels
- materializes presets from `preset_items`
