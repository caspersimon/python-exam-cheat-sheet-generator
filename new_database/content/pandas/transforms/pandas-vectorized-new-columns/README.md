# Vectorized new columns

> [!summary] Summary
> Create new columns with vectorized column arithmetic instead of row-by-row Python loops where possible.

> [!tip] Why this snippet matters
> Many pandas questions are easiest because the answer is just `df['new'] = df['A'] - df['B']` or a similar vectorized expression.

## Metadata

- slug: `pandas-vectorized-new-columns`
- topic: `pandas`
- subtopic: `transforms`
- course phase: `post-midterm`
- default priority: `5`
- difficulty: `mixed`
- recurrence: `common`
- question refs: `7`
- traps: `2`

## Pieces

- `01` **Vectorized patterns** — `template` / `core` / default `yes`
- `02` **Scalar + Series is fine** — `rules` / `core` / default `yes`
- `03` **Trap hint** — `rules` / `trap` / default `no`
