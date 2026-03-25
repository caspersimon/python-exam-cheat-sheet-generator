# Vectorized new columns

> [!summary] Summary
> Create new columns with vectorized column arithmetic instead of row-by-row Python loops where possible.

> [!info] Metadata
> - Snippet slug: `pandas-vectorized-new-columns`
> - Topic: `pandas` — Pandas
> - Subtopic: `transforms` — Transforms
> - UI section: `start-here` — Start here
> - Default priority: `5`
> - Recurrence: `common` across `3` family/families and `7` question(s)
> - Phase: `post-midterm`
> - Difficulty: `mixed`
> - Default-selected pieces: `2/3`
> - Estimated space: `310` chars selected / `432` chars total
> - Trap count: `2`
> - Included in presets: `balanced-default`, `post-midterm-tilted`, `ultra-dense-core`

**Why it matters.** Many pandas questions are easiest because the answer is just `df['new'] = df['A'] - df['B']` or a similar vectorized expression.

## Piece index

| # | Piece title | kind | role | default selected | file |
|---:|---|---|---|---|---|
| 1 | Vectorized patterns | `template` | `core` | yes | `01_vectorized-patterns.md` |
| 2 | Scalar + Series is fine | `rules` | `core` | yes | `02_scalar-series-is-fine.md` |
| 3 | Trap hint | `rules` | `trap` | no | `03_trap-hint.md` |

## Keywords

`column arithmetic`, `new column`, `vectorized`

## Trap slugs

`broadcast_shape_mismatch`, `vectorized_ops_vs_map`

## Question refs

`final-exam-solutions-for-python-programming-62oop21-q05`, `final-exam-solutions-for-python-programming-62oop21-q06`, `final-exam-study-guide-trial-python-basics-2023-q20`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q23`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q24`, `resit-solutions-for-introduction-to-python-35761538-q23`, `resit-solutions-for-introduction-to-python-35761538-q24`
