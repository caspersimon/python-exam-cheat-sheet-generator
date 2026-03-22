import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from pipelines.study_database.raw_ingestion import ingest_raw_materials
from pipelines.study_database.raw_sources import RawSourceRecord


class RawIngestionPipelineTests(unittest.TestCase):
    def test_ingestion_writes_week_and_assessment_artifacts(self) -> None:
        records = [
            RawSourceRecord(
                path=Path("/tmp/Lecture Week 4.pptx"),
                relative_path="Lecture Week 4.pptx",
                kind="pptx",
                role="lecture",
                week=4,
                text="Slide 1: string methods",
            ),
            RawSourceRecord(
                path=Path("/tmp/Exercise_4.1.py"),
                relative_path="Exercise_4.1.py",
                kind="py",
                role="exercise",
                week=4,
                text="Write a function called main",
            ),
            RawSourceRecord(
                path=Path("/tmp/OOP.py"),
                relative_path="OOP.py",
                kind="py",
                role="unknown",
                week=None,
                text="class Vehicle: pass",
            ),
            RawSourceRecord(
                path=Path("/tmp/Sample Final plus answers.pdf"),
                relative_path="Sample Final plus answers.pdf",
                kind="pdf",
                role="assessment",
                week=None,
                text="Question 1 ...",
            ),
        ]

        def fake_run_json_agent(prompt: str, *, model: str = "test-model", timeout_seconds: int = 0):
            if "unassigned_files" in prompt:
                return {
                    "assignments": [
                        {
                            "path": "OOP.py",
                            "bucket": "week",
                            "week": 4,
                            "role": "supporting",
                            "reason": "Matches the object-oriented exercises for week 4.",
                        }
                    ],
                    "notes": ["assigned support file"],
                }
            if '"exam_label": "short stable label"' in prompt:
                return {
                    "exam_label": "sample_final_plus_answers",
                    "source": "Sample Final plus answers.pdf",
                    "year": "2024",
                    "questions": [
                        {
                            "number": 1,
                            "topic": "oop",
                            "question": "What does the constructor do?",
                            "options": {"a": "Creates object", "b": "Deletes object"},
                            "correct": "a",
                            "explanation": "It creates an object.",
                            "code_context": "class A:\n    pass",
                        }
                    ],
                    "notes": ["cleaned pdf"],
                }
            return {
                "week": 4,
                "topics": ["objects", "oop"],
                "lecture": {
                    "concepts": [
                        {
                            "topic": "Objects",
                            "explanation": "Objects hold state.",
                            "code_examples": [{"description": "class skeleton", "code": "class A:\n    pass"}],
                        }
                    ],
                    "lecture_questions": [
                        {
                            "topic": "Objects",
                            "question": "What does class A do?",
                            "options": {"a": "Defines a class", "b": "Runs code"},
                            "correct": "a",
                            "explanation": "It defines a class.",
                        }
                    ],
                },
                "notebook_cells": [
                    {
                        "cell_index": 1,
                        "cell_type": "code",
                        "topic": "Objects",
                        "is_advanced_optional": False,
                        "source": "class A:\n    pass",
                        "outputs": [],
                    }
                ],
                "sources": ["Lecture Week 4.pptx", "Exercise_4.1.py", "OOP.py"],
                "review_notes": ["week bundle okay"],
            }

        with tempfile.TemporaryDirectory() as tmp:
            output_dir = Path(tmp) / "out"
            with patch("pipelines.study_database.raw_ingestion.collect_raw_source_records", return_value=records), patch(
                "pipelines.study_database.raw_ingestion.run_json_agent", side_effect=fake_run_json_agent
            ):
                report = ingest_raw_materials(Path(tmp), output_dir=output_dir, model="test-model", write_payloads=True)

            self.assertEqual(1, report["summary"]["week_count"])
            self.assertEqual(1, report["summary"]["assessment_count"])
            self.assertEqual(2, report["summary"]["artifact_count"])
            self.assertIn("OOP.py", report["week_sources"]["4"])

            week_payload = json.loads((output_dir / "week-04" / "payload.json").read_text(encoding="utf-8"))
            self.assertEqual(4, week_payload["week"])
            self.assertEqual("Objects", week_payload["lecture"]["concepts"][0]["topic"])

            assessment_payload = json.loads((output_dir / "assessment-sample-final-plus-answers" / "payload.json").read_text(encoding="utf-8"))
            self.assertEqual("sample_final_plus_answers", assessment_payload["exam_label"])
            self.assertEqual("Sample Final plus answers.pdf", assessment_payload["source"])

            self.assertTrue(any("assigned support file" in warning for warning in report["warnings"]))


if __name__ == "__main__":
    unittest.main()
