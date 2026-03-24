# Overnight Agent Runbook

This runbook is for unsupervised overnight execution of the snippet-completeness phase.

Primary objective:

- improve snippet completeness end-to-end
- keep the work resumable
- avoid drifting into premature architecture/UI refactors

Primary checklist:

- [SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/docs/curation/SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md)

Execution board:

- [OVERNIGHT_EXECUTION_BOARD.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/OVERNIGHT_EXECUTION_BOARD.md)

## Recommended Automation Pattern

Use a supervisor-worker loop, not one giant prompt.

Good fit:

- a Ralph-style loop
- or any similar recurring supervisor agent pattern

Why:

- the work is multi-phase
- there are natural checkpoints
- the repo already has resumable pipeline artifacts
- independent workers need bounded scopes to avoid stepping on each other

## Recommended Topology

### One Supervisor

The supervisor should own:

- reading the checklist
- checking current state
- choosing the next cluster
- assigning workers with disjoint scopes
- integrating results
- running validation
- updating the execution board

The supervisor should not:

- blindly re-scan the whole repo every loop
- hand workers vague goals like “improve snippets”
- start UI/data-model refactors during this phase

### Two To Four Workers

Suggested worker scopes:

- worker A: strings, formatting, predicates, indexing
- worker B: loops, operators, comprehensions, dictionaries
- worker C: pandas, lambda, datetime
- worker D: OOP, returns, scope, flexible arguments, light retrieval cleanup

If multiple workers are active:

- give them disjoint write scopes whenever possible
- if they must touch the same file, stagger those tasks instead of parallelizing them

## Supervisor Loop

Repeat this cycle:

1. Read:
   - the execution checklist
   - the execution board
   - `python3 scripts/vision_exam_pipeline.py status --round round1`
2. Pick one or more unchecked clusters.
3. Delegate bounded work to workers.
4. Wait only when blocked on results.
5. Review and integrate changes.
6. Run targeted tests, then `make leave-better`.
7. Update the execution board with:
   - what finished
   - what is in progress
   - what remains
   - any blockers or quality concerns
8. Start the next loop.

## Guardrails

Always:

- use the current checklist as the source of execution truth
- keep the focus on snippet completeness
- preserve breadth unless something is clearly redundant or weak
- prefer compact reference pieces plus optional explanation pieces
- keep exact-match search improvements fair and light

Never:

- use OCR or deterministic text extraction for exam capture
- pivot into topic-first UI work during this phase
- hard-prune aggressively before the next grading pass
- reward bloat by creating lots of tiny selectable pieces

## Suggested Supervisor Prompt Shape

Use something like:

```text
You are the overnight supervisor for the snippet-completeness phase.

First read:
- docs/curation/SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md
- data/vision_exam_pipeline/OVERNIGHT_EXECUTION_BOARD.md
- data/vision_exam_pipeline/plan_after_manual_synthesis.md
- data/vision_exam_pipeline/review_packets/round1_manual_synthesis.md

Then run:
- python3 scripts/vision_exam_pipeline.py status --round round1

Your job is to:
- choose the next unchecked high-value cluster(s)
- delegate bounded tasks to workers
- integrate results
- run validation
- update the execution board

Do not start UI/topic-architecture refactors in this phase.
Do not aggressively prune the corpus before the next grading pass.
```

## Suggested Worker Prompt Shape

```text
You own only this cluster: <cluster name>.

Read:
- docs/curation/SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md
- data/vision_exam_pipeline/plan_after_manual_synthesis.md
- data/vision_exam_pipeline/review_packets/round1_manual_synthesis.md

Your task:
- implement only the approved snippet additions/edits for this cluster
- keep snippets concise and cheat-sheet optimized
- split selectable pieces only when users may reasonably want one without the other
- avoid drifting into unrelated cleanup

Before finishing:
- summarize exactly what changed
- note any overlap risk with other clusters
- do not touch UI/topic-architecture work
```

## Resume Protocol

At the start of any resumed run:

1. Read the execution board.
2. Run:

```bash
python3 scripts/vision_exam_pipeline.py status --round round1
```

3. Compare the status output against the board.
4. If they disagree, trust the files and fix the board.

## Failure Handling

If a worker stalls:

- do not wait indefinitely
- reclaim the cluster and either narrow the task or do the integration locally

If validation fails:

- fix the failure before starting new cluster work

If two clusters overlap unexpectedly:

- pause parallel execution for those files
- assign one canonical owner

## Minimum Overnight Deliverable

A successful overnight run should ideally produce:

- implemented high-value completeness improvements
- passing `make leave-better`
- an updated execution board
- a clear handoff about what is now ready for the next grading pass
