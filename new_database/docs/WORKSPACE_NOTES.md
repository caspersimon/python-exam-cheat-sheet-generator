# Workspace notes

> [!summary] Status
> Steps **2–6** are complete. This file records the setup decisions, manual coding workflow, and the main conclusions that shaped the current snippet bank.

## Step 2 — workspace setup

- [x] Created a working directory with separate areas for `content`, `db`, `exports`, `docs`, and `notes`
- [x] Built a full question digest from the supplied exam bank
- [x] Decided on an authoritative data shape: **SQLite + markdown content files**
- [x] Reserved TSV exports for quick inspection and easy import into other systems

> [!info] Why not a giant JSON file?
> The snippet bodies contain:
> - multi-line code fences
> - markdown tables
> - inline backticks
> - small formatting differences that matter
>
> Keeping the body text in standalone `.md` files makes the content easier to edit, diff, render, and import into a frontend without newline-escaping pain.

## Step 3 — manual close inspection and coding strategy

### How the questions were coded

I did **not** start with a deterministic classifier.

Instead, I manually reviewed the exams by family, in small batches, and iteratively assigned:

- a **main topic**
- a **subtopic**
- a **dominant question form**
- a **primary snippet**
- optional **secondary snippets**
- a rough **course-phase** label (`pre-midterm`, `post-midterm`, or later `mixed` for survival snippets)

This means the taxonomy is qualitative-first, then structured.

### Deduplication / family handling

Some source exams are clearly related enough that counting all of them equally would inflate recurrence.

The family comparison used for pattern analysis looks like this:

| Exam A                         | Exam B                         |   Avg similarity |   Questions ≥ 0.7 |   Questions ≥ 0.5 |
|:-------------------------------|:-------------------------------|-----------------:|------------------:|------------------:|
| 2025 Sample Final Plus Answers | Trial Final Later-Course Focus |            0.7   |                15 |                16 |
| 2023 Resit Exam Guidelines     | 2023 Resit Solutions           |            0.929 |                22 |                24 |
| 2023 Trial Final Study Guide   | 2024 Trial Final               |            0.259 |                 2 |                 5 |

Interpretation:

- the **resit pair** should be treated as one family for recurrence analysis
- the **sample final / later-course trial** pair is strongly related and should also be deduped when asking “how often does this pattern recur?”
- the **2023 vs 2024 trial finals** are distinct enough to keep separate

### Source-bank anomalies noted during inspection

- `sample-final-plus-answers-q08` and `sample-final-plus-answers-q11` are exact duplicates
- the bank still works fine for pattern mining because the repeated concepts are obvious even when one family partially overlaps another

## Step 4 — what the manual inspection revealed

> [!abstract] High-level exam anatomy
> The exam is cumulative, but with a **post-midterm tilt** rather than a post-midterm monopoly.

Deduped family-level phase counts:

| Exam family                              |   Post-midterm |   Pre-midterm |
|:-----------------------------------------|---------------:|--------------:|
| 2022 final                               |             13 |            11 |
| 2023 resit family                        |             15 |             9 |
| 2023 trial                               |             14 |            10 |
| 2024 trial                               |             14 |            10 |
| 2025 sample-family / later-course family |             13 |            11 |

So the safe interpretation is:

- finals/resits are **not** post-midterm-only
- but they are usually a little heavier on post-midterm material
- students still need a real amount of pre-midterm syntax fluency

### Dominant question forms

Across the five deduped exam families:

| Question form                          |   Questions |
|:---------------------------------------|------------:|
| Choose the code that works             |          52 |
| Predict the output                     |          30 |
| Match equivalent expressions / outputs |          12 |
| Choose the code that fails             |           8 |
| Explain why a mismatch/error happens   |           8 |
| Find the odd one out                   |           4 |
| Fill a template / blank                |           2 |
| Identify the bad line                  |           2 |
| Reverse-engineer a transform           |           1 |
| Select the true statement              |           1 |

The most important design implication for the snippet bank is that students need help with:

1. **quick elimination**
2. **output prediction**
3. **spotting why code fails**
4. **recognizing recurring skeletons**, not memorizing prose wording

### Topic spread

Across the five deduped exam families:

| Topic                         |   Questions |
|:------------------------------|------------:|
| Core Python                   |          24 |
| Dictionaries & comprehensions |          21 |
| Pandas                        |          17 |
| Functions & scope             |          17 |
| Strings                       |          15 |
| OOP                           |          13 |
| Datetime                      |          13 |

Across the full 168-question bank (with duplicates left in):

| Topic                         |   Questions |
|:------------------------------|------------:|
| Dictionaries & comprehensions |          31 |
| Core Python                   |          31 |
| Functions & scope             |          25 |
| Pandas                        |          24 |
| Strings                       |          21 |
| OOP                           |          18 |
| Datetime                      |          18 |

## Step 5 — snippet creation decisions

The current bank has:

- **46 snippets**
- **134 pieces**
- **8 topics**
- **20 subtopics**

### Why the snippet count landed here

> [!tip] Balance point
> This is deliberately in the zone where the library is:
> - small enough to browse
> - large enough to be modular
> - specific enough to mirror exam traps rather than generic Python teaching

The design target was not “make as many pieces as possible”; it was “make pieces small enough that students can remove what they already know by heart.”

## Step 6 — polishing pass notes

During the rewrite / consolidation pass, I intentionally:

- merged generic or overlapping content into **trap-centered** snippets
- avoided repeating the same basic rule in five different topic areas
- kept some “extra clarity” pieces optional by marking them `default_selected = false`
- kept question references mainly at the **snippet level**, because many individual pieces are synthesized from several past questions rather than copied from a single one

## Current deliverable boundaries

> [!warning] Review boundary
> This package intentionally stops **before** the step-8 stress test.
>
> After your review, the next pass should:
> - pressure-test every question against the snippet bank
> - patch any gaps immediately
> - then do the final navigation/preset curation pass
