from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts" / "repair_topic_cards.py"


def _load_module():
    spec = importlib.util.spec_from_file_location("repair_topic_cards", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


class RepairTopicCardsTests(unittest.TestCase):
    def test_repair_payload_merges_known_duplicate_cards(self) -> None:
        module = _load_module()
        payload = {
            "meta": {},
            "cards": [
                {
                    "id": "topic-f-string",
                    "topic": "Strings",
                    "canonical_topic": "f string",
                    "weeks": [1],
                    "exam_stats": {"total_hits": 1, "by_exam": {"exam-a": 1}, "coverage_count": 1},
                    "related_topics": ["formatting"],
                    "trap_patterns": [{"pattern": "f string", "trap": "missing prefix", "weeks": [1]}],
                    "sections": {
                        "lecture_snippets": [{"id": "lec-1", "topic": "f-string"}],
                        "exam_questions": [{"id": "exm-1", "exam_label": "exam-a"}],
                        "notebook_snippets": [{"id": "nb-1"}],
                        "ai_examples": [{"id": "ex-1", "title": "Basic", "code": "print(f'{x}')"}],
                        "key_points_to_remember": [{"id": "kp-1", "text": "Remember the f prefix."}],
                        "recommended_ids": ["lec-1", "exm-1"],
                    },
                },
                {
                    "id": "topic-debugging-f-string",
                    "topic": "Strings",
                    "canonical_topic": "debugging f string",
                    "weeks": [2],
                    "exam_stats": {"total_hits": 1, "by_exam": {"exam-b": 1}, "coverage_count": 1},
                    "related_topics": ["debugging"],
                    "trap_patterns": [{"pattern": "f string", "trap": "spacing", "weeks": [2]}],
                    "sections": {
                        "lecture_snippets": [{"id": "lec-2", "topic": "f-string debug"}],
                        "exam_questions": [{"id": "exm-2", "exam_label": "exam-b"}],
                        "notebook_snippets": [{"id": "nb-2"}],
                        "ai_examples": [{"id": "ex-2", "title": "Debug", "code": "print(f'{x=}')"}],
                        "key_points_to_remember": [{"id": "kp-2", "text": "f'{x=}' keeps the name."}],
                        "recommended_ids": ["lec-2", "exm-2"],
                    },
                },
            ],
        }

        summary = module.repair_payload(payload)

        self.assertEqual(summary["merges_applied"], 1)
        self.assertEqual(summary["card_count"], 1)
        self.assertEqual(len(payload["cards"]), 1)
        card = payload["cards"][0]
        self.assertEqual(card["id"], "topic-f-string")
        self.assertEqual(card["weeks"], [1, 2])
        self.assertEqual(card["exam_stats"]["total_hits"], 2)
        self.assertEqual(card["exam_stats"]["coverage_count"], 2)
        self.assertEqual(
            [item["id"] for item in card["sections"]["exam_questions"]],
            ["exm-1", "exm-2"],
        )
        self.assertIn("lec-2", card["sections"]["recommended_ids"])
        self.assertEqual(len(payload["deck_groups"]), 2)
        self.assertTrue(any("merged hand-reviewed duplicate cards" in note for note in payload["meta"]["notes"]))

    def test_repair_payload_relabels_generic_topics(self) -> None:
        module = _load_module()
        payload = {
            "meta": {},
            "cards": [
                {
                    "id": "topic-loop",
                    "topic": "OOP",
                    "canonical_topic": "loop",
                    "weeks": [2],
                    "exam_stats": {"total_hits": 1, "by_exam": {"exam-a": 1}, "coverage_count": 1},
                    "related_topics": [],
                    "trap_patterns": [],
                    "sections": {
                        "lecture_snippets": [],
                        "exam_questions": [],
                        "notebook_snippets": [],
                        "ai_examples": [],
                        "key_points_to_remember": [],
                        "recommended_ids": [],
                    },
                },
                {
                    "id": "topic-fstring",
                    "topic": "Strings",
                    "canonical_topic": "f string",
                    "weeks": [2],
                    "exam_stats": {"total_hits": 1, "by_exam": {"exam-a": 1}, "coverage_count": 1},
                    "related_topics": [],
                    "trap_patterns": [],
                    "sections": {
                        "lecture_snippets": [],
                        "exam_questions": [],
                        "notebook_snippets": [],
                        "ai_examples": [],
                        "key_points_to_remember": [],
                        "recommended_ids": [],
                    },
                },
            ],
        }

        summary = module.repair_payload(payload)

        self.assertEqual(summary["labels_changed"], 2)
        self.assertEqual(payload["cards"][0]["topic"], "Loops")
        self.assertEqual(payload["cards"][1]["topic"], "f-Strings")


if __name__ == "__main__":
    unittest.main()
