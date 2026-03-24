# Vision Exam Pipeline

Operator-facing map of the vision-first exam pipeline.

Use this when you need to understand:

- which module owns which part of the pipeline
- which artifacts are durable vs disposable
- which states are safe to continue from
- where the human review gates are

## Purpose

The vision exam pipeline is the repo’s exam-review workflow for:

- rendering exam PDFs to PNG pages
- capturing canonical question/answer records from those PNGs
- grading the current snippet corpus against those questions
- producing synthesis and analytics for later curation

This pipeline is separate from the broader raw-ingestion pipeline.

Important boundary:

- the broader raw-ingestion pipeline may use OCR/text extraction for other source types
- the vision exam pipeline must not use OCR, `pdftotext`, or deterministic text-layer extraction for exam capture

## Module Map

- [scripts/vision_exam_pipeline.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/scripts/vision_exam_pipeline.py)
  Thin CLI entrypoint for the pipeline.

- [pipelines/vision_exam_pipeline.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/pipelines/vision_exam_pipeline.py)
  Re-export surface for pipeline helpers.

- [pipelines/vision_exam_pipeline_shared.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/pipelines/vision_exam_pipeline_shared.py)
  Shared constants, paths, IDs, safe helpers, and validation primitives.

- [pipelines/vision_exam_pipeline_bank.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/pipelines/vision_exam_pipeline_bank.py)
  Page manifest prep, bank seeding, completeness reporting, extraction packets, and review-drop merge logic.

- [pipelines/vision_exam_pipeline_gemini.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/pipelines/vision_exam_pipeline_gemini.py)
  Gemini-based auto-capture and auto-evaluation helpers.

- [pipelines/vision_exam_pipeline_review.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/pipelines/vision_exam_pipeline_review.py)
  Evaluation scaffold generation, validation, synthesis, and analytics.

- [pipelines/vision_exam_pipeline_packet.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/pipelines/vision_exam_pipeline_packet.py)
  Human-facing review packet generation.

- [pipelines/vision_exam_pipeline_status.py](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/pipelines/vision_exam_pipeline_status.py)
  Current-state summary for resumable supervision.

## Durable vs Disposable Artifacts

### Durable

These are system-of-record or checkpoint artifacts:

- `data/vision_exam_pipeline/exam_question_bank.json`
- `data/vision_exam_pipeline/exam_question_bank_completeness.json`
- `data/vision_exam_pipeline/selectable_items_snapshot.json`
- `data/vision_exam_pipeline/evaluations/<round>.json`
- `data/vision_exam_pipeline/synthesis/<round>.json`
- `data/vision_exam_pipeline/analytics/<round>.json`
- `data/vision_exam_pipeline/review_packets/<round>.json`
- `data/vision_exam_pipeline/review_packets/<round>.md`
- `data/vision_exam_pipeline/review_packets/<round>_manual_synthesis.md`

### Semi-Durable

Useful inputs or reusable working artifacts:

- `data/vision_exam_pipeline/page_manifest.json`
- `data/vision_exam_pipeline/review_drops/*.json`
- `data/vision_exam_pipeline/work_packets/extractions/*.json`
- `data/vision_exam_pipeline/work_packets/evaluations/<round>/*.json`

### Disposable / Regenerable Inputs

- `tmp/exam_coverage_audit/manifest.json`
- `tmp/exam_coverage_audit/selectable_items.json`
- `tmp/exam_coverage_audit/pages/<exam-id>/page-XX.png`

## State Machine

### Question Bank Review Status

- `seeded_legacy_needs_vision_review`
  Legacy-seeded content exists, but still requires vision review.

- `pending_vision_review`
  No reviewed question record exists yet.

- `agent_reviewed_pending_human_confirmation`
  A vision review has been merged, but not yet human-confirmed.

- `human_confirmed`
  Fully reviewed and human-confirmed.

### Evaluation Status

- `blocked_missing_question_capture`
  Question capture is still missing.

- `captured_pending_human_confirmation`
  Question exists and may be graded, but the bank item is still awaiting human confirmation.

- `pending_review`
  Eligible for grading but not yet completed.

- `completed`
  Grading for that question is filled in.

## Human Gates

Human review is required:

- after synthesis/review-packet generation and before snippet implementation
- after the snippet implementation round and before final ranking/category/UI decisions

Do not automatically cross those gates in unattended runs.

## Safe Operator Loop

Use this order:

1. `prepare-pages`
2. `seed-question-bank`
3. `audit-completeness`
4. `dispatch-extraction`
5. capture and merge review drops until blocked count is zero
6. `dispatch-evaluations`
7. complete evaluations for the target round
8. `synthesize-suggestions`
9. `generate-ranking-analytics`
10. `generate-review-packet`
11. `status`
12. stop at the human gate

## Resume Command

```bash
python3 scripts/vision_exam_pipeline.py status --round round1
```

That command is the fastest way to see:

- question-bank completeness
- evaluation-round completion
- whether synthesis/analytics/review packets exist
- the next gate

## Parallelism Rules

Safe to parallelize:

- page-level or exam-level vision review work that emits separate review-drop files
- read-only analysis
- bounded snippet/content work with disjoint write scopes

Do not parallelize direct writes to canonical files:

- `exam_question_bank.json`
- `evaluations/<round>.json`

Use a single supervisor/integrator for canonical writes.
