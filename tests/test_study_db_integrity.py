import json
from pathlib import Path
import unittest

from pipelines.shared import flatten_study_db_for_pipeline


class StudyDatabaseIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.root = Path(__file__).resolve().parents[1]
        cls.db_path = cls.root / "data" / "study_db.json"
        with cls.db_path.open("r", encoding="utf-8") as handle:
            cls.db = json.load(handle)
        cls.materialized = flatten_study_db_for_pipeline(cls.db)

    def test_top_level_sections_exist(self) -> None:
        for key in ["meta", "weeks", "assessments", "knowledge"]:
            self.assertIn(key, self.db)

    def test_week_numbers_are_unique_and_sorted(self) -> None:
        weeks = [int(item["week"]) for item in self.db["weeks"]]
        self.assertEqual(weeks, sorted(weeks))
        self.assertEqual(len(weeks), len(set(weeks)))

    def test_week_structure(self) -> None:
        for week in self.db["weeks"]:
            self.assertIsInstance(week.get("topics"), list)
            lecture = week.get("lecture")
            self.assertIsInstance(lecture, dict)
            self.assertIsInstance(lecture.get("concepts"), list)
            self.assertIsInstance(lecture.get("lecture_questions"), list)
            self.assertIsInstance(week.get("notebook_cells"), list)
            self.assertIsInstance(week.get("sources"), list)

    def test_materialized_shape_is_compatible_with_pipelines(self) -> None:
        for key in ["meta", "lectures", "notebooks", "exams", "key_exam_patterns_and_traps", "topic_analysis"]:
            self.assertIn(key, self.materialized)
        self.assertIsInstance(self.materialized["lectures"], list)
        self.assertIsInstance(self.materialized["notebooks"], list)
        self.assertIsInstance(self.materialized["exams"], list)

    def test_material_sources_exist(self) -> None:
        for source in self.db.get("meta", {}).get("sources", []):
            if not isinstance(source, str) or not source.strip():
                continue
            path = self.root / source
            self.assertTrue(path.exists(), f"Missing source file listed in db meta.sources: {source}")


if __name__ == "__main__":
    unittest.main()
