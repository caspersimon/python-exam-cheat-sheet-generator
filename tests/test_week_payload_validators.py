import json
from pathlib import Path
import unittest

from pipelines.study_database.validators import analyze_week_payload, missing_source_paths


class WeekPayloadValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.template = json.loads((cls.root / "data" / "templates" / "week_template.json").read_text(encoding="utf-8"))

    def test_template_payload_has_no_hard_errors(self) -> None:
        issues = analyze_week_payload(self.template)
        self.assertEqual([], issues["errors"])

    def test_duplicate_notebook_cell_indexes_are_rejected(self) -> None:
        payload = {
            "week": 8,
            "lecture": {
                "concepts": [{"topic": "loops", "explanation": "for loops"}],
                "lecture_questions": [],
            },
            "notebook_cells": [
                {"cell_index": 1, "cell_type": "code", "source": "print('a')"},
                {"cell_index": 1, "cell_type": "code", "source": "print('b')"},
            ],
            "sources": [],
        }
        issues = analyze_week_payload(payload)
        self.assertTrue(any("Duplicate notebook cell_index" in message for message in issues["errors"]))

    def test_question_correct_must_exist_in_options(self) -> None:
        payload = {
            "week": 6,
            "lecture": {
                "concepts": [{"topic": "slicing", "explanation": "slice basics"}],
                "lecture_questions": [
                    {
                        "question": "What does x[0] return?",
                        "options": {"a": "first", "b": "last"},
                        "correct": "d",
                    }
                ],
            },
            "notebook_cells": [],
            "sources": [],
        }
        issues = analyze_week_payload(payload)
        self.assertTrue(any("is not present in options" in message for message in issues["errors"]))

    def test_missing_source_paths_are_reported(self) -> None:
        payload = {
            "week": 9,
            "lecture": {"concepts": [{"topic": "dict", "explanation": "maps"}], "lecture_questions": []},
            "notebook_cells": [],
            "sources": [
                "materials/lectures/Lecture Week 1.md",
                "materials/lectures/Lecture Week 999.md",
            ],
        }
        missing = missing_source_paths(payload, root_dir=self.root)
        self.assertEqual(["materials/lectures/Lecture Week 999.md"], missing)


if __name__ == "__main__":
    unittest.main()
