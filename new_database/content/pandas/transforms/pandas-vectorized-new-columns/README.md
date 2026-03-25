# Vectorized new columns

> [!summary] Snippet summary
> Create new columns with vectorized column arithmetic instead of row-by-row Python loops where possible.

> [!info] Metadata
> - Slug: `pandas-vectorized-new-columns`
> - Topic: `Pandas` (`pandas`)
> - Subtopic: `Transforms` (`transforms`)
> - Course phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `common` across `3` exam families / `7` referenced questions
> - Keywords: `new column`, `vectorized`, `column arithmetic`
> - Trap slugs: `broadcast_shape_mismatch`, `vectorized_ops_vs_map`

> [!tip] Why this exists
> Many pandas questions are easiest because the answer is just `df['new'] = df['A'] - df['B']` or a similar vectorized expression.

## Piece files

- `01_vectorized-patterns.md` — **Vectorized patterns** (`template` · `core` · `default`)
- `02_scalar-series-is-fine.md` — **Scalar + Series is fine** (`rules` · `core` · `default`)
- `03_trap-hint.md` — **Trap hint** (`rules` · `trap` · `optional`)

## Question references

`final-exam-solutions-for-python-programming-62oop21-q05`, `final-exam-solutions-for-python-programming-62oop21-q06`, `final-exam-study-guide-trial-python-basics-2023-q20`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q23`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q24`, `resit-solutions-for-introduction-to-python-35761538-q23`, `resit-solutions-for-introduction-to-python-35761538-q24`
