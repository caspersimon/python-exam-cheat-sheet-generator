from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT / "new_database" / "exports" / "frontend_bundle.json"

VALID_BLOCK_TYPES = {"paragraph", "table", "code", "list"}
VALID_EMPHASIS = {"trap"}


class FrontendBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(DATASET_PATH.read_text(encoding="utf-8"))

    def test_topics_shape_is_valid(self) -> None:
        topics = self.payload.get("topics")
        self.assertIsInstance(topics, list)
        self.assertGreaterEqual(len(topics), 1)

    def test_bundle_uses_topic_subtopic_snippet_piece_hierarchy(self) -> None:
        seen_piece_ids: set[str] = set()

        for topic in self.payload["topics"]:
            self.assertTrue(topic["topic_slug"])
            self.assertTrue(topic["title"])
            self.assertIsInstance(topic["subtopics"], list)

            for subtopic in topic["subtopics"]:
                self.assertTrue(subtopic["slug"])
                self.assertTrue(subtopic["title"])
                self.assertIsInstance(subtopic["snippets"], list)

                for snippet in subtopic["snippets"]:
                    self.assertTrue(snippet["slug"])
                    self.assertTrue(snippet["title"])
                    self.assertIsInstance(snippet["keywords"], list)
                    self.assertIsInstance(snippet["trap_slugs"], list)
                    self.assertIsInstance(snippet["pieces"], list)

                    for piece in snippet["pieces"]:
                        self.assertTrue(piece["piece_id"])
                        self.assertNotIn(piece["piece_id"], seen_piece_ids)
                        seen_piece_ids.add(piece["piece_id"])
                        self.assertIn("body_markdown", piece)
                        self.assertIsInstance(piece["body_blocks"], list)
                        for block in piece["body_blocks"]:
                            self.assertIn(block["type"], VALID_BLOCK_TYPES)

    def test_trap_metadata_is_optional_but_valid(self) -> None:
        for topic in self.payload["topics"]:
            for subtopic in topic["subtopics"]:
                for snippet in subtopic["snippets"]:
                    for piece in snippet["pieces"]:
                        if piece.get("role") == "trap":
                            self.assertIsInstance(piece.get("trap_slugs"), list)

    def test_presets_reference_real_bundle_pieces(self) -> None:
        piece_ids = {
            piece["piece_id"]
            for topic in self.payload["topics"]
            for subtopic in topic["subtopics"]
            for snippet in subtopic["snippets"]
            for piece in snippet["pieces"]
        }
        presets = self.payload.get("presets")
        self.assertIsInstance(presets, list)
        self.assertGreaterEqual(len(presets), 1)

        for preset in presets:
            self.assertTrue(preset["preset_id"])
            self.assertIsInstance(preset["items"], list)
            for item in preset["items"]:
                self.assertIn(item["piece_id"], piece_ids)


if __name__ == "__main__":
    unittest.main()
