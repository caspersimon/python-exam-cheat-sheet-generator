from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts import validate_extracted_material as extracted


class ExtractedMaterialValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.script = cls.root / "scripts" / "validate_extracted_material.py"

    def _run_cli(self, payload: dict, *, kind: str = "bundle") -> subprocess.CompletedProcess[str]:
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = Path(temp_dir.name)
        payload_path = temp_path / "payload.json"
        report_path = temp_path / "report.json"
        payload_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        result = subprocess.run(
            [
                sys.executable,
                str(self.script),
                "--kind",
                kind,
                "--input",
                str(payload_path),
                "--report-file",
                str(report_path),
            ],
            cwd=self.root,
            capture_output=True,
            text=True,
        )
        result.report_path = report_path  # type: ignore[attr-defined]
        result._temp_dir = temp_dir  # type: ignore[attr-defined]
        self.addCleanup(temp_dir.cleanup)
        return result

    def test_week_payload_validates_clean_agent_output(self) -> None:
        payload = {
            "week": 4,
            "topics": ["strings", "methods"],
            "lecture": {
                "concepts": [
                    {
                        "topic": "string methods",
                        "explanation": "String methods are used to transform text.",
                        "code_examples": [{"description": "capitalize", "code": "s = 'abc'\nprint(s.capitalize())"}],
                    }
                ],
                "lecture_questions": [
                    {
                        "question": "What does capitalize return?",
                        "options": {"a": "ABC", "b": "Abc"},
                        "correct": "b",
                        "explanation": "Only the first letter changes.",
                    }
                ],
            },
            "notebook_cells": [
                {
                    "cell_index": 1,
                    "cell_type": "code",
                    "topic": "string methods",
                    "source": "print('hello'.upper())",
                }
            ],
            "sources": ["materials/lectures/Lecture Week 4.pptx"],
        }

        report = extracted.validate_week_payload(payload)
        self.assertEqual([], report["errors"], msg=str(report))
        result = self._run_cli(payload, kind="week")
        self.assertEqual(0, result.returncode)
        self.assertTrue(result.report_path.exists())

    def test_week_payload_rejects_bad_python_code(self) -> None:
        payload = {
            "week": 4,
            "lecture": {
                "concepts": [
                    {
                        "topic": "strings",
                        "explanation": "example",
                        "code_examples": [{"description": "broken", "code": "for x in range(3)\n    print(x)"}],
                    }
                ],
                "lecture_questions": [],
            },
            "notebook_cells": [
                {"cell_index": 1, "cell_type": "code", "topic": "broken", "source": "if True print('oops')"}
            ],
            "sources": [],
        }

        report = extracted.validate_week_payload(payload)
        self.assertTrue(report["errors"], msg="Expected syntax errors to be reported.")
        result = self._run_cli(payload, kind="week")
        self.assertNotEqual(0, result.returncode)
        self.assertTrue(result.report_path.exists())

    def test_exam_payload_rejects_invalid_correct_option(self) -> None:
        payload = {
            "exams": [
                {
                    "exam_label": "trial-final",
                    "questions": [
                        {
                            "number": 1,
                            "question": "Which line prints the result?",
                            "options": {"a": "print(1)", "b": "print(2)"},
                            "correct": "c",
                            "explanation": "The correct letter is missing from options.",
                        }
                    ],
                }
            ]
        }

        report = extracted.validate_exam_payload(payload)
        self.assertTrue(report["errors"], msg="Expected invalid correct option to be rejected.")
        result = self._run_cli(payload, kind="exam")
        self.assertNotEqual(0, result.returncode)
        self.assertTrue(result.report_path.exists())
        self.assertIn("correct", result.stdout.lower() + result.stderr.lower())

    def test_bundle_payload_validates_week_and_exam_sections_together(self) -> None:
        payload = {
            "week": 6,
            "topics": ["loops"],
            "lecture": {
                "concepts": [
                    {
                        "topic": "while loops",
                        "explanation": "Repeat until a condition changes.",
                        "code_examples": [{"description": "loop", "code": "while x < 3:\n    x += 1"}],
                    }
                ],
                "lecture_questions": [],
            },
            "notebook_cells": [
                {"cell_index": 1, "cell_type": "code", "topic": "loops", "source": "for i in range(3):\n    print(i)"},
            ],
            "exams": [
                {
                    "exam_label": "trial-final",
                    "questions": [
                        {
                            "number": 1,
                            "question": "What is printed?",
                            "options": {"a": "1", "b": "2"},
                            "correct": "a",
                            "explanation": "The first option is correct.",
                        }
                    ],
                }
            ],
            "sources": ["materials/lectures/Lecture Week 6.pptx"],
        }

        report = extracted.validate_payload(payload, kind="bundle")
        self.assertEqual([], report["errors"], msg=str(report))


if __name__ == "__main__":
    unittest.main()
