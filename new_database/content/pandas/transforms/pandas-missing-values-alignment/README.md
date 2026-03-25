# Missing values and index alignment

> [!summary] Summary
> Backup pandas reference for `fillna`, `dropna`, and the label-alignment behavior that can create `NaN` unexpectedly.

> [!tip] Why this snippet matters
> These are classic pandas gotchas: keeping the table shape versus dropping rows, and assuming row-by-row arithmetic when pandas is actually aligning on index labels.

## Metadata

- slug: `pandas-missing-values-alignment`
- topic: `pandas`
- subtopic: `transforms`
- course phase: `post-midterm`
- default priority: `3`
- difficulty: `mixed`
- recurrence: `rare`
- question refs: `0`
- traps: `3`

## Pieces

- `01` **`fillna` versus `dropna`** — `table` / `core` / default `no`
- `02` **Alignment creates `NaN` by labels** — `example` / `clarifier` / default `no`
- `03` **Fast rules** — `rules` / `trap` / default `yes`
