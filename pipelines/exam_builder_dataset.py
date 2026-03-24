from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pipelines.exam_builder_dataset_families import build_existing_families
from pipelines.exam_builder_dataset_specs import MAIN_TOPIC_SUMMARIES, PARENT_TOPIC_SPECS, slugify, timestamp_utc
from pipelines.exam_builder_manual_snippets import MANUAL_SNIPPETS
from scripts.exam_coverage_audit import ROOT


OUTPUT_PATH = ROOT / "data" / "exam_builder_topics.json"
ROUND2_PATH = ROOT / "data" / "vision_exam_pipeline" / "evaluations" / "round2.json"


@dataclass
class RankingStats:
    repeat_exam_count: int = 0
    best_single_count: int = 0
    top_three_support_count: int = 0
    minimal_only_count: int = 0
    certain_support_count: int = 0

    @property
    def highest_value_score(self) -> int:
        return (
            5 * self.best_single_count
            + 3 * self.top_three_support_count
            + 2 * self.minimal_only_count
            + self.certain_support_count
        )


def compute_ranking_stats(round2_payload: dict[str, Any]) -> dict[str, RankingStats]:
    stats: dict[str, RankingStats] = defaultdict(RankingStats)
    for question in round2_payload.get("questions", []):
        if not isinstance(question, dict):
            continue
        answerability = question.get("answerability") or {}
        is_certain = answerability.get("status") == "certain"
        minimal_families = [entry.get("snippet_id") for entry in question.get("minimal_snippet_families", []) if isinstance(entry, dict) and entry.get("snippet_id")]
        best_family = (question.get("best_snippet_family") or {}).get("snippet_id")
        support_families = [entry.get("snippet_id") for entry in question.get("supporting_snippet_families", []) if isinstance(entry, dict) and entry.get("snippet_id")]
        near_identical = [entry.get("snippet_id") for entry in question.get("near_identical_past_exam_pieces", []) if isinstance(entry, dict) and entry.get("snippet_id")]

        for snippet_id in near_identical:
            stats[snippet_id].repeat_exam_count += 1
        if best_family:
            stats[best_family].best_single_count += 1
        for snippet_id in support_families:
            stats[snippet_id].top_three_support_count += 1

        scored_families = {best_family, *support_families}
        for snippet_id in minimal_families:
            if snippet_id and snippet_id not in scored_families:
                stats[snippet_id].minimal_only_count += 1
        if is_certain:
            for snippet_id in {best_family, *support_families, *minimal_families}:
                if snippet_id:
                    stats[snippet_id].certain_support_count += 1
    return stats


def assign_scores(snippets: list[dict[str, Any]], ranking_stats: dict[str, RankingStats]) -> None:
    for snippet in snippets:
        if snippet["score_source"] == "manual_bootstrap":
            continue
        stats = ranking_stats.get(snippet.get("source_snippet_id", ""), RankingStats())
        snippet["repeat_exam_count"] = stats.repeat_exam_count
        snippet["best_single_count"] = stats.best_single_count
        snippet["top_three_support_count"] = stats.top_three_support_count
        snippet["minimal_only_count"] = stats.minimal_only_count
        snippet["certain_support_count"] = stats.certain_support_count
        snippet["importance_score"] = stats.highest_value_score
        if stats.repeat_exam_count >= 2:
            snippet["importance_bucket"] = "expect_questions"
            snippet["importance_score"] = stats.repeat_exam_count * 10 + stats.highest_value_score
        elif stats.best_single_count > 0 or stats.top_three_support_count > 0:
            snippet["importance_bucket"] = "highest_value"
        elif stats.minimal_only_count > 0:
            snippet["importance_bucket"] = "dont_forget"
            snippet["importance_score"] = 2 * stats.minimal_only_count + stats.certain_support_count
        else:
            snippet["importance_bucket"] = "maybe_need"
            snippet["importance_score"] = fallback_score(snippet)


def fallback_score(snippet: dict[str, Any]) -> int:
    pieces = snippet.get("pieces", [])
    piece_count = len(pieces)
    all_types = {piece.get("piece_type") for piece in pieces}
    score = 0.0
    if any(piece.get("piece_type") == "reference_table" for piece in pieces):
        score += 2.0
    if snippet.get("snippet_type") == "past_exam_question":
        score += 1.5
    score += min(2.5, piece_count * 0.6)
    if all_types == {"explanation"}:
        score -= 1.0
    return max(1, round(score))


