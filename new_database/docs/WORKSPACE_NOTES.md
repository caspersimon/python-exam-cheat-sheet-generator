# Workspace notes

> [!summary] Status
> Steps **2–9** are complete.
> This file records the setup decisions, the manual coding workflow, the review-driven revisions, and the final stress-test/preset pass.

## Step 2 — workspace setup

- [x] Built a full question digest from the supplied exam bank
- [x] Chose an authoritative data shape: **SQLite + markdown content files**
- [x] Reserved TSV mirrors for quick inspection and portability
- [x] Kept snippet bodies out of giant escaped JSON fields on purpose

## Step 3 — manual close inspection and coding strategy

The taxonomy was **qualitative-first**, not classifier-first.

I manually reviewed the exams by family, in small batches, and iteratively assigned:

- a **main topic**
- a **subtopic**
- a **question form**
- a **primary snippet**
- optional **secondary snippets**
- a rough **course-phase** label

That qualitative pass is what made the later trap/snippet structure reliable.

## Step 4 — exam anatomy conclusions

The final is best modeled as:

- **cumulative**
- slightly **post-midterm tilted**
- dominated by short **multiple-choice recognition** tasks
- especially dependent on:
  - output prediction
  - “which code works?” elimination
  - spotting why code fails
  - recognizing recurring skeletons with different nouns

## Step 5 — snippet creation result

The final bank now has:

- **45 snippets**
- **137 pieces**
- **8 topics**
- **20 subtopics**

The aim was not to maximize raw piece count.
The aim was to keep pieces small enough that students can leave out what they already know.

## Step 6 — polishing pass decisions

During the rewrite / consolidation pass, I intentionally:

- merged overlapping content into more trap-centered snippets
- kept some clarity-heavy pieces optional with `default_selected = 0`
- made example code more context-rich where needed
- preferred output-first mini examples when a table alone was too abstract

## Step 7 — human review gate

The user reviewed the first half of the snippets and gave style-focused feedback.
Main signals from that review:

- use realistic method call syntax
- prefer concrete examples over vague placeholders
- split overly compressed examples if context is missing
- avoid drifting into “how to write code” advice when the exam is about reading code
- show outputs explicitly when that improves fast recognition

Those preferences were applied to the reviewed pieces and then propagated through the rest of the bank.

## Step 8 — full stress test

Every one of the **168** bank questions was checked against the snippets.

Threshold rule used:

- `cross_off_score` should ideally be `3`
- `select_score` should be at least `2`
- if a question failed both thresholds, a snippet had to be edited before moving on

### Result

- `cross_off_score = 3` for **168 / 168**
- `select_score >= 2` for **168 / 168**
- `select_score = 3` for **163 / 168**
- questions that triggered edits: **3**
- remaining threshold failures: **0**

## Step 9 — final curation

Final curation added:

- four ready-to-use presets
- importance-aware snippet ordering within subtopics
- frontend-friendly snippet grouping fields:
  - `ui_section_slug`
  - `ui_section_title`
  - `ui_section_sort_order`
  - `ui_card_order`
- estimated space metadata per snippet:
  - `default_piece_count`
  - `default_char_count`
  - `total_char_count`

## Deliverable boundary

This package is now the **production-ready final release** for content integration.
