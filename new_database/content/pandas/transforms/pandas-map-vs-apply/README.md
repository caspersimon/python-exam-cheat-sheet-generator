# map() vs apply()

> [!summary] Summary
> When to use `Series.map(...)` and when to use `DataFrame.apply(..., axis=1)`.

> [!tip] Why this snippet matters
> This is the main pandas trap family: elementwise vs rowwise reasoning.

## Metadata

- slug: `pandas-map-vs-apply`
- topic: `pandas`
- subtopic: `transforms`
- course phase: `post-midterm`
- default priority: `5`
- difficulty: `mixed`
- recurrence: `very-common`
- question refs: `7`
- traps: `2`

## Pieces

- `01` **Decision table** — `table` / `core` / default `yes`
- `02` **Correct examples** — `example` / `clarifier` / default `no`
- `03` **Common wrong patterns** — `table` / `trap` / default `yes`
