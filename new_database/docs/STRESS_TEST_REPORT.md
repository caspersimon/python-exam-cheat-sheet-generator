# Stress-test report

> [!summary] Baseline status
> The original final-bank release already passed the required threshold for **all 168 questions**.
> V2 mainly adds backup/reference coverage from the old dataset, so the per-question baseline scores are carried forward.

## Threshold check

- questions with `cross_off_score >= 3`: **168 / 168**
- questions with `select_score >= 2`: **168 / 168**
- questions below threshold: **0**

## Score distribution

| Cross-off score | Select score | Question count |
|---:|---:|---:|
| 3 | 2 | 5 |
| 3 | 3 | 163 |

## Interpretation

> [!tip] What V2 changed
> V2 did **not** need a fresh rescue pass to clear the bank. Instead, it broadens coverage around older/reference material:
> syntax fragments, aliasing/copies, numeric edge cases, iterator/control-flow backups, pandas missing-value alignment, and inheritance.

See `exports/question_stress_test.tsv` for the full per-question baseline table.
