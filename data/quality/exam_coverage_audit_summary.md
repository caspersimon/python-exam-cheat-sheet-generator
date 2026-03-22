# Exam Coverage Audit Summary

Audit date: `2026-03-22`

## Scope

- Method: vision-first review of rendered PNG pages only
- PDFs reviewed: 7 unique exams
- Duplicate handling: excluded the duplicate 2022 final copy
- Official scoring corpus:
  - common exam questions
  - key points
  - key-point details
  - AI examples
  - recommended source snippets
  - additional source snippets
- `ai_summary` was tracked as a follow-up signal only and did not materially change any audited question outcome

## Overall Result

- Total questions reviewed: `168`
- Score `3`: `87`
- Score `2`: `58`
- Score `1`: `22`
- Score `0`: `1`
- Questions answerable from the builder without outside knowledge (`score >= 2`): `145 / 168` (`86.3%`)

## By Exam

| Exam | Qs | 3 | 2 | 1 | 0 | Verdict |
|---|---:|---:|---:|---:|---:|---|
| `sample-final-plus-answers` | 24 | 24 | 0 | 0 | 0 | Excellent raw coverage; discoverability still weak because many exact matches live in `additional`. |
| `trial-final-exam-solutions-introduction-to-python-3077951` | 24 | 24 | 0 | 0 | 0 | Excellent raw coverage; exact matches already exist for every question. |
| `introduction-to-python-trial-final-exam-solutions-py22` | 24 | 7 | 12 | 5 | 0 | Strong coverage with a mix of exact and concept-level support. |
| `final-exam-study-guide-trial-python-basics-2023` | 24 | 6 | 12 | 6 | 0 | Good coverage, but several synthesis-heavy questions still need prior knowledge. |
| `final-exam-solutions-for-python-programming-62oop21` | 24 | 6 | 12 | 5 | 1 | Good coverage overall; one genuine gap remained. |
| `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023` | 24 | 10 | 11 | 3 | 0 | Strong coverage with only a few partial-support questions. |
| `resit-solutions-for-introduction-to-python-35761538` | 24 | 10 | 11 | 3 | 0 | Strong coverage with only a few partial-support questions. |

## Strongest Findings

- The current-year sample final is fully covered at `24 / 24` exact matches.
- The later-course trial final is also fully covered at `24 / 24` exact matches.
- Across the full deduplicated audit set, exact-match coverage is already very high because many practice-exam questions were imported into the builder as selectable `source_exam` items.
- There was only one audited `score 0` question: the 2022 final question asking for the sub-list with the highest element sum from a list of lists.

## Why This Is Not “Great” Yet

- Discoverability is weaker than raw coverage.
  - In the current sample final alone, `14 / 24` exact matches are only surfaced in `additional`.
  - Several exact matches are routed under topic cards that are not intuitive for students.
- The weaker questions cluster around synthesis-heavy tasks rather than direct recall:
  - multi-method OOP implementations
  - interval-overlap / datetime logic
  - some pandas construction and transformation tasks
  - a few string-formatting and `kwargs` ordering questions
- Exact coverage is inflated by imported exam snippets. That is useful, but it means “the builder contains the answer somewhere” is stronger than “a student will easily find the right answer path.”

## Practical Verdict

The cheat sheet generator is already strong on raw exam coverage, and very strong for the current sample final. I would not call it great yet for student-facing use, because discoverability and topic routing still lag behind the underlying content quality.

If the goal is “can the builder answer practice-exam questions at all?”, the answer is yes.

If the goal is “can a student quickly find the right support without hunting through `additional` or oddly routed cards?”, the answer is not consistently yes yet.

## Recommended Next Step

- Prioritize [RM-008](../../docs/specs/RM-008-exam-snippet-discoverability.md):
  - promote exact exam-match items out of `additional` when appropriate
  - fix misrouted exam snippets
  - keep auditing after each curation pass

## Notes

- The current sample-final detailed map is saved in [current_sample_exam_coverage_report.md](./current_sample_exam_coverage_report.md).
- The rendered audit packet is available under `tmp/exam_coverage_audit/`.
