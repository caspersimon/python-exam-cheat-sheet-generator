# Current Sample Final Coverage Audit

## Summary

- Exam: `sample-final-plus-answers`
- Question count: 24
- Exact selectable matches found: 24/24
- Score distribution: `3 => 24`, `2 => 0`, `1 => 0`, `0 => 0`
- Exact matches already in `recommended`: 10
- Exact matches only in `additional`: 14

## Key Findings

- The builder already contains an exact selectable `source_exam` item for every question in the current sample final.
- Discoverability is weaker than raw coverage: 14 of the 24 exact matches are hidden in `additional` rather than `recommended`.
- Several exact matches appear routed under topic cards that do not match the imported question topic labels. The most obvious examples are questions 1-2 (OOP questions currently under `Pandas Core Structures`) and questions 5-8 (Pandas/String-method questions mapped into string-heavy or other non-obvious cards).
- This makes the current dataset better as a hidden coverage corpus than as an easy-to-navigate student-facing cheat-sheet builder.

## Question Map

| Q | Imported topic label | Current card topic | Bucket | Evidence item id |
|---|---|---|---|---|
| 1 | OOP (Initializers) | Pandas Core Structures | recommended | `exam-intro_python_sample_final_24_25-1-w5-pandas-core-structures` |
| 2 | OOP (Methods) | Pandas Core Structures | recommended | `exam-intro_python_sample_final_24_25-2-w5-pandas-core-structures` |
| 3 | Dictionaries | Defining and Calling Functions | recommended | `exam-intro_python_sample_final_24_25-3-w3-defining-and-calling-functions` |
| 4 | String Methods | Conditions | additional | `exam-intro_python_sample_final_24_25-4-w2-conditions` |
| 5 | Pandas (Basic) | String Fundamentals | recommended | `exam-intro_python_sample_final_24_25-5-w4-string-fundamentals` |
| 6 | Pandas (Indexing) | String Operations and Methods | recommended | `exam-intro_python_sample_final_24_25-6-w4-string-operations-and-methods` |
| 7 | Pandas (Subset/Sort) | String Fundamentals | recommended | `exam-intro_python_sample_final_24_25-7-w4-string-fundamentals` |
| 8 | Pandas (Series Strings) | String Fundamentals | recommended | `exam-intro_python_sample_final_24_25-8-w4-string-fundamentals` |
| 9 | Datetime (Parsing) | Datetime | recommended | `exam-intro_python_sample_final_24_25-9-w6-datetime` |
| 10 | Datetime (Arithmetic) | Datetime | recommended | `exam-intro_python_sample_final_24_25-10-w6-datetime` |
| 11 | Comprehensions | Defining and Calling Functions | recommended | `exam-intro_python_sample_final_24_25-11-w3-defining-and-calling-functions` |
| 12 | List Comprehensions | Conditions | additional | `exam-intro_python_sample_final_24_25-12-w2-conditions` |
| 13 | Data Types | Objects and Names | additional | `exam-intro_python_sample_final_24_25-13-w1-objects-and-names` |
| 14 | Loops | Loops | additional | `exam-intro_python_sample_final_24_25-14-w2-loops` |
| 15 | Functions (Scope) | Conditions | additional | `exam-intro_python_sample_final_24_25-15-w2-conditions` |
| 16 | Lambdas | Higher-Order Patterns | additional | `exam-intro_python_sample_final_24_25-16-w3-higher-order-patterns` |
| 17 | Iterables/Logic | Defining and Calling Functions | additional | `exam-intro_python_sample_final_24_25-17-w3-defining-and-calling-functions` |
| 18 | Slicing | Conditions | additional | `exam-intro_python_sample_final_24_25-18-w2-conditions` |
| 19 | Dictionaries | Defining and Calling Functions | additional | `exam-intro_python_sample_final_24_25-19-w3-defining-and-calling-functions` |
| 20 | Dictionaries | Defining and Calling Functions | additional | `exam-intro_python_sample_final_24_25-20-w3-defining-and-calling-functions` |
| 21 | Dict Iteration | Defining and Calling Functions | additional | `exam-intro_python_sample_final_24_25-21-w3-defining-and-calling-functions` |
| 22 | String Methods | Conditions | additional | `exam-intro_python_sample_final_24_25-22-w2-conditions` |
| 23 | Functions (*args) | Arguments | additional | `exam-intro_python_sample_final_24_25-23-w3-arguments` |
| 24 | Modules | Conditions | additional | `exam-intro_python_sample_final_24_25-24-w2-conditions` |

## Follow-up

- Roadmap item: [RM-008](../../docs/specs/RM-008-exam-snippet-discoverability.md)
- Validated findings file: `tmp/exam_coverage_audit/sample_final_findings.json`
