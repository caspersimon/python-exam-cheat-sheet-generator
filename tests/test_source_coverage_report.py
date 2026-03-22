import json
import unittest
from pathlib import Path


class SourceCoverageReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[1]
        with (root / "data" / "quality" / "source_coverage_report.json").open("r", encoding="utf-8") as handle:
            cls.report = json.load(handle)
        with (root / "data" / "study_db.json").open("r", encoding="utf-8") as handle:
            cls.study_db = json.load(handle)

    def test_report_has_expected_top_level_shape(self) -> None:
        self.assertIsInstance(self.report.get("meta"), dict)
        self.assertIsInstance(self.report.get("units"), list)
        self.assertGreater(self.report["meta"].get("total_units", 0), 0)
        self.assertEqual(self.report["meta"].get("uncovered_units"), 0)

    def test_all_units_are_marked_covered(self) -> None:
        uncovered = [unit["unit_id"] for unit in self.report["units"] if unit.get("coverage_status") != "covered"]
        self.assertEqual(uncovered, [], f"Expected all source units to be covered, found: {uncovered[:10]}")

    def test_units_have_required_fields(self) -> None:
        required = {
            "unit_id",
            "source_file",
            "source_kind",
            "question_or_exercise_number",
            "prompt",
            "code_context",
            "answer_or_explanation",
            "week",
            "topic",
            "subtopic",
            "pattern_tags",
            "coverage_targets",
            "coverage_status",
            "compression_type",
        }
        for unit in self.report["units"]:
            self.assertTrue(required.issubset(unit), f"Missing fields in coverage unit {unit.get('unit_id')}")
            self.assertIsInstance(unit.get("coverage_targets"), dict)
            self.assertIsInstance(unit["coverage_targets"].get("item_ids"), list)

    def test_old_midterm_counts_match_rebuilt_sources(self) -> None:
        counts = {
            exam.get("source"): len(exam.get("questions", []))
            for exam in self.study_db.get("assessments", {}).get("exams", [])
        }
        self.assertEqual(counts.get("materials/exams/trial midterm.pdf"), 24)
        self.assertEqual(counts.get("materials/exams/2023.pdf"), 16)
        self.assertEqual(counts.get("materials/exams/2024.pdf"), 24)

    def test_missing_practice_exam_is_now_present(self) -> None:
        sources = {exam.get("source") for exam in self.study_db.get("assessments", {}).get("exams", [])}
        self.assertIn(
            "materials/post_midterm/practice_exams_previous_years/final-exam-solutions-for-python-programming-62oop21.pdf",
            sources,
        )


if __name__ == "__main__":
    unittest.main()
