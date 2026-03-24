from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from pipelines.vision_exam_pipeline_selectable import build_selectable_items_snapshot, snippet_family_index
from pipelines.vision_exam_pipeline_shared import (
    ANALYTICS_DIR,
    ANALYTICS_SCHEMA,
    EVALUATIONS_DIR,
    SELECTABLE_ITEMS_FILE,
    _read_json,
    _safe_dict,
    _safe_list,
    _safe_str,
    _write_json,
    portable_path,
    snippet_identity_for_item,
    timestamp_utc,
)


def _evaluation_file(round_name: str) -> Path:
    return EVALUATIONS_DIR / f"{round_name}.json"


def _analytics_file(round_name: str) -> Path:
    return ANALYTICS_DIR / f"{round_name}.json"


def _analytics_report_file(round_name: str) -> Path:
    return ANALYTICS_DIR / f"{round_name}.md"


def _comparison_summary(current: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    current_counts = Counter(_safe_str(_safe_dict(item.get("answerability")).get("status")) for item in _safe_list(current.get("questions")))
    baseline_counts = Counter(_safe_str(_safe_dict(item.get("answerability")).get("status")) for item in _safe_list(baseline.get("questions")))
    return {
        key: {
            "current": int(current_counts.get(key, 0)),
            "baseline": int(baseline_counts.get(key, 0)),
            "delta": int(current_counts.get(key, 0) - baseline_counts.get(key, 0)),
        }
        for key in sorted(set(current_counts) | set(baseline_counts))
        if key
    }


def build_ranking_analytics(
    *,
    round_name: str,
    evaluation_payload: dict[str, Any],
    selectable_items: list[dict[str, Any]],
    baseline_payload: dict[str, Any] | None = None,
) -> tuple[dict[str, Any], str]:
    selectable_by_id = {item["item_id"]: item for item in selectable_items if isinstance(item, dict) and item.get("item_id")}
    selectable_by_snippet = snippet_family_index(selectable_items)
    completed = [item for item in _safe_list(evaluation_payload.get("questions")) if _safe_str(_safe_dict(item).get("status")) == "completed"]
    status_counts = Counter(_safe_str(_safe_dict(item).get("status")) for item in _safe_list(evaluation_payload.get("questions")))
    answerability_counts = Counter(_safe_str(_safe_dict(item.get("answerability")).get("status")) for item in completed)
    week_stats: dict[int, dict[str, set[str]]] = defaultdict(lambda: {"top1": set(), "top3": set(), "minimal": set(), "all": set()})
    repeated_exam_piece_counts: Counter[str] = Counter()

    for snippet_id, family in selectable_by_snippet.items():
        week = int(family.get("week") or 0)
        if week > 0:
            week_stats[week]["all"].add(snippet_id)
    for evaluation in completed:
        for piece in _safe_list(evaluation.get("near_identical_past_exam_pieces")):
            item_id = _safe_str(_safe_dict(piece).get("item_id"))
            if item_id:
                repeated_exam_piece_counts[item_id] += 1
        best_family = _safe_dict(evaluation.get("best_snippet_family"))
        best_snippet_id = _safe_str(best_family.get("snippet_id"))
        if best_snippet_id in selectable_by_snippet:
            week = int(selectable_by_snippet[best_snippet_id].get("week") or 0)
            week_stats[week]["top1"].add(best_snippet_id)
            week_stats[week]["top3"].add(best_snippet_id)
        elif not best_snippet_id:
            best = _safe_dict(evaluation.get("best_single_snippet"))
            item_id = _safe_str(best.get("item_id"))
            if item_id in selectable_by_id:
                snippet_id = _safe_str(selectable_by_id[item_id].get("snippet_id"))
                if not snippet_id:
                    snippet_id, _ = snippet_identity_for_item(selectable_by_id[item_id])
                if snippet_id in selectable_by_snippet:
                    week = int(selectable_by_snippet[snippet_id].get("week") or 0)
                    week_stats[week]["top1"].add(snippet_id)
                    week_stats[week]["top3"].add(snippet_id)
        if _safe_list(evaluation.get("supporting_snippet_families")):
            for family in _safe_list(evaluation.get("supporting_snippet_families")):
                snippet_id = _safe_str(_safe_dict(family).get("snippet_id"))
                if snippet_id in selectable_by_snippet:
                    week_stats[int(selectable_by_snippet[snippet_id].get("week") or 0)]["top3"].add(snippet_id)
        else:
            for snippet in _safe_list(evaluation.get("top_three_snippets")):
                item_id = _safe_str(_safe_dict(snippet).get("item_id"))
                if item_id in selectable_by_id:
                    snippet_id = _safe_str(selectable_by_id[item_id].get("snippet_id"))
                    if not snippet_id:
                        snippet_id, _ = snippet_identity_for_item(selectable_by_id[item_id])
                    if snippet_id in selectable_by_snippet:
                        week_stats[int(selectable_by_snippet[snippet_id].get("week") or 0)]["top3"].add(snippet_id)
        if _safe_list(evaluation.get("minimal_snippet_families")):
            for family in _safe_list(evaluation.get("minimal_snippet_families")):
                snippet_id = _safe_str(_safe_dict(family).get("snippet_id"))
                if snippet_id in selectable_by_snippet:
                    week_stats[int(selectable_by_snippet[snippet_id].get("week") or 0)]["minimal"].add(snippet_id)
        else:
            for snippet in _safe_list(evaluation.get("minimal_sufficient_snippets")):
                item_id = _safe_str(_safe_dict(snippet).get("item_id"))
                if item_id in selectable_by_id:
                    snippet_id = _safe_str(selectable_by_id[item_id].get("snippet_id"))
                    if not snippet_id:
                        snippet_id, _ = snippet_identity_for_item(selectable_by_id[item_id])
                    if snippet_id in selectable_by_snippet:
                        week_stats[int(selectable_by_snippet[snippet_id].get("week") or 0)]["minimal"].add(snippet_id)

    weeks_payload = []
    for week in sorted(week for week in week_stats if week > 0):
        stats = week_stats[week]
        never_used = sorted(stats["all"] - stats["minimal"])
        weeks_payload.append(
            {
                "week": week,
                "top1_unique_snippets": len(stats["top1"]),
                "top3_unique_snippets": len(stats["top3"]),
                "minimal_set_unique_snippets": len(stats["minimal"]),
                "minimal_set_unused_snippets": len(never_used),
                "unused_snippet_ids": never_used[:50],
            }
        )

    insights = []
    if not completed:
        insights.append("No completed question-to-snippet evaluations yet. Ranking decisions should wait until round reviews are filled in.")
    elif weeks_payload:
        top_week = max(weeks_payload, key=lambda row: row["minimal_set_unique_snippets"])
        insights.append(f"Week {top_week['week']} currently has the broadest minimal-set footprint with {top_week['minimal_set_unique_snippets']} unique snippets.")

    analytics = {
        "schema_version": ANALYTICS_SCHEMA,
        "generated_at": timestamp_utc(),
        "round": round_name,
        "input_evaluations_path": portable_path(_evaluation_file(round_name)),
        "summary": {
            "total_evaluations": len(_safe_list(evaluation_payload.get("questions"))),
            "completed_evaluations": len(completed),
            "status_counts": dict(status_counts),
            "answerability_counts": dict(answerability_counts),
            "near_identical_repeat_piece_count": sum(1 for _, count in repeated_exam_piece_counts.items() if count >= 2),
        },
        "weeks": weeks_payload,
        "insights": insights,
        "repeated_near_identical_exam_pieces": [
            {"item_id": item_id, "count": int(count)}
            for item_id, count in repeated_exam_piece_counts.most_common()
            if count >= 2
        ],
        "comparison": _comparison_summary(evaluation_payload, baseline_payload or {}) if baseline_payload else {},
    }

    lines = [
        f"# Ranking Analytics ({round_name})",
        "",
        f"- Total evaluations: `{analytics['summary']['total_evaluations']}`",
        f"- Completed evaluations: `{analytics['summary']['completed_evaluations']}`",
        f"- Status counts: `{json.dumps(analytics['summary']['status_counts'], ensure_ascii=False, sort_keys=True)}`",
    ]
    if analytics["summary"]["answerability_counts"]:
        lines.append(f"- Answerability counts: `{json.dumps(analytics['summary']['answerability_counts'], ensure_ascii=False, sort_keys=True)}`")
    if analytics["summary"]["near_identical_repeat_piece_count"]:
        lines.append(f"- Repeated near-identical past-exam pieces: `{analytics['summary']['near_identical_repeat_piece_count']}`")
    lines.extend(["", "## Week Summary", ""])
    if weeks_payload:
        lines.append("| Week | Top 1 unique | Top 3 unique | Minimal-set unique | Minimal-set unused |")
        lines.append("|---|---:|---:|---:|---:|")
        for row in weeks_payload:
            lines.append(f"| {row['week']} | {row['top1_unique_snippets']} | {row['top3_unique_snippets']} | {row['minimal_set_unique_snippets']} | {row['minimal_set_unused_snippets']} |")
    else:
        lines.append("No completed evaluations yet.")
    if insights:
        lines.extend(["", "## Insights", ""])
        for insight in insights:
            lines.append(f"- {insight}")
    return analytics, "\n".join(lines) + "\n"


def write_ranking_analytics(
    *,
    round_name: str,
    baseline_round: str = "",
    selectable_items_path: Path = SELECTABLE_ITEMS_FILE,
) -> dict[str, Any]:
    evaluations = _read_json(_evaluation_file(round_name))
    selectable_items = _read_json(selectable_items_path) if selectable_items_path.exists() else build_selectable_items_snapshot()
    baseline = _read_json(_evaluation_file(baseline_round)) if baseline_round and _evaluation_file(baseline_round).exists() else None
    analytics, markdown = build_ranking_analytics(
        round_name=round_name,
        evaluation_payload=evaluations,
        selectable_items=selectable_items,
        baseline_payload=baseline,
    )
    _write_json(_analytics_file(round_name), analytics)
    _analytics_report_file(round_name).parent.mkdir(parents=True, exist_ok=True)
    _analytics_report_file(round_name).write_text(markdown, encoding="utf-8")
    return analytics
