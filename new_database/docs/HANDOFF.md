# HANDOFF.md

> [!summary] Context for the next agent
> This package is the **final content release**.
> It is post-review, post-stress-test, and ready for frontend integration.

## 1. What already exists

- a normalized dataset in `db/snippet_bank.sqlite`
- actual markdown piece bodies in `content/`
- per-snippet `README.md` files in each content folder
- TSV mirrors in `exports/`
- final presets in `presets` / `preset_items`
- question stress-test results in `question_stress_test`
- frontend-oriented snippet grouping fields:
  - `ui_section_slug`
  - `ui_section_title`
  - `ui_section_sort_order`
  - `ui_card_order`

## 2. The most important implementation rule

### Keep pieces selectable individually

The whole point of the dataset is modularity.
Do **not** collapse a snippet into one indivisible blob in the UI.

A good card flow is:

1. show snippet cards in a subtopic grid
2. group cards by `ui_section_title`
3. open a card
4. show summary + why it matters + badges
5. let the user tick individual pieces inside it

## 3. Recommended frontend data flow

### Navigation

- Sidebar uses `topics` and `subtopics`
- Subtopic page queries `snippets`
- Group snippet cards by `ui_section_title`
- Sort sections by `ui_section_sort_order`
- Sort cards inside sections by `ui_card_order`

### Card metadata worth showing

- recurrence badge (`signature`, `very-common`, etc.)
- phase badge (`pre-midterm`, `post-midterm`, `mixed`)
- optional “trap-heavy” badge from `is_trap_heavy`
- default piece count / total piece count
- estimated char count if you want a rough space-cost indicator

### Piece rendering

Do **not** treat piece bodies as plain text.
They contain:

- fenced code blocks
- markdown tables
- inline code
- short comments that matter for meaning

Use a renderer that supports tables + code fences at minimum.

## 4. Presets are already ready

There are four final presets:

|   # | Preset              | Slug                |   Snippets |   Pieces |   Char count |
|----:|:--------------------|:--------------------|-----------:|---------:|-------------:|
|   1 | Balanced default    | balanced-default    |         40 |       90 |        21342 |
|   2 | Post-midterm tilted | post-midterm-tilted |         31 |       73 |        17737 |
|   3 | Ultra-dense core    | ultra-dense-core    |         21 |       43 |        10354 |
|   4 | Trap hunter         | trap-hunter         |         20 |       46 |        11504 |

Implementation suggestion:

- load `presets`
- when a user picks one, preselect the exact `piece_id`s from `preset_items`
- still allow manual deselection afterward

## 5. Search and filtering suggestions

Search over:

- snippet `title`
- snippet `summary`
- `why`
- keywords
- trap labels

Useful filters:

- topic / subtopic
- phase
- recurrence
- trap-heavy only
- snippets with examples
- preset membership

## 6. Visual suggestion for optional arguments

Some pieces use docs-style optional-argument notation such as:

- `text.replace(old, new[, count])`
- `text.find(value[, start[, end]])`

If the renderer allows it, consider styling the square-bracketed optional parts slightly more subtly than the required arguments.
That would match the content design intent without changing the underlying markdown.

## 7. Preset recommendation logic

If you need a default entry point in the UI:

- default preset = `balanced-default`
- alternate compact preset = `ultra-dense-core`

### Suggested labels for end users

- `balanced-default` → “Start here”
- `post-midterm-tilted` → “Later-course heavy”
- `ultra-dense-core` → “Minimal space”
- `trap-hunter` → “I mainly fall for traps”

## 8. Known source-bank caveats

- the sample final contains one exact duplicate question (`q08` = `q11`)
- the resit pair should be deduped for recurrence analytics
- the sample-final / later-course trial pair should also be deduped for recurrence analytics
- piece-level question refs are intentionally sparse; snippet-level refs are the main coverage signal

## 9. Source-of-truth order

Treat these as the priority order of truth:

1. `db/snippet_bank.sqlite`
2. `content/.../*.md`
3. `exports/*.tsv`

## 10. If you need one sanity-check query

The first integration smoke test should confirm that:

- `balanced-default` exists in `presets`
- every `preset_items.piece_id` exists in `pieces`
- every `pieces.body_path` file exists
- every `snippets.readme_path` file exists

If that passes, the content bundle is structurally sound.
