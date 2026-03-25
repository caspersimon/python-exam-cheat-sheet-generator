# Schema

> [!summary] Authoritative format
> V2 uses **SQLite + plain Markdown files**.
> Metadata and relationships live in SQLite / TSV exports.
> Piece bodies live as standalone `.md` files under `content/`.

## Core hierarchy

`topic -> subtopic -> snippet -> piece`

- **topic**: sidebar level
- **subtopic**: expandable section inside a topic
- **snippet**: grid card shown under a subtopic
- **piece**: smallest selectable unit

## Why piece bodies are files

A piece can contain:

- Markdown tables
- fenced code blocks
- inline backticks
- multi-paragraph explanations
- compact output notes

Putting those bodies in individual files avoids brittle newline/escape parsing on the frontend.

## Main exports

- `topics.tsv`
- `subtopics.tsv`
- `snippets.tsv`
- `pieces.tsv`
- `question_taxonomy.tsv`
- `question_stress_test.tsv`
- `snippet_keywords.tsv`
- `snippet_question_refs.tsv`
- `snippet_traps.tsv`
- `trap_catalog.tsv`
- `presets.tsv`
- `preset_items.tsv`
- `navigation_plan.tsv`
- `legacy_integration_map.tsv`

## Important snippet fields

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
- `question_ref_count`
- `piece_count`
- `default_piece_count`
- `default_char_count`
- `total_char_count`
- `trap_count`
- `keyword_count`
- `ui_section_slug`
- `ui_section_title`
- `ui_section_sort_order`
- `ui_card_order`

## Important piece fields

- `piece_id`
- `snippet_slug`
- `piece_slug`
- `sort_order`
- `title`
- `kind`
- `role`
- `default_selected`
- `body_path`
- `char_count`

## Recurrence levels

- `signature`
- `very-common`
- `common`
- `occasional`
- `rare`

## UI grouping helpers

Current UI section values:

- `start-here`
- `add-next`
- `edge-cases`

Render order recommendation:

1. group by `ui_section_title`
2. order groups by `ui_section_sort_order`
3. order cards by `ui_card_order`
