from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "data" / "exam_builder_topics.json"

VALID_PIECE_TYPES = {"reference_table", "code_example", "explanation", "past_exam_piece"}


class ExamBuilderDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(DATASET_PATH.read_text(encoding="utf-8"))

    def test_parent_topics_exist(self) -> None:
        parent_topics = self.payload.get("parent_topics")
        self.assertIsInstance(parent_topics, list)
        self.assertEqual(7, len(parent_topics))

    def test_manual_sections_shape_is_valid(self) -> None:
        seen_piece_ids: set[str] = set()

        for parent_topic in self.payload["parent_topics"]:
            self.assertTrue(parent_topic["id"])
            self.assertTrue(parent_topic["title"])

            for main_topic in parent_topic["main_topics"]:
                self.assertTrue(main_topic["id"])
                self.assertTrue(main_topic["title"])
                self.assertEqual(parent_topic["title"], main_topic["parent_topic"])
                self.assertIsInstance(main_topic.get("sections"), list)
                self.assertGreaterEqual(len(main_topic["sections"]), 1)
                self.assertLessEqual(len(main_topic["sections"]), 10)

                seen_section_keys: set[str] = set()
                for section in main_topic["sections"]:
                    self.assertTrue(section["key"])
                    self.assertTrue(section["title"])
                    self.assertNotIn(section["key"], seen_section_keys)
                    seen_section_keys.add(section["key"])
                    self.assertGreaterEqual(section["initial_visible_count"], 1)

                    for index, snippet in enumerate(section["snippets"], start=1):
                        self.assertTrue(snippet["id"])
                        self.assertTrue(snippet["title"])
                        self.assertEqual(index, snippet["order"])
                        self.assertEqual(parent_topic["title"], snippet["parent_topic"])
                        self.assertEqual(main_topic["title"], snippet["main_topic"])
                        self.assertIn(snippet["snippet_type"], {"general_snippet", "past_exam_question"})
                        self.assertIn("source_refs", snippet)

                        for piece_index, piece in enumerate(snippet["pieces"], start=1):
                            self.assertTrue(piece["id"])
                            self.assertEqual(piece_index, piece["order"])
                            self.assertIn(piece["piece_type"], VALID_PIECE_TYPES)
                            self.assertNotIn(piece["id"], seen_piece_ids)
                            seen_piece_ids.add(piece["id"])
                            self.assertIn("source_refs", piece)

    def test_score_driven_fields_are_not_required(self) -> None:
        for parent_topic in self.payload["parent_topics"]:
            for main_topic in parent_topic["main_topics"]:
                for section in main_topic["sections"]:
                    for snippet in section["snippets"]:
                        self.assertNotIn("importance_bucket", snippet)
                        self.assertNotIn("importance_score", snippet)
                        self.assertNotIn("score_source", snippet)
                        self.assertNotIn("manual_score_reason", snippet)


if __name__ == "__main__":
    unittest.main()
