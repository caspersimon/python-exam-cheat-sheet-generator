from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from pipelines import vision_exam_pipeline as pipeline


class VisionExamPipelineTests(unittest.TestCase):
    def test_duplicate_aliases_keep_canonical_exam_set_unique(self) -> None:
        aliases = pipeline.duplicate_exam_aliases()
        canonical_ids = {exam["exam_id"] for exam in pipeline.unique_exam_sources()}
        self.assertTrue(aliases)
        self.assertEqual(7, len(canonical_ids))
        self.assertNotIn(aliases[0]["exam_id"], canonical_ids)
        self.assertIn(aliases[0]["duplicate_of"], canonical_ids)

    def test_completeness_report_marks_blocked_questions_incomplete(self) -> None:
        report = pipeline.build_completeness_report(
            {
                "schema_version": "1.0",
                "exams": [
                    {
                        "exam_id": "demo-exam",
                        "title": "Demo Exam",
                        "expected_questions": 2,
                        "questions": [
                            {
                                "question_id": "demo-exam-q01",
                                "number": 1,
                                "provenance": {"human_confirmed": True},
                            }
                        ],
                        "blocked_questions": [
                            {
                                "question_id": "demo-exam-q02",
                                "number": 2,
                                "status": "pending_vision_review",
                                "reason": "Not reviewed yet.",
                            }
                        ],
                    }
                ],
            }
        )
        self.assertEqual("incomplete", report["overall_status"])
        self.assertEqual(1, report["summary"]["incomplete_exam_count"])

    def test_completeness_report_allows_unconfirmed_but_fully_captured_exam(self) -> None:
        report = pipeline.build_completeness_report(
            {
                "schema_version": "1.0",
                "exams": [
                    {
                        "exam_id": "demo-exam",
                        "title": "Demo Exam",
                        "expected_questions": 2,
                        "questions": [
                            {
                                "question_id": "demo-exam-q01",
                                "number": 1,
                                "provenance": {"human_confirmed": False},
                            },
                            {
                                "question_id": "demo-exam-q02",
                                "number": 2,
                                "provenance": {"human_confirmed": False},
                            },
                        ],
                        "blocked_questions": [],
                    }
                ],
            }
        )
        self.assertEqual("complete", report["overall_status"])
        self.assertEqual(1, report["summary"]["complete_exam_count"])
        self.assertEqual(0, report["summary"]["incomplete_exam_count"])
        self.assertEqual(0, report["exams"][0]["human_confirmed_questions"])

    def test_build_evaluation_scaffold_preserves_existing_completed_review(self) -> None:
        question_bank = {
            "schema_version": "1.0",
            "exams": [
                {
                    "exam_id": "demo-exam",
                    "questions": [
                        {
                            "question_id": "demo-exam-q01",
                            "number": 1,
                            "topic": "Loops",
                            "question": "What prints?",
                            "options": {"a": "1", "b": "2"},
                            "correct": "a",
                            "explanation": "Because.",
                            "code_context": "print(1)",
                            "provenance": {"review_status": "human_confirmed"},
                        }
                    ],
                    "blocked_questions": [],
                }
            ],
        }
        selectable_items = [{"item_id": "snippet-1", "week": 2}]
        existing = {
            "questions": [
                {
                    "evaluation_id": "round1:demo-exam-q01",
                    "question_id": "demo-exam-q01",
                    "status": "completed",
                    "best_single_snippet": {"item_id": "snippet-1", "why": "Exact match"},
                    "top_three_snippets": [{"item_id": "snippet-1", "why": "Only item"}],
                    "minimal_sufficient_snippets": [{"item_id": "snippet-1", "why": "Enough"}],
                    "answerability": {"status": "fully_answerable"},
                    "gap_analysis": {"summary": ""},
                    "suggested_changes": [],
                    "review_meta": {"reviewed_at": "2026-03-23T10:00:00Z"},
                }
            ]
        }
        payload = pipeline.build_evaluation_scaffold(
            round_name="round1",
            question_bank=question_bank,
            selectable_items=selectable_items,
            existing_payload=existing,
            findings_paths=[],
        )
        question = payload["questions"][0]
        self.assertEqual("completed", question["status"])
        self.assertEqual("snippet-1", question["best_single_snippet"]["item_id"])
        self.assertEqual("2026-03-23T10:00:00Z", question["review_meta"]["reviewed_at"])

    def test_build_evaluation_scaffold_marks_missing_question_capture_as_blocked(self) -> None:
        question_bank = {
            "schema_version": "1.0",
            "exams": [
                {
                    "exam_id": "demo-exam",
                    "questions": [],
                    "blocked_questions": [
                        {
                            "question_id": "demo-exam-q02",
                            "number": 2,
                            "status": "pending_vision_review",
                            "reason": "Need page review.",
                        }
                    ],
                }
            ],
        }
        payload = pipeline.build_evaluation_scaffold(
            round_name="round1",
            question_bank=question_bank,
            selectable_items=[],
            existing_payload=None,
            findings_paths=[],
        )
        question = payload["questions"][0]
        self.assertEqual("blocked_missing_question_capture", question["status"])
        self.assertIn("Need page review.", question["gap_analysis"]["summary"])

    def test_build_evaluation_scaffold_marks_agent_captured_questions_as_pending_confirmation(self) -> None:
        question_bank = {
            "schema_version": "1.0",
            "exams": [
                {
                    "exam_id": "demo-exam",
                    "questions": [
                        {
                            "question_id": "demo-exam-q01",
                            "number": 1,
                            "topic": "demo",
                            "question": "What is 1 + 1?",
                            "options": {"a": "2"},
                            "correct": "a",
                            "explanation": "Basic arithmetic.",
                            "provenance": {"review_status": "agent_reviewed_pending_human_confirmation"},
                        }
                    ],
                    "blocked_questions": [],
                }
            ],
        }
        existing_payload = {
            "questions": [
                {
                    "question_id": "demo-exam-q01",
                    "status": "blocked_missing_question_capture",
                }
            ]
        }
        payload = pipeline.build_evaluation_scaffold(
            round_name="round1",
            question_bank=question_bank,
            selectable_items=[],
            existing_payload=existing_payload,
            findings_paths=[],
        )
        question = payload["questions"][0]
        self.assertEqual("captured_pending_human_confirmation", question["status"])
        self.assertIn("awaiting human confirmation", question["gap_analysis"]["summary"])

    def test_validate_evaluation_payload_rejects_unknown_snippet_ids(self) -> None:
        errors = pipeline.validate_evaluation_payload(
            {
                "questions": [
                    {
                        "question_id": "demo-exam-q01",
                        "status": "completed",
                        "best_single_snippet": {"item_id": "missing-snippet"},
                        "top_three_snippets": [],
                        "minimal_sufficient_snippets": [],
                        "suggested_changes": [],
                    }
                ]
            },
            selectable_items=[{"item_id": "snippet-1"}],
        )
        self.assertTrue(errors)
        self.assertIn("missing-snippet", errors[0])

    def test_build_ranking_analytics_tracks_week_counts_and_comparison(self) -> None:
        evaluation_payload = {
            "questions": [
                {
                    "question_id": "q1",
                    "status": "completed",
                    "answerability": {"status": "fully_answerable"},
                    "best_single_snippet": {"item_id": "snippet-1"},
                    "top_three_snippets": [{"item_id": "snippet-1"}, {"item_id": "snippet-2"}],
                    "minimal_sufficient_snippets": [{"item_id": "snippet-2"}],
                },
                {
                    "question_id": "q2",
                    "status": "pending_review",
                    "answerability": {"status": "unknown"},
                    "best_single_snippet": None,
                    "top_three_snippets": [],
                    "minimal_sufficient_snippets": [],
                },
            ]
        }
        baseline_payload = {
            "questions": [
                {
                    "question_id": "q1",
                    "status": "completed",
                    "answerability": {"status": "partial"},
                    "best_single_snippet": {"item_id": "snippet-1"},
                    "top_three_snippets": [],
                    "minimal_sufficient_snippets": [],
                }
            ]
        }
        selectable_items = [
            {"item_id": "snippet-1", "week": 1},
            {"item_id": "snippet-2", "week": 1},
            {"item_id": "snippet-3", "week": 2},
        ]
        analytics, markdown = pipeline.build_ranking_analytics(
            round_name="round2",
            evaluation_payload=evaluation_payload,
            selectable_items=selectable_items,
            baseline_payload=baseline_payload,
        )
        self.assertEqual(1, analytics["summary"]["completed_evaluations"])
        self.assertEqual(1, analytics["weeks"][0]["top1_unique_snippets"])
        self.assertEqual(1, analytics["comparison"]["fully_answerable"]["delta"])
        self.assertIn("Week Summary", markdown)

    def test_validate_question_bank_payload_requires_reasoned_blocked_slots(self) -> None:
        errors = pipeline.validate_question_bank_payload(
            {
                "schema_version": "1.0",
                "exams": [
                    {
                        "exam_id": "demo-exam",
                        "expected_questions": 1,
                        "questions": [],
                        "blocked_questions": [{"question_id": "demo-exam-q01", "number": 1, "status": "pending_vision_review"}],
                    }
                ],
            }
        )
        self.assertTrue(errors)
        self.assertIn("missing a reason", errors[0])

    def test_write_extraction_packets_tracks_captured_and_pending_questions(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            question_bank_path = Path(tmp) / "exam_question_bank.json"
            output_dir = Path(tmp) / "packets"
            question_bank_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "exams": [
                            {
                                "exam_id": "demo-exam",
                                "title": "Demo Exam",
                                "expected_questions": 2,
                                "pdf_path": "demo.pdf",
                                "page_image_paths": ["tmp/demo/page-01.png"],
                                "questions": [{"question_id": "demo-exam-q01", "number": 1}],
                                "blocked_questions": [
                                    {
                                        "question_id": "demo-exam-q02",
                                        "number": 2,
                                        "status": "pending_vision_review",
                                        "reason": "Need capture.",
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            index = pipeline.write_extraction_packets(question_bank_path=question_bank_path, output_dir=output_dir)

        self.assertEqual(1, index["packet_count"])
        self.assertEqual(1, index["packets"][0]["captured_questions"])
        self.assertEqual(1, index["packets"][0]["pending_questions"])

    def test_merge_review_drop_promotes_blocked_question_into_question_bank(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            question_bank_path = Path(tmp) / "exam_question_bank.json"
            review_drop_path = Path(tmp) / "review_drop.json"
            question_bank_path.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "exams": [
                            {
                                "exam_id": "demo-exam",
                                "title": "Demo Exam",
                                "expected_questions": 1,
                                "questions": [],
                                "blocked_questions": [
                                    {
                                        "question_id": "demo-exam-q01",
                                        "number": 1,
                                        "status": "pending_vision_review",
                                        "reason": "Need capture.",
                                    }
                                ],
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            review_drop_path.write_text(
                json.dumps(
                    {
                        "exam_id": "demo-exam",
                        "question_updates": [
                            {
                                "number": 1,
                                "topic": "Loops",
                                "question": "What prints?",
                                "options": {"a": "1", "b": "2"},
                                "correct": "a",
                                "explanation": "Because.",
                                "provenance": {"page_refs": ["tmp/page-01.png"]},
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            merged_exam = pipeline.merge_review_drop(review_drop_path=review_drop_path, question_bank_path=question_bank_path)

        self.assertEqual(1, merged_exam["review_tracking"]["present_questions"])
        self.assertEqual(0, merged_exam["review_tracking"]["blocked_questions"])
        self.assertEqual("Loops", merged_exam["questions"][0]["topic"])


if __name__ == "__main__":
    unittest.main()
