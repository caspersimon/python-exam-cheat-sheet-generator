# HANDOFF.md

> [!summary] Context for the next agent
> This package is the **pre-stress-test review release**.
> The taxonomy, cookbook, and snippet bank are in place.
> The mandatory review gate happened here on purpose.
>
> You should treat this as **version 0.9**, not final production data.

## 1. What already exists

- a normalized dataset in `db/snippet_bank.sqlite`
- plain markdown piece bodies in `content/`
- TSV mirrors in `exports/`
- documentation explaining the exam patterns and the schema
- snippet metadata for:
  - topic / subtopic placement
  - question references
  - trap slugs
  - recurrence level
  - default priority
  - default-selected pieces

## 2. What does *not* exist yet

The following are intentionally deferred until after human review:

- the full step-8 stress-test matrix
- final preset packs
- final navigation curation / rebalancing
- any frontend-specific static bundle generation

## 3. Implementation advice

### Render markdown properly

Do **not** treat piece bodies as plain text.
They contain:

- fenced code blocks
- markdown tables
- inline code
- compact comments that matter for meaning

The renderer must support tables and code fences at minimum.

### Keep pieces selectable individually

The whole point of the dataset is modularity.
Do not collapse a snippet into one indivisible blob in the UI.

A good card flow is:

1. snippet card in the grid
2. expand/open card
3. show summary + why it matters + trap badges
4. let the user tick individual pieces inside it

### Use metadata, not just text search

Good filters/searches should use:

- `title`
- `summary`
- `keywords`
- `trap_slugs`
- `course_phase`
- `recurrence_level`
- `default_priority`

### Respect the `default_selected` field

This is the most useful first-pass signal for building a later “balanced starter cheat sheet.”
Some pieces are intentionally extra clarifiers and should start deselected.

## 4. Suggested frontend affordances

### Card badges worth adding

- **Signature / very common / common** recurrence badge
- **Pre-midterm / post-midterm / mixed**
- **Trap-heavy**
- **Optional clarifier available**

### Useful sort options

- default priority
- recurrence
- topic/subtopic
- piece count
- question coverage count

### Useful filters

- only show post-midterm
- only show signature/common snippets
- only show pandas/datetime/OOP
- only show snippets with trap badges
- only show snippets with code examples

## 5. Preset ideas for the next pass

Not implemented yet, but the metadata already supports them.

### Likely preset families

- **Balanced beginner preset** — high `default_priority`, broad topic spread
- **Post-midterm heavy preset** — pandas, datetime, OOP, strings, but still some pre-midterm essentials
- **Trap-hunter preset** — snippets with the most recurring trap coverage
- **Pandas rescue preset** / **functions & scope rescue preset** / etc.

Use:

- `default_priority`
- `exam_family_count`
- `question_ref_count`
- `default_selected`
- `course_phase`

## 6. Known source-bank caveats

- the sample final contains one exact duplicate question (`q08` = `q11`)
- the resit pair should be deduped for analytics
- the sample-final / later-course trial pair should also be deduped when measuring recurrence
- piece-level question refs are intentionally sparse; snippet-level refs are the main coverage signal right now

## 7. If you need to regenerate or transform the data

Treat these as the priority order of truth:

1. `db/snippet_bank.sqlite`
2. `content/.../*.md`
3. `exports/*.tsv`

Do **not** rebuild from the giant question digest unless you are intentionally redoing the taxonomy.

## 8. What to do after the human review

1. apply feedback to snippets / taxonomy / structure
2. run the step-8 stress test question by question
3. patch any coverage gaps immediately
4. only then generate presets and final nav curation
5. freeze a production release
