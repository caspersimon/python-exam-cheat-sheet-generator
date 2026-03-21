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
            data = json.load(handle)
        cls.cards = data["cards"]
        cls.deck_groups = data.get("deck_groups", [])

    def test_deck_groups_cover_all_week_bundles(self) -> None:
        self.assertEqual(len(self.deck_groups), 6, "Expected six week deck groups")
        weeks = [group.get("week") for group in self.deck_groups]
        self.assertEqual(weeks, [1, 2, 3, 4, 5, 6], "Week deck groups should be ordered and contiguous")
        for group in self.deck_groups:
            week = group.get("week")
            self.assertEqual(group.get("id"), f"week-{week}")
            self.assertEqual(group.get("title"), f"Week {week}")
            self.assertIsInstance(group.get("topic_refs"), list)
            self.assertGreater(len(group["topic_refs"]), 0, f"Week {week} should reference at least one topic")

    def test_cards_have_expected_shape(self) -> None:
        for card in self.cards:
            self.assertIsInstance(card.get("id"), str)
            self.assertIsInstance(card.get("topic"), str)
            self.assertIsInstance(card.get("canonical_topic"), str)
            self.assertIsInstance(card.get("weeks"), list)
            self.assertIsInstance(card.get("exam_stats"), dict)
            self.assertIsInstance(card.get("related_topics"), list)
            self.assertIsInstance(card.get("trap_patterns"), list)

            sections = card["sections"]
            for key in [
                "lecture_snippets",
                "exam_questions",
                "notebook_snippets",
                "ai_examples",
                "key_points_to_remember",
                "recommended_ids",
            ]:
                self.assertIsInstance(sections.get(key), list, f"{card['id']}: {key} must be list")
            self.assertIsInstance(sections.get("ai_summary"), dict, f"{card['id']}: ai_summary must be dict")
            self.assertIsInstance(sections.get("ai_common_questions"), dict, f"{card['id']}: ai_common_questions must be dict")

    def test_card_ids_are_unique(self) -> None:
        ids = [card["id"] for card in self.cards]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate card ids found in topic_cards.json")

    def test_recommended_ids_refer_to_real_source_items(self) -> None:
        for card in self.cards:
            sections = card["sections"]
            valid_ids = {
                item.get("id")
                for bucket in ["lecture_snippets", "exam_questions", "notebook_snippets"]
                for item in sections.get(bucket, [])
                if isinstance(item, dict) and item.get("id")
            }
            for recommended_id in sections.get("recommended_ids", []):
                self.assertIn(recommended_id, valid_ids, f"{card['id']}: missing recommended id {recommended_id}")

    def test_week_bundle_references_align_with_cards(self) -> None:
        card_ids = {card["id"] for card in self.cards}
        for group in self.deck_groups:
            for ref in group.get("topic_refs", []):
                self.assertIn(ref.get("card_id"), card_ids, f"{group.get('id')}: unknown card reference {ref.get('card_id')}")
                self.assertIsInstance(ref.get("item_counts"), dict, f"{group.get('id')}: item_counts must be a dict")
                self.assertIsInstance(ref.get("exam_hits"), int, f"{group.get('id')}: exam_hits must be an int")
                self.assertGreaterEqual(ref.get("exam_hits", 0), 0)


if __name__ == "__main__":
    unittest.main()
