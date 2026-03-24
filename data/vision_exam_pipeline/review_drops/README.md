# Review Drops

Agents doing vision-only exam capture should write one JSON file per batch here, then merge it with:

```bash
python3 scripts/vision_exam_pipeline.py merge-review-drop --input data/vision_exam_pipeline/review_drops/<file>.json
```

Contract:

```json
{
  "exam_id": "introduction-to-python-trial-final-exam-solutions-py22",
  "question_updates": [
    {
      "number": 8,
      "topic": "short topic label",
      "question": "full question text",
      "options": {
        "a": "option text",
        "b": "option text",
        "c": "option text",
        "d": "option text"
      },
      "correct": "a",
      "explanation": "brief explanation of why the answer is correct",
      "code_context": "optional code block or empty string",
      "provenance": {
        "review_status": "agent_reviewed_pending_human_confirmation",
        "review_pass": 1,
        "human_confirmed": false,
        "page_refs": [
          "tmp/exam_coverage_audit/pages/<exam-id>/page-08.png"
        ],
        "notes": [
          "Reviewed from rendered PNG pages only."
        ]
      }
    }
  ]
}
```

Rules:

- Use only rendered PNG pages as source material.
- Do not use OCR, `pdftotext`, or any deterministic text extraction.
- Keep question numbering exact.
- Preserve answer options faithfully.
- Leave `code_context` empty when there is no meaningful code block to preserve.
