from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from pipelines import vision_exam_pipeline_batch as batch


class VisionExamPipelineBatchTests(unittest.TestCase):
    def test_evaluation_progress_summary_counts_remaining_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "round2.json"
            path.write_text(
                json.dumps(
                    {
                        "generated_at": "2026-03-24T08:00:00Z",
                        "questions": [
                            {"question_id": "q1", "status": "completed"},
                            {"question_id": "q2", "status": "captured_pending_human_confirmation"},
                            {"question_id": "q3", "status": "blocked_missing_question_capture"},
                            {"question_id": "q4", "status": "pending_review"},
                        ],
                    }
                ),
                encoding="utf-8",
            )
            summary = batch.evaluation_progress_summary(round_name="round2", evaluation_path=path)

        self.assertEqual(4, summary["total_questions"])
        self.assertEqual(1, summary["completed_questions"])
        self.assertEqual(1, summary["blocked_questions"])
        self.assertEqual(2, summary["remaining_questions"])
        self.assertEqual("2026-03-24T08:00:00Z", summary["generated_at"])


if __name__ == "__main__":
    unittest.main()
