# Vision Pipeline Runbook

Start here if you are operating the current snippet-completeness round from inside `data/vision_exam_pipeline/`.

## Read In This Order

1. [OVERNIGHT_EXECUTION_BOARD.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/OVERNIGHT_EXECUTION_BOARD.md)
2. [plan_after_manual_synthesis.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/plan_after_manual_synthesis.md)
3. [round1_manual_synthesis.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/data/vision_exam_pipeline/review_packets/round1_manual_synthesis.md)
4. [SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/docs/curation/SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md)
5. [OVERNIGHT_AGENT_RUNBOOK.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/docs/curation/OVERNIGHT_AGENT_RUNBOOK.md)
6. [VISION_EXAM_PIPELINE.md](/Users/juliuseikmans/Desktop/Studies/2025-2026/intro%20to%20python/python-exam-cheat-sheet-generator/docs/VISION_EXAM_PIPELINE.md)

## Quick State Check

```bash
python3 scripts/vision_exam_pipeline.py status --round round1
```

## Current Priority

Improve snippet completeness.

Do not:

- start the topic-first UI refactor
- aggressively prune the corpus before the next grading pass
- cross the human review gates automatically

## Canonical Validation

Before handoff or after integrating meaningful work:

```bash
make leave-better
```
