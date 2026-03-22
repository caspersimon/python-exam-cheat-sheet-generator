# Spec: RM-008 Exam Snippet Discoverability

## Metadata

- ID: `RM-008`
- Status: `in_progress`
- Priority: `High`
- Owner: `codex/human`
- Last Updated: `2026-03-22`

## Problem

The exam coverage audit shows that the current builder can already contain exact matches for exam questions, but discoverability is weaker than coverage. In the current sample-final audit, many exact question matches are surfaced only in `additional`, and several imported exam items appear routed under topic cards that do not match the question's actual subject area.

## Goals

- Promote exact exam-match items so students can find them quickly without digging through `additional`.
- Repair topic/card routing for imported exam snippets whose current card placement is misleading.
- Evaluate whether a constrained subset of `ai_summary` content should become selectable when it materially improves exam answerability.

## Non-Goals

- Rebuild the whole card-generation pipeline in one pass.
- Make every `ai_summary` block selectable by default.

## Proposed Solution

Start with the current-year sample final and other audit-backed high-value exams. For each exact exam-match snippet, verify whether it sits in the correct topic card and whether it belongs in `recommended` instead of `additional`. Where exact matches are absent but `ai_summary` clearly fills a repeated gap, define a small policy for promoting only the highest-value `ai_summary` fragments into selectable content.

## Implementation Plan

1. Use the audit report to list exact exam-match items by question number, card topic, and `recommended`/`additional` bucket.
2. Re-route misclassified exam snippets to the correct topic cards and update `recommended_ids` so exact matches surface earlier.
3. Identify repeated cases where non-selectable `ai_summary` text materially improves answerability and draft a narrow promotion policy.
4. Re-run the exam coverage audit after each curation batch to confirm that discoverability improves, not just raw coverage.

## Risks and Mitigations

- Risk: Aggressively promoting items into `recommended` may make rails noisy.
- Mitigation: Limit promotion to exact matches and repeat offenders from the audit.
- Risk: Re-routing snippets may break subtopic balance or `recommended_ids`.
- Mitigation: Run integrity tests and audit validation after each curation pass.
- Risk: Making `ai_summary` selectable could bloat cards with generic text.
- Mitigation: Gate any promotion behind a strict “material exam value” rule.

## Test Plan

- Run `python3 scripts/exam_coverage_audit.py prepare` and revalidate findings against the updated corpus.
- Run `make leave-better`.
- Spot-check audited questions in the Topic Explorer to confirm the surfaced topic/bucket now makes sense to a student.

## Rollout and Validation

- First target: current-year sample final exact matches.
- 2026-03-22 curation pass:
  - Re-routed the audited misclassified current sample-final exact matches into the more intuitive destination cards.
  - Promoted audited exact matches from the current sample final, 2024 trial final, resits, and related high-value exams into `recommended_ids`.
  - Added small selectable gap-fill examples for repeated weak themes without making `ai_summary` selectable.
- Success criteria:
  - Fewer exact exam matches hidden in `additional`.
  - No obviously misrouted exam snippets in audited high-value questions.
  - Any newly selectable `ai_summary` content is deliberate, sparse, and clearly useful.

## Open Questions

- Should “exact match to a current-year or recent practice-exam question” automatically outrank generic recommended snippets?
- Should `ai_summary` promotion happen as manual curation only, or should the pipeline support a dedicated selectable-summary field?
