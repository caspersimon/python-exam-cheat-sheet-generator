from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from pipelines import vision_exam_pipeline as pipeline
from pipelines import vision_exam_pipeline_status as pipeline_status


class VisionExamPipelineFollowupTests(unittest.TestCase):
    def test_build_review_packet_surfaces_themes_and_top_snippets(self) -> None:
        synthesis_payload = {
            "suggestions": [
                {
                    "suggestion_id": "round1:1",
                    "proposal": "Add a snippet explaining string slicing and split().",
                    "pros": ["Helps with string parsing questions."],
                    "cons": [],
                    "recommended_direction": "add_this",
                    "source_exams": ["exam-a"],
                },
                {
                    "suggestion_id": "round1:2",
                    "proposal": "Create a datetime cheat-sheet snippet using strptime and timedelta.",
                    "pros": ["Reduces guessing on datetime questions."],
                    "cons": [],
                    "recommended_direction": "add_this",
                    "source_exams": ["exam-b"],
                },
            ]
        }
        analytics_payload = {
            "weeks": [
                {
                    "week": 4,
                    "top1_unique_snippets": 2,
                    "top3_unique_snippets": 4,
                    "minimal_set_unique_snippets": 3,
                    "minimal_set_unused_snippets": 1,
                }
            ]
        }
        evaluation_payload = {
            "questions": [
                {
                    "question_id": "q1",
                    "exam_id": "exam-a",
                    "status": "completed",
                    "answerability": {"status": "partial"},
                    "gap_analysis": {
                        "summary": "Student needs string indexing and split rules.",
                        "missing_concepts": ["string slicing"],
                        "proposed_fix": "Add a string methods summary snippet.",
                    },
                    "best_single_snippet": {"item_id": "snippet-1"},
                    "top_three_snippets": [{"item_id": "snippet-1"}],
                    "minimal_sufficient_snippets": [{"item_id": "snippet-1"}],
                },
                {
                    "question_id": "q2",
                    "exam_id": "exam-b",
                    "status": "completed",
                    "answerability": {"status": "insufficient"},
                    "gap_analysis": {
                        "summary": "Student lacks datetime parsing rules.",
                        "missing_concepts": ["datetime.strptime"],
                        "proposed_fix": "Add a datetime and timedelta summary card.",
                    },
                    "best_single_snippet": {"item_id": "snippet-2"},
                    "top_three_snippets": [{"item_id": "snippet-2"}],
                    "minimal_sufficient_snippets": [{"item_id": "snippet-2"}],
                },
            ]
        }
        selectable_items = [
            {"item_id": "snippet-1", "week": 4, "topic": "Strings", "bucket": "recommended", "item_type": "source_exam", "search_text": "String slicing and split example."},
            {"item_id": "snippet-2", "week": 6, "topic": "Datetime", "bucket": "recommended", "item_type": "source_exam", "search_text": "Datetime parsing example."},
        ]

        packet, markdown = pipeline.build_review_packet(
            round_name="round1",
            synthesis_payload=synthesis_payload,
            analytics_payload=analytics_payload,
            evaluation_payload=evaluation_payload,
            selectable_items=selectable_items,
        )

        self.assertEqual(2, packet["summary"]["completed_evaluations"])
        theme_names = {theme["theme_name"] for theme in packet["themes"]}
        self.assertIn("Strings, Indexing, and Text Methods", theme_names)
        self.assertIn("Datetime and Timedelta", theme_names)
        self.assertTrue(packet["top_existing_snippets"])
        self.assertIn("Recommended Review Order", markdown)
        self.assertIn("Strong Existing Snippets", markdown)

    def test_build_pipeline_status_summarizes_current_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            question_bank_path = tmp_root / "exam_question_bank.json"
            completeness_path = tmp_root / "exam_question_bank_completeness.json"
            evaluations_dir = tmp_root / "evaluations"
            synthesis_dir = tmp_root / "synthesis"
            analytics_dir = tmp_root / "analytics"
            review_packets_dir = tmp_root / "review_packets"

            question_bank_path.write_text(
                json.dumps(
                    {
                        "canonical_exam_count": 1,
                        "exams": [
                            {
                                "exam_id": "demo-exam",
                                "questions": [
                                    {
                                        "question_id": "demo-exam-q01",
                                        "number": 1,
                                        "provenance": {"review_status": "agent_reviewed_pending_human_confirmation"},
                                    }
                                ],
                                "blocked_questions": [],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            completeness_path.write_text(json.dumps({"overall_status": "complete"}), encoding="utf-8")
            evaluations_dir.mkdir()
            synthesis_dir.mkdir()
            analytics_dir.mkdir()
            review_packets_dir.mkdir()
            (evaluations_dir / "round1.json").write_text(
                json.dumps(
                    {
                        "questions": [
                            {
                                "question_id": "demo-exam-q01",
                                "status": "completed",
                                "answerability": {"status": "certain"},
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (synthesis_dir / "round1.json").write_text(json.dumps({"summary": {"suggestion_count": 3}}), encoding="utf-8")
            (analytics_dir / "round1.json").write_text(json.dumps({"summary": {"completed_evaluations": 1}}), encoding="utf-8")
            (review_packets_dir / "round1.json").write_text(json.dumps({"summary": {"theme_count": 2}}), encoding="utf-8")
            (review_packets_dir / "round1_manual_synthesis.md").write_text("# manual\n", encoding="utf-8")

            with mock.patch.object(pipeline_status, "QUESTION_BANK_FILE", question_bank_path), \
                mock.patch.object(pipeline_status, "COMPLETENESS_FILE", completeness_path), \
                mock.patch.object(pipeline_status, "EVALUATIONS_DIR", evaluations_dir), \
                mock.patch.object(pipeline_status, "SYNTHESIS_DIR", synthesis_dir), \
                mock.patch.object(pipeline_status, "ANALYTICS_DIR", analytics_dir), \
                mock.patch.object(pipeline_status, "REVIEW_PACKET_DIR", review_packets_dir):
                status = pipeline.build_pipeline_status(round_name="round1")

        self.assertEqual("complete", status["question_bank"]["completeness_status"])
        self.assertEqual(1, status["evaluation_round"]["completed_evaluations"])
        self.assertEqual("human_review_of_synthesized_changes", status["next_gate"])
        self.assertTrue(status["review_outputs"]["manual_review_packet_exists"])


if __name__ == "__main__":
    unittest.main()
