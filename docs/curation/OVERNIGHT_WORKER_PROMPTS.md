# Overnight Worker Prompt Templates

Use these as bounded worker prompts under a single supervisor.

## Shared Worker Prefix

```text
Read first:
- AGENTS.md
- RTK.md
- docs/curation/SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md
- data/vision_exam_pipeline/plan_after_manual_synthesis.md
- data/vision_exam_pipeline/review_packets/round1_manual_synthesis.md

You own only the assigned cluster below.

Rules:
- optimize for snippet completeness
- keep snippets concise and cheat-sheet friendly
- split selectable pieces only when users may reasonably want one without the other
- do not drift into UI/topic-architecture refactors
- do not aggressively prune old material
- if a merge/delete is risky, note it instead of forcing it

Before finishing:
- summarize exactly what changed
- name the files touched
- mention any overlap or merge-risk for the supervisor
```

## Worker A

```text
Cluster ownership:
- Essential String Methods and Indexing Reference
- Output Formatting and String Construction
- Boolean String Predicates
```

## Worker B

```text
Cluster ownership:
- Iteration Helpers and Basic Operator Traps
- Comprehension Syntax Reference
- Dictionary Construction and Iteration Patterns
```

## Worker C

```text
Cluster ownership:
- Pandas Selection and Indexing Rules
- Pandas Filtering, Aggregation, and Column Arithmetic (expand existing)
- Lambda, `map`, and `apply`
- Datetime Parse/Format + object-vs-string arithmetic reference family
```

## Worker D

```text
Cluster ownership:
- OOP Fundamentals
- OOP Comparison Logic
- Flexible Arguments, Returns, and `kwargs`
- Return-Value and Scope Cleanup
- Exact-Match Retrieval Fixes (light and fair only)
```
