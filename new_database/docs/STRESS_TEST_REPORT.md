# Stress-test report

> [!summary] Purpose
> This document is the final step-8 report.
> It answers the question:
> **Can the snippet bank actually answer the whole exam bank?**

## 1. Rule used during the pass

For each question I recorded:

- `cross_off_score` — how many wrong answers the snippets let me confidently eliminate (`0`–`3`)
- `select_score` — how confidently the snippets let me identify the correct answer (`0`–`3`)
- whether I edited or added a snippet because of that question

Patch rule:

- if `cross_off_score` was not `3`
- **and** `select_score` was below `2`

then the relevant snippet had to be edited before moving on.

## 2. Overall result

> [!success] Bank-wide result
> The final bank passes the threshold for **all 168 questions**.

| Metric | Value |
|---|---:|
| Questions checked | 168 |
| `cross_off_score = 3` | 168 |
| `select_score = 3` | 163 |
| `select_score >= 2` | 168 |
| Questions that triggered edits | 3 |
| Remaining threshold failures | 0 |

## 3. By exam

| Exam                           |   Questions |   Avg cross-off |   Avg select |   Select=3 |   Select>=2 |   Triggered edits |
|:-------------------------------|------------:|----------------:|-------------:|-----------:|------------:|------------------:|
| 2022 Final Exam                |          24 |               3 |      3       |         24 |          24 |                 0 |
| 2023 Trial Final Study Guide   |          24 |               3 |      2.95833 |         23 |          24 |                 1 |
| 2024 Trial Final               |          24 |               3 |      2.875   |         21 |          24 |                 0 |
| 2023 Resit Exam Guidelines     |          24 |               3 |      3       |         24 |          24 |                 0 |
| 2023 Resit Solutions           |          24 |               3 |      3       |         24 |          24 |                 0 |
| 2025 Sample Final Plus Answers |          24 |               3 |      3       |         24 |          24 |                 2 |
| Trial Final Later-Course Focus |          24 |               3 |      2.95833 |         23 |          24 |                 0 |

## 4. Questions that triggered snippet edits

| Question ID                                         | Exam                           |   Q# | Primary snippet                        | Action                         | Change notes                                                                                                                                          |
|:----------------------------------------------------|:-------------------------------|-----:|:---------------------------------------|:-------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| final-exam-study-guide-trial-python-basics-2023-q24 | 2023 Trial Final Study Guide   |   24 | Object state and collection attributes | yes I edited one snippet       | Added a numbered-report-dictionary piece to the OOP collection-attributes snippet so the `enumerate(..., start=1)` garage-report pattern is explicit. |
| sample-final-plus-answers-q02                       | 2025 Sample Final Plus Answers |    2 | Object state and collection attributes | yes I edited multiple snippets | Added an average-rating OOP piece and added `round(x, n)` to the built-ins snippet so the rounded output 3.7 is directly supported.                   |
| sample-final-plus-answers-q03                       | 2025 Sample Final Plus Answers |    3 | f-strings and .format()                | yes I edited one snippet       | Expanded the f-strings snippet with a list-of-dicts print pattern and `:.1f` formatting so the correct loop/access pattern is explicit.               |

## 5. Questions that remained at `select_score = 2`

These still meet the required threshold, but they are the ones where the student is usually **deducing** the answer rather than recognizing it instantly.

| Question ID                                                   | Exam                           |   Q# | Primary snippet                          |   Cross-off |   Select |
|:--------------------------------------------------------------|:-------------------------------|-----:|:-----------------------------------------|------------:|---------:|
| final-exam-study-guide-trial-python-basics-2023-q06           | 2023 Trial Final Study Guide   |    6 | Build, count, and aggregate dictionaries |           3 |        2 |
| introduction-to-python-trial-final-exam-solutions-py22-q06    | 2024 Trial Final               |    6 | Build, count, and aggregate dictionaries |           3 |        2 |
| introduction-to-python-trial-final-exam-solutions-py22-q12    | 2024 Trial Final               |   12 | *args and **kwargs                       |           3 |        2 |
| introduction-to-python-trial-final-exam-solutions-py22-q23    | 2024 Trial Final               |   23 | Compare/report method patterns           |           3 |        2 |
| trial-final-exam-solutions-introduction-to-python-3077951-q08 | Trial Final Later-Course Focus |    8 | Dictionary comprehension patterns        |           3 |        2 |

## 6. Interpretation

The snippet bank is now:

- strong at eliminating wrong options quickly
- strong at recurring pattern recognition
- especially reliable on the bank’s dominant question forms:
  - “which code works?”
  - “what prints / returns?”
  - “why does this fail?”
  - “which option could / could not have created this?”

The remaining `select_score = 2` cases are acceptable because the snippets still narrow the field completely and support a confident deduction.
