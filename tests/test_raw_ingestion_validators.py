import unittest

from pipelines.study_database.validators import analyze_assessment_payload, normalize_assessment_payload


class RawIngestionValidatorTests(unittest.TestCase):
    def test_assessment_payload_validator_accepts_valid_payload(self) -> None:
        payload = {
            "exam_label": "trial_final",
            "source": "materials/exams/trial final.pdf",
            "year": "2024",
            "questions": [
                {
                    "number": 1,
                    "topic": "basics",
                    "question": "Which line prints 1?",
                    "options": {"a": "print(1)", "b": "print(2)"},
                    "correct": "a",
                    "explanation": "Option a prints 1.",
                }
            ],
            "notes": ["cleaned from pdf"],
        }
        issues = analyze_assessment_payload(payload)
        self.assertEqual([], issues["errors"])

    def test_assessment_payload_validator_rejects_bad_correct_answer(self) -> None:
        payload = {
            "exam_label": "trial_final",
            "source": "materials/exams/trial final.pdf",
            "year": "unknown",
            "questions": [
                {
                    "number": 1,
                    "question": "Which line prints 1?",
                    "options": {"a": "print(1)", "b": "print(2)"},
                    "correct": "c",
                }
            ],
            "notes": [],
        }
        issues = analyze_assessment_payload(payload)
        self.assertTrue(any("is not present in options" in message for message in issues["errors"]))

    def test_assessment_normalization_fills_default_year(self) -> None:
        normalized = normalize_assessment_payload(
            {
                "exam_label": "sample_final",
                "source": "materials/exams/sample.pdf",
                "questions": [],
            }
        )
        self.assertEqual("unknown", normalized["year"])
        self.assertEqual("sample_final", normalized["exam_label"])


if __name__ == "__main__":
    unittest.main()
