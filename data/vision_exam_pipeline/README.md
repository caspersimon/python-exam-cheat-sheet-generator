# Vision-First Exam Pipeline

Derived artifacts for the exam-question review and snippet-value workflow live here.

Key files:

- `page_manifest.json`: target exams plus rendered/reused PNG page paths
- `exam_question_bank.json`: canonical per-exam question bank with provenance and blocked slots
- `exam_question_bank_completeness.json`: completeness report for the current bank
- `selectable_items_snapshot.json`: stable snapshot of selectable snippet IDs used in review rounds
- `evaluations/<round>.json`: per-question snippet evaluations
- `synthesis/<round>.json`: grouped edit/addition suggestions for human review
- `analytics/<round>.json` and `analytics/<round>.md`: ranking-prep summaries
- `work_packets/extractions/*.json`: per-exam capture packets
- `work_packets/evaluations/<round>/*.json`: per-exam evaluation packets

Workflow:

```bash
python3 scripts/vision_exam_pipeline.py prepare-pages
python3 scripts/vision_exam_pipeline.py seed-question-bank
python3 scripts/vision_exam_pipeline.py audit-completeness
python3 scripts/vision_exam_pipeline.py dispatch-extraction
python3 scripts/vision_exam_pipeline.py dispatch-evaluations --round round1 --findings tmp/exam_coverage_audit/seed_exact_matches.json
python3 scripts/vision_exam_pipeline.py synthesize-suggestions --round round1
python3 scripts/vision_exam_pipeline.py generate-ranking-analytics --round round1
python3 scripts/vision_exam_pipeline.py generate-review-packet --round round1
python3 scripts/vision_exam_pipeline.py validate --evaluation-round round1
```

Policy:

- Use rendered PNG pages as the review source of truth.
- Do not use `pdftotext`, OCR, or other deterministic text extraction for exam question capture in this workflow.
- Keep human review between evaluation/synthesis and any later snippet-content implementation round.
