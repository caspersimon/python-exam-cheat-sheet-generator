# Spec: RM-009 Vision-First Exam Curation Pipeline

## Metadata

- ID: `RM-009`
- Status: `in_progress`
- Priority: `High`
- Owner: `codex/human`
- Last Updated: `2026-03-24`

## Problem

The repo already contains exam imports and audit packets, but the exam data is still a mix of partial imports, legacy provenance, and text/OCR-derived material. That makes it hard to guarantee that every past/mock exam question is captured once, reviewed consistently, and mapped to the most useful snippet evidence for student-facing curation.

## Goals

- Build a vision-only exam capture workflow that treats rendered page images as the source of truth for question review.
- Store a persistent canonical question bank for each unique exam, including duplicate/alias metadata and explicit completeness status.
- Add question-to-snippet evaluation artifacts that record the best snippets, top 3 snippets, minimal sufficient snippet sets, and gap notes.
- Produce synthesis and ranking outputs that can drive later snippet reclassification, presets, and week-level leaderboards.

## Non-Goals

- Rewriting the Topic Explorer UI in this phase.
- Implementing leaderboard or preset pages before the ranking logic is agreed.
- Using `pdftotext`, OCR, or any other deterministic text-layer extraction for exam question capture.

## Proposed Solution

Keep `data/study_db.json` as the canonical course-content database, but add separate derived JSON artifacts under `data/vision_exam_pipeline/` for the exam workflow:

- a question bank for reviewed exam questions and provenance
- a question-evaluation file for snippet scoring and answerability notes
- a synthesis file for suggested edits/additions with pros/cons
- a ranking summary for weekly highest-value snippet analysis

Use the existing render packet pattern from `scripts/exam_coverage_audit.py` as the bootstrap for page PNG generation, then have agents review only the PNGs. The orchestrator should be resumable and idempotent so page rendering, question capture, evaluation, synthesis, and analytics can be run in separate passes.

## Implementation Plan

1. Add a pipeline entrypoint (`scripts/vision_exam_pipeline.py`) that can prepare page renders, audit completeness, record reviewed questions, evaluate snippet evidence, synthesize edits, and generate ranking analytics.
2. Define stable JSON contracts for the question bank, evaluations, synthesis, and ranking outputs.
3. Seed the new artifacts from the current audit packet and legacy imports, but mark legacy records as provisional until they are superseded by vision-reviewed records.
4. Document the workflow in the testing and dataset references so future curation rounds follow the same capture and review policy.

## Risks and Mitigations

- Risk: Duplicate PDFs could create duplicate canonical entries.
- Mitigation: Keep one canonical exam record per unique exam and store duplicate copies as aliases/audit evidence only.
- Risk: Mixing OCR-derived and vision-derived records could blur provenance.
- Mitigation: Preserve explicit provenance fields and treat the vision-reviewed records as the authoritative layer.
- Risk: Ranking logic may be premature before the evaluation round is complete.
- Mitigation: Keep ranking outputs separate from UI implementation and gate step 8 on the human review round.

## Test Plan

- Validate every derived JSON artifact against a schema.
- Check that each unique target exam reaches the expected question count.
- Verify the duplicate 2022 final does not produce a second canonical exam bank entry.
- Confirm every snippet reference points at a currently selectable item.
- Re-run the pipeline from a partial state to confirm resume/idempotency.

## Rollout and Validation

- Start with the seven unique exam sources already covered by the audit packet.
- Reuse the existing rendered PNG packet when it matches the current source PDFs.
- Review the question bank and evaluation summaries before implementing any snippet reclassification or UI changes.

## Current Follow-Up

The pipeline itself is now in active use and has produced:

- a complete canonical question bank
- a first completed evaluation round
- synthesis and analytics artifacts
- human/manual review packets

The current follow-up phase is deliberately completeness-first:

- improve the snippet corpus using the approved manual synthesis decisions
- avoid premature UI/topic-architecture refactors
- rerun grading only after the snippet corpus is stronger

Operator docs for this follow-up live in:

- `docs/curation/SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md`
- `docs/curation/OVERNIGHT_AGENT_RUNBOOK.md`
- `docs/VISION_EXAM_PIPELINE.md`
- `data/vision_exam_pipeline/RUNBOOK.md`

## Open Questions

- Which exact JSON filenames should be treated as the long-term canonical review artifacts if the pipeline expands further?
- Should page PNGs remain temporary regeneration artifacts, or should some be stored in a persistent local cache for repeated vision passes?
