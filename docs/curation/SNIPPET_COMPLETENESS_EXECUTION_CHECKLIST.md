# Snippet Completeness Execution Checklist

Execution-ready checklist for the current overnight objective:

- maximize snippet completeness
- do not prematurely reorganize the UI or data architecture
- prepare the corpus for one more evidence-driven grading pass after the new snippets are in place

This checklist is the primary execution surface for agents working on the post-synthesis snippet expansion round.

## Objective

Build the missing snippet corpus needed to answer past/mock exam questions more completely, while keeping the work:

- cheat-sheet optimized
- concise
- selectable at the right granularity
- compatible with a later grading pass that will determine final topic/category structure

## Current Scope Lock

Do:

- add the approved missing snippets
- expand or merge existing snippets where approved
- add metadata that may help later (`main_theme`, `related_themes`, `main_week`, `related_weeks`) if it is low-risk
- improve exact-match retrieval text only when it is clearly helpful and fair
- keep the corpus broad until the next grading pass

Do not:

- refactor the UI into topic-first navigation yet
- rewrite the overall topic/week data model yet
- hard-prune large parts of the corpus yet
- use OCR, `pdftotext`, or deterministic PDF text extraction for exam capture
- optimize rankings or categories based only on intuition

## Sources Of Truth

Start every run from these files:

- [plan_after_manual_synthesis.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/plan_after_manual_synthesis.md)
- [round1_manual_synthesis.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/review_packets/round1_manual_synthesis.md)
- [exam_question_bank.json](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/exam_question_bank.json)
- [round1.json](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/evaluations/round1.json)
- [topic_cards.json](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/topic_cards.json)
- [study_db.json](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/study_db.json)

Quick state check:

```bash
python3 scripts/vision_exam_pipeline.py status --round round1
```

## Definition Of Done For This Phase

This phase is done when:

- all approved snippet additions/edits from the manual synthesis review are implemented
- the updated corpus remains internally valid
- no obvious high-value completeness gaps remain from the approved cluster list
- the project is ready for a fresh grading pass

This phase is not done when:

- the UI/topic architecture has been redesigned
- final ranking/preset logic has been implemented
- topic categories have been fully redefined

## Execution Order

### Phase 1. Prepare And Orient

- [ ] Read the scope lock above.
- [ ] Run `python3 scripts/vision_exam_pipeline.py status --round round1`.
- [ ] Read the current plan and the manual synthesis packet.
- [ ] Identify the next highest-value unchecked cluster from the manual packet.
- [ ] Confirm whether the work is `add`, `edit existing`, or `merge into existing`.

Done when:

- you can state exactly which cluster you are working on
- you know which files you expect to touch

### Phase 2. Implement High-Value Additions

Start with these clusters:

- [ ] Essential String Methods and Indexing Reference
- [ ] Output Formatting and String Construction
- [ ] Boolean String Predicates
- [ ] Iteration Helpers and Basic Operator Traps
- [ ] Comprehension Syntax Reference
- [ ] Dictionary Construction and Iteration Patterns
- [ ] Pandas Selection and Indexing Rules
- [ ] Lambda, `map`, and `apply`
- [ ] Datetime Parse/Format + object-vs-string arithmetic reference family
- [ ] OOP Fundamentals
- [ ] Flexible Arguments, Returns, and `kwargs`

For each new snippet family:

- [ ] prefer concise, exam-useful pieces
- [ ] include compact reference-first content
- [ ] add optional explanation only when it genuinely adds value
- [ ] split into separate selectable pieces only when users may reasonably want one without the other
- [ ] avoid turning one concept into many tiny fragments

Done when:

- the approved additions exist in the dataset
- they are selectable in a way that feels deliberate rather than over-fragmented

### Phase 3. Implement Approved Expansions And Merges

- [ ] Pandas Filtering, Aggregation, and Column Arithmetic: expand existing instead of blindly adding a new standalone cluster
- [ ] OOP Comparison Logic: merge into existing or expand the strongest current item
- [ ] Return-Value and Scope Cleanup: edit existing
- [ ] Exact-Match Retrieval Fixes: small, fair, non-biased improvements only

Rules:

- [ ] do not over-optimize `search_text` toward arbitrary snippets
- [ ] avoid making agents prefer one snippet only because its wording is easier to match
- [ ] preserve fair discoverability across similar snippets

Done when:

- existing high-value snippets are stronger, clearer, and more self-contained
- no retrieval improvement feels manipulative or unfair

### Phase 4. Conservative Curation Pass

- [ ] merge obvious near-duplicates
- [ ] avoid hard-pruning before the next grading pass unless something is clearly redundant or low quality
- [ ] preserve breadth of information
- [ ] prefer compact transformations over deletions when possible

Done when:

- the corpus is cleaner
- information breadth has not been meaningfully reduced

### Phase 5. Validate

- [ ] run targeted tests while working
- [ ] run `python3 scripts/vision_exam_pipeline.py status --round round1` again
- [ ] run `make leave-better`

Done when:

- tests pass
- maintenance audit has no failures

### Phase 6. Prepare For The Next Pass

- [ ] update the execution board
- [ ] write a concise handoff noting which clusters are complete, partially complete, or untouched
- [ ] note any unresolved ambiguity that should be reviewed before the next grading pass

Done when:

- another agent can resume work without reconstructing your reasoning from scratch

## Snippet Design Rules

### Piece Splitting

Split into separate selectable pieces only when:

- a user may want the compact version without the explanation
- a table and a code example can stand on their own
- one piece is clearly higher-value than the rest for space-constrained cheat sheets

Keep bundled when:

- the parts only make sense together
- splitting would create tiny low-value fragments
- the extra granularity would mostly add clutter

### Two-Audience Rule

Preferred pattern:

- one compact reference piece
- one optional explanation piece

Only provide both when they add genuinely different value.

### Example Rules

Good examples:

- short correct syntax
- short incorrect syntax when it helps users spot traps
- slightly longer examples only when they efficiently teach several related patterns

Avoid:

- long decorative examples
- question-specific overfitting unless the same pattern recurs across multiple exams

### Tables

Use reference tables aggressively when they compress information better than prose.

Good table types:

- syntax / what it does
- correct / incorrect / why
- code / output
- operation / return type / common trap

## Stop Conditions

Stop and escalate if:

- the work starts drifting into topic/UI restructuring
- you are about to delete a lot of existing content before the next grading pass
- two candidate snippets should maybe be one canonical snippet but the merge would destroy important nuance
- you are no longer improving completeness and are mostly bikeshedding presentation

## Expected Next Phase After This One

Do not do this yet, but optimize for it:

- rerun question grading with the improved corpus
- record near-identical past exam pieces separately from the “best general snippet” judgments
- use actual co-usage patterns to inform future topic structure
