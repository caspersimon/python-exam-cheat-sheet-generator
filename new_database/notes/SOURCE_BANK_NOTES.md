# Source bank notes

> [!summary] Why this exists
> Small notes about the supplied exam bank that matter for analysis but do not block snippet use.

## Near-duplicate exam-family comparisons

| Exam A                         | Exam B                         |   Avg similarity |   Questions ≥ 0.7 |   Questions ≥ 0.5 |
|:-------------------------------|:-------------------------------|-----------------:|------------------:|------------------:|
| 2025 Sample Final Plus Answers | Trial Final Later-Course Focus |            0.7   |                15 |                16 |
| 2023 Resit Exam Guidelines     | 2023 Resit Solutions           |            0.929 |                22 |                24 |
| 2023 Trial Final Study Guide   | 2024 Trial Final               |            0.259 |                 2 |                 5 |

## Specific notes

| Note slug | Severity | Affected questions | Note |
|:--|:--|:--|:--|
| `sample-q08-q11-duplicate` | `info` | `sample-final-plus-answers-q08|sample-final-plus-answers-q11` | These two questions are exact duplicates in the supplied bank: same prompt, options, and answer. |
| `family-near-duplicate-sample-vs-later-course` | `info` | `sample-final-plus-answers-q01..q24|trial-final-exam-solutions-introduction-to-python-3077951-q01..q24` | The current-year sample final and the later-course trial final are strongly related. Treat them as the same exam family during analytics to avoid overcounting recurring patterns. |
| `family-near-duplicate-resit-pair` | `info` | `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q01..q24|resit-solutions-for-introduction-to-python-35761538-q01..q24` | The resit guidelines and resit solutions are near-duplicate versions of the same family; dedupe when computing recurrence. |
