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
            self.assertIsInstance(group.get("topic_groups"), list)
            self.assertGreater(len(group["topic_groups"]), 0, f"Week {week} should contain at least one topic group")

    def test_cards_have_expected_shape(self) -> None:
        for card in self.cards:
            self.assertIsInstance(card.get("id"), str)
            self.assertIsInstance(card.get("topic"), str)
            self.assertIsInstance(card.get("canonical_topic"), str)
            self.assertIsInstance(card.get("weeks"), list)
            self.assertIsInstance(card.get("week_id"), str)
            self.assertIsInstance(card.get("topic_meta"), dict)
            self.assertIsInstance(card.get("subtopics"), list)
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
            for subtopic in card.get("subtopics", []):
                self.assertIsInstance(subtopic.get("id"), str)
                self.assertIsInstance(subtopic.get("title"), str)
                self.assertIsInstance(subtopic.get("item_ids"), dict)

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
            for topic_group in group.get("topic_groups", []):
                for ref in topic_group.get("topic_refs", []):
                    self.assertIn(ref.get("card_id"), card_ids, f"{group.get('id')}: unknown card reference {ref.get('card_id')}")
                    self.assertIsInstance(ref.get("exam_hits"), int, f"{group.get('id')}: exam_hits must be an int")
                    self.assertGreaterEqual(ref.get("exam_hits", 0), 0)

    def test_subtopic_item_ids_reference_real_items(self) -> None:
        for card in self.cards:
            valid_ids = {
                item.get("id")
                for bucket in ["lecture_snippets", "exam_questions", "notebook_snippets", "ai_examples", "key_points_to_remember"]
                for item in card.get("sections", {}).get(bucket, [])
                if isinstance(item, dict) and item.get("id")
            }
            for subtopic in card.get("subtopics", []):
                item_ids = subtopic.get("item_ids", {})
                for bucket_ids in item_ids.values():
                    for item_id in bucket_ids:
                        self.assertIn(item_id, valid_ids, f"{card['id']}: unknown subtopic item id {item_id}")

    def test_common_question_bullets_are_unique_per_card(self) -> None:
        for card in self.cards:
            bullets = card.get("sections", {}).get("ai_common_questions", {}).get("bullets", [])
            normalized = [" ".join(str(bullet or "").lower().split()) for bullet in bullets if str(bullet or "").strip()]
            self.assertEqual(
                len(normalized),
                len(set(normalized)),
                f"{card['id']}: duplicate ai_common_questions bullets found",
            )

    def test_dense_tables_do_not_repeat_across_common_questions_and_key_points(self) -> None:
        for card in self.cards:
            common_tables = {
                self._table_signature(item.get("table"))
                for item in card.get("sections", {}).get("ai_common_questions", {}).get("items", [])
                if isinstance(item, dict) and item.get("table")
            }
            detail_tables = {
                self._table_signature(detail.get("table"))
                for key_point in card.get("sections", {}).get("key_points_to_remember", [])
                for detail in key_point.get("details", []) or []
                if isinstance(detail, dict) and detail.get("table")
            }
            common_tables.discard("")
            detail_tables.discard("")
            self.assertFalse(
                common_tables & detail_tables,
                f"{card['id']}: duplicate dense reference table appears in common questions and key point details",
            )

    @staticmethod
    def _table_signature(table: dict | None) -> str:
        if not isinstance(table, dict):
            return ""
        headers = "|".join(" ".join(str(cell or "").lower().split()) for cell in table.get("headers", []))
        rows = "||".join(
            "|".join(" ".join(str(cell or "").lower().split()) for cell in row)
            for row in table.get("rows", [])
        )
        return f"{headers}###{rows}"


if __name__ == "__main__":
    unittest.main()
