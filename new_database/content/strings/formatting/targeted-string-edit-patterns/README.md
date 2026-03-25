# Targeted string edits

> [!summary] Summary
> Small but common string-edit tasks: swap two marked letters, replace only one occurrence, or normalize text before comparison.

> [!tip] Why this snippet matters
> These questions reward knowing the exact order of operations, especially because strings are immutable and `replace(..., count)` works left-to-right.

## Metadata

- slug: `targeted-string-edit-patterns`
- topic: `strings`
- subtopic: `formatting`
- course phase: `post-midterm`
- default priority: `4`
- difficulty: `mixed`
- recurrence: `very-common`
- question refs: `6`
- traps: `2`

## Pieces

- `01` **Single-occurrence replace rule** — `rules` / `core` / default `yes`
- `02` **Swap `x` and `y` when each appears once** — `example` / `clarifier` / default `no`
- `03` **Normalize before comparing strings** — `template` / `core` / default `yes`