def add_manual_snippets(snippets: list[dict[str, Any]]) -> None:
    for snippet in MANUAL_SNIPPETS:
        record = json.loads(json.dumps(snippet))
        record.setdefault("repeat_exam_count", 0)
        record.setdefault("best_single_count", 0)
        record.setdefault("top_three_support_count", 0)
        record.setdefault("minimal_only_count", 0)
        record.setdefault("certain_support_count", 0)
        record.setdefault("source_snippet_id", "")
        snippets.append(record)


def sort_snippet_key(snippet: dict[str, Any]) -> tuple[Any, ...]:
    source_priority = 0 if snippet.get("score_source") == "round2_derived" else 1
    return (
        -int(snippet.get("importance_score") or 0),
        source_priority,
        -int(snippet.get("repeat_exam_count") or 0),
        snippet.get("title", "").lower(),
    )


def bucket_initial_count(bucket_key: str, snippets: list[dict[str, Any]]) -> int:
    if bucket_key in {"expect_questions", "dont_forget", "maybe_need"}:
        return min(5, len(snippets))
    if not snippets:
        return 0
    total = sum(int(snippet.get("importance_score") or 0) for snippet in snippets)
    if total <= 0:
        return min(3, len(snippets))
    running = 0
    count = 0
    for snippet in snippets:
        running += int(snippet.get("importance_score") or 0)
        count += 1
        if running >= total * 0.5:
            break
    if len(snippets) >= 3:
        count = max(count, 3)
    return min(count, len(snippets))


def build_payload() -> dict[str, Any]:
    round2_payload = json.loads(ROUND2_PATH.read_text(encoding="utf-8"))
    ranking_stats = compute_ranking_stats(round2_payload)
    family_map = build_existing_families()
    snippets = list(family_map.values())
    add_manual_snippets(snippets)
    assign_scores(snippets, ranking_stats)

    by_topic: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for snippet in snippets:
        snippet["pieces"] = sorted(snippet["pieces"], key=lambda piece: piece["id"])
        search_bits = [snippet["title"], *[piece.get("title", "") for piece in snippet["pieces"]]]
        for piece in snippet["pieces"]:
            content = piece.get("content", {})
            if isinstance(content, dict):
                search_bits.extend(str(value) for value in content.values() if isinstance(value, (str, int)))
        snippet["search_text"] = " ".join(str(bit) for bit in search_bits if bit).strip()
        by_topic[(snippet["parent_topic"], snippet["main_topic"])].append(snippet)

    parent_topics: list[dict[str, Any]] = []
    for parent_index, (parent_id, parent_title, main_topics) in enumerate(PARENT_TOPIC_SPECS, start=1):
        parent_record = {"id": parent_id, "title": parent_title, "order": parent_index, "main_topics": []}
        for main_index, main_title in enumerate(main_topics, start=1):
            topic_snippets = sorted(by_topic.get((parent_title, main_title), []), key=sort_snippet_key)
            buckets = []
            for bucket_key, bucket_title in [
                ("expect_questions", "Expect these questions"),
                ("highest_value", "Highest value snippets"),
                ("dont_forget", "Don't forget about"),
                ("maybe_need", "Maybe you'll need these"),
            ]:
                bucket_snippets = [snippet for snippet in topic_snippets if snippet.get("importance_bucket") == bucket_key]
                if bucket_snippets:
                    buckets.append(
                        {
                            "key": bucket_key,
                            "title": bucket_title,
                            "initial_visible_count": bucket_initial_count(bucket_key, bucket_snippets),
                            "snippets": bucket_snippets,
                        }
                    )
            related_weeks = sorted({week for snippet in topic_snippets for week in snippet.get("related_weeks", []) if isinstance(week, int)})
            parent_record["main_topics"].append(
                {
                    "id": slugify(main_title),
                    "title": main_title,
                    "summary": MAIN_TOPIC_SUMMARIES[main_title],
                    "parent_topic": parent_title,
                    "main_week": min(related_weeks) if related_weeks else 0,
                    "related_weeks": related_weeks,
                    "search_text": " ".join(snippet.get("search_text", "") for snippet in topic_snippets).strip(),
                    "topic_order": main_index,
                    "buckets": buckets,
                }
            )
        parent_topics.append(parent_record)

    return {
        "schema_version": "1.0",
        "generated_at": timestamp_utc(),
        "meta": {
            "title": "Exam-first cheat sheet builder dataset",
            "source_topic_cards": "topic_cards.json",
            "source_round": "round2",
        },
        "parent_topics": parent_topics,
    }


def write_payload(output_path: Path = OUTPUT_PATH) -> Path:
    payload = build_payload()
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
