import json
from collections import Counter
from pathlib import Path
import re
import unittest


class TopicCardsIntegrityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[1]
        with (root / "topic_cards.json").open("r", encoding="utf-8") as handle:
            cls.cards = json.load(handle)["cards"]

    def test_unique_card_ids(self) -> None:
        ids = [card["id"] for card in self.cards]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate card IDs found")

    def test_no_duplicate_normalized_topics(self) -> None:
        def norm_topic(topic: str) -> str:
            topic = (topic or "").lower().replace("_", " ").replace("-", " ")
            topic = re.sub(r"\s+", " ", topic).strip()
            if topic.endswith("ies") and len(topic) > 4:
                topic = topic[:-3] + "y"
            elif topic.endswith("s") and len(topic) > 4 and not topic.endswith("ss"):
                topic = topic[:-1]
            return topic

        duplicates = [
            key
            for key, count in Counter(norm_topic(card["topic"]) for card in self.cards).items()
            if count > 1
        ]
        self.assertEqual(duplicates, [], f"Duplicate normalized topics found: {duplicates}")

    def test_sections_and_recommended_ids_are_valid(self) -> None:
        for card in self.cards:
            sections = card["sections"]
            required_lists = [
                "lecture_snippets",
                "exam_questions",
                "notebook_snippets",
                "ai_examples",
                "key_points_to_remember",
                "recommended_ids",
            ]
            for key in required_lists:
                self.assertIsInstance(sections.get(key), list, f"{card['id']}: {key} must be list")

            valid_ids = {
                item.get("id")
                for bucket in ["lecture_snippets", "exam_questions", "notebook_snippets"]
                for item in sections.get(bucket, [])
                if isinstance(item, dict)
            }
            for rid in sections.get("recommended_ids", []):
                self.assertIn(rid, valid_ids, f"{card['id']}: recommended id not found: {rid}")


if __name__ == "__main__":
    unittest.main()
