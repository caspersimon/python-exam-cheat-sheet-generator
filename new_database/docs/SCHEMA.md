# Schema and file layout

> [!summary] Authoritative format
> The release uses **SQLite for metadata/relations** and **plain Markdown files for content bodies**.

This solves two practical problems at once:

1. metadata stays queryable and normalized
2. code-heavy multi-line content does **not** get trapped inside escaped JSON strings

## 1. Directory layout

```text
release/
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
│   ├── trap_catalog.tsv
│   └── ...
├── docs/
│   ├── WORKSPACE_NOTES.md
│   ├── QUESTION_TAXONOMY.md
│   ├── EXAM_COOKBOOK.md
│   ├── SNIPPETS_CATALOG.md
│   ├── SCHEMA.md
│   └── HANDOFF.md
└── notes/
    └── question_digest.md
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
- avoid the newline / escape-character issues that happen with a giant JSON field

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
- `exam_family`
- `question_number`
- `raw_topic`
- `first_line`
- `main_topic`
- `subtopic`
- `course_phase`
- `question_form`
- `primary_snippet_slug`
- `secondary_snippet_slugs`

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

### `recurrence_level`

Derived from question-ref count and family coverage.

Current levels:

- `signature`
- `very-common`
- `common`
- `occasional`
- `rare`

### `question_refs`

Question references are strongest at the **snippet** level.
Many pieces are synthetic, polished explanations of a recurring pattern rather than a direct copy of one option from one exam.

That is intentional.

## 5. Suggested import strategy for a frontend

### Minimal strategy

1. query `topics` and `subtopics` for navigation
2. query `snippets` for card metadata
3. query `pieces` for the selected snippet
4. read the markdown file pointed to by `body_path`
5. render markdown with code fences + tables enabled

### Better strategy

Precompile a lightweight frontend bundle that:

- inlines the markdown bodies during build
- keeps SQLite/TSV as the editable source of truth
- derives search indexes from `title`, `summary`, `keywords`, and trap labels

## 6. Why not JSON?

> [!info] Explicit rationale
> A single JSON export would be possible, but it is **not** the best source of truth here.
>
> The bodies are exactly the kind of content that becomes annoying inside JSON:
> - fenced code
> - lots of backticks
> - multiline tables
> - escape-heavy diffs

SQLite + markdown avoids that without making the data proprietary.

## 7. Quick examples

### Find all snippets in Pandas / selection

```sql
SELECT snippet_slug, title
FROM snippets
WHERE topic_slug = 'pandas'
  AND subtopic_slug = 'selection'
ORDER BY sort_order;
```

### Find all question refs for one snippet

```sql
SELECT question_id
FROM snippet_question_refs
WHERE snippet_slug = 'pandas-loc-iloc'
ORDER BY question_id;
```

### Find all trap labels attached to one snippet

```sql
SELECT t.trap_slug, c.label, c.description
FROM snippet_traps t
LEFT JOIN trap_catalog c USING (trap_slug)
WHERE t.snippet_slug = 'mutation-vs-return'
ORDER BY t.trap_slug;
```
