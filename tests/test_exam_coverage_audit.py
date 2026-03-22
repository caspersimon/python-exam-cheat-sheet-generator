import unittest

from scripts.exam_coverage_audit import EXAM_SOURCES, iter_selectable_items, unique_exam_sources


class ExamCoverageAuditTests(unittest.TestCase):
    def test_iter_selectable_items_excludes_ai_summary_and_keeps_detail_ids(self) -> None:
        cards = [
            {
                "id": "card-1",
                "topic": "Demo Topic",
                "sections": {
                    "ai_summary": {"content": "Useful but not selectable."},
                    "ai_common_questions": {"items": [{"id": "aiq-1", "summary": "What is x?"}]},
                    "key_points_to_remember": [
                        {
                            "id": "kp-1",
                            "text": "Names bind to objects.",
                            "details": [{"id": "kp-1-d1", "title": "Example", "code": "x = 1"}],
                        }
                    ],
                    "ai_examples": [{"id": "ai-example-1", "title": "Demo", "code": "print(1)"}],
                    "exam_questions": [{"id": "exam-1", "question": "What prints?"}],
                    "lecture_snippets": [{"id": "lecture-1", "explanation": "Names can be rebound.", "code_examples": []}],
                    "notebook_snippets": [{"id": "nb-1", "source": "values = [1, 2]\\nprint(values)", "outputs": ["[1, 2]"]}],
                    "recommended_ids": ["exam-1", "lecture-1"],
                },
            }
        ]

        items = iter_selectable_items(cards)
        item_ids = {item["item_id"] for item in items}
        item_types = {item["item_type"] for item in items}

        self.assertIn("aiq-1", item_ids)
        self.assertIn("kp-1", item_ids)
        self.assertIn("kp-1-d1", item_ids)
        self.assertIn("ai-example-1", item_ids)
        self.assertIn("exam-1", item_ids)
        self.assertIn("lecture-1", item_ids)
        self.assertIn("nb-1", item_ids)
        self.assertNotIn("ai_summary", item_types)

    def test_recommended_and_additional_source_buckets_match_ui_split(self) -> None:
        cards = [
            {
                "id": "card-1",
                "topic": "Demo Topic",
                "sections": {
                    "ai_summary": {},
                    "ai_common_questions": {},
                    "key_points_to_remember": [],
                    "ai_examples": [],
                    "exam_questions": [{"id": "exam-1", "question": "Q"}],
                    "lecture_snippets": [{"id": "lecture-1", "explanation": "Long enough explanation.", "code_examples": []}],
                    "notebook_snippets": [{"id": "nb-1", "source": "x = 1\\nprint(x)", "outputs": ["1"]}],
                    "recommended_ids": ["lecture-1"],
                },
            }
        ]

        items = {item["item_id"]: item for item in iter_selectable_items(cards)}
        self.assertEqual(items["lecture-1"]["bucket"], "recommended")
        self.assertEqual(items["exam-1"]["bucket"], "additional")
        self.assertEqual(items["nb-1"]["bucket"], "additional")

    def test_unique_exam_sources_drop_the_known_duplicate_copy(self) -> None:
        duplicate_exam_ids = {exam["exam_id"] for exam in EXAM_SOURCES if exam.get("duplicate_of")}
        unique_exam_ids = {exam["exam_id"] for exam in unique_exam_sources()}

        self.assertEqual(len(duplicate_exam_ids), 1)
        self.assertEqual(len(unique_exam_ids), len(EXAM_SOURCES) - 1)
        self.assertFalse(duplicate_exam_ids & unique_exam_ids)


if __name__ == "__main__":
    unittest.main()
