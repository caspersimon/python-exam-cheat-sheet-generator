from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path
import re
from typing import Any

from pipelines.vision_exam_pipeline_shared import (
    ANALYTICS_DIR,
    EVALUATIONS_DIR,
    REVIEW_PACKET_DIR,
    REVIEW_PACKET_SCHEMA,
    SELECTABLE_ITEMS_FILE,
    SYNTHESIS_DIR,
    _read_json,
    _safe_dict,
    _safe_list,
    _safe_str,
    _write_json,
    portable_path,
    timestamp_utc,
)

THEME_SPECS = [
    ("strings_text_methods", "Strings, Indexing, and Text Methods", [r"\bstring", r"\bstrings", r"\bindex(?:ing)?\b", r"\bslic(?:e|ing)\b", r"\bsplit\b", r"\bjoin\b", r"\breplace\b", r"\bf-?string", r"\bislower\b", r"\bisupper\b", r"\bdigit"]),
    ("loops_iteration", "Loops, Iteration, and Comprehensions", [r"\bfor loop", r"\bwhile loop", r"\bwhile\b", r"\brange\b", r"\bzip\b", r"\benumerate\b", r"\blist comprehension", r"\bcomprehension", r"\bparallel iteration", r"\bunpacking\b", r"\bappend\b"]),
    ("functions_scope", "Functions, Returns, and Scope", [r"\breturn\b", r"\bprint\b", r"\bfunction", r"\bfunctions", r"\bargument", r"\barguments", r"\bscope\b", r"\bglobal\b", r"\blocal\b", r"\bunbound"]),
    ("oop_self_attributes", "OOP, self, and Attributes", [r"\bself\b", r"\b__init__\b", r"\bclass\b", r"\bobject", r"\bobjects", r"\battribute", r"\battributes", r"\binstance", r"\bcompare method", r"\bcurrent instance"]),
    ("pandas_core", "Pandas Core Operations", [r"\bpandas\b", r"\bdataframe\b", r"\bseries\b", r"\b\.loc\b", r"\b\.iloc\b", r"\bboolean mask", r"\bfiltering\b", r"\bcolumn\b", r"\bcolumns\b", r"\bdf\[", r"\bmap\(", r"\blambda\b"]),
    ("datetime_time", "Datetime and Timedelta", [r"\bdatetime\b", r"\btimedelta\b", r"\bstrftime\b", r"\bstrptime\b", r"\bday of year\b", r"\bmonth\b", r"\byear\b"]),
    ("dicts_tuples_sets", "Dictionaries, Tuples, and Sets", [r"\bdictionary", r"\bdictionaries", r"\bdict\b", r"\btuple", r"\btuples", r"\bset\b", r"\bsets\b", r"\b\.items\(\)", r"\bkey-value"]),
    ("operators_boolean_logic", "Operators and Boolean Logic", [r"\bboolean\b", r"\btrue\b", r"\bfalse\b", r"\bfloor division\b", r"\b//\b", r"\blogic\b", r"\bcomparison\b", r"\bcondition", r"\bconditional expression", r"\bternary"]),
    ("file_handling", "File Handling", [r"\bfile\b", r"\bopen\(", r"\bread mode\b", r"\bwrite mode\b", r"\bappend mode\b", r"\bfile handling"]),
]


def _packet_json_file(round_name: str) -> Path:
    return REVIEW_PACKET_DIR / f"{round_name}.json"


def _packet_markdown_file(round_name: str) -> Path:
    return REVIEW_PACKET_DIR / f"{round_name}.md"


def _analytics_file(round_name: str) -> Path:
    return ANALYTICS_DIR / f"{round_name}.json"


def _synthesis_file(round_name: str) -> Path:
    return SYNTHESIS_DIR / f"{round_name}.json"


def _evaluation_file(round_name: str) -> Path:
    return EVALUATIONS_DIR / f"{round_name}.json"


def _classify_theme(text: str) -> tuple[str, str]:
    lowered = text.lower()
    for theme_id, theme_name, patterns in THEME_SPECS:
        if any(re.search(pattern, lowered) for pattern in patterns):
            return theme_id, theme_name
    return "miscellaneous_exam_specific", "Miscellaneous Exam-Specific Gaps"


def _item_label(item: dict[str, Any]) -> str:
    week = int(item.get("week") or 0)
    topic = _safe_str(item.get("topic")) or "Unknown topic"
    bucket = _safe_str(item.get("bucket")) or "unknown"
    item_type = _safe_str(item.get("item_type")) or "unknown"
    return f"Week {week} • {topic} • {bucket}/{item_type}"


def _item_excerpt(item: dict[str, Any]) -> str:
    text = _safe_str(item.get("search_text")).replace("\n", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text[:180] + ("..." if len(text) > 180 else "")


def _priority_label(question_count: int, suggestion_count: int) -> str:
    if question_count >= 8 or suggestion_count >= 12:
        return "high"
    if question_count >= 4 or suggestion_count >= 6:
        return "medium"
    return "selective"


def _snippet_usage(evaluations: list[dict[str, Any]], selectable_by_id: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    usage: dict[str, Counter[str]] = defaultdict(Counter)
    for question in evaluations:
        if _safe_str(question.get("status")) != "completed":
            continue
        best_id = _safe_str(_safe_dict(question.get("best_single_snippet")).get("item_id"))
        if best_id in selectable_by_id:
            usage[best_id]["best_single_count"] += 1
        for snippet in _safe_list(question.get("top_three_snippets")):
            item_id = _safe_str(_safe_dict(snippet).get("item_id"))
            if item_id in selectable_by_id:
                usage[item_id]["top_three_count"] += 1
        for snippet in _safe_list(question.get("minimal_sufficient_snippets")):
            item_id = _safe_str(_safe_dict(snippet).get("item_id"))
            if item_id in selectable_by_id:
                usage[item_id]["minimal_set_count"] += 1

    rows = []
    for item_id, counts in usage.items():
        item = selectable_by_id[item_id]
        weighted_score = int(counts["best_single_count"] * 3 + counts["minimal_set_count"] * 2 + counts["top_three_count"])
        rows.append(
            {
                "item_id": item_id,
                "label": _item_label(item),
                "excerpt": _item_excerpt(item),
                "week": int(item.get("week") or 0),
                "topic": _safe_str(item.get("topic")),
                "bucket": _safe_str(item.get("bucket")),
                "item_type": _safe_str(item.get("item_type")),
                "best_single_count": int(counts["best_single_count"]),
                "top_three_count": int(counts["top_three_count"]),
                "minimal_set_count": int(counts["minimal_set_count"]),
                "weighted_score": weighted_score,
            }
        )
    return sorted(rows, key=lambda row: (-row["weighted_score"], -row["best_single_count"], row["item_id"]))


def build_review_packet(
    *,
    round_name: str,
    synthesis_payload: dict[str, Any],
    analytics_payload: dict[str, Any],
    evaluation_payload: dict[str, Any],
    selectable_items: list[dict[str, Any]],
) -> tuple[dict[str, Any], str]:
    selectable_by_id = {item["item_id"]: item for item in selectable_items if isinstance(item, dict) and item.get("item_id")}
    completed = [item for item in _safe_list(evaluation_payload.get("questions")) if _safe_str(_safe_dict(item).get("status")) == "completed"]
    answerability = Counter(_safe_str(_safe_dict(item.get("answerability")).get("status")) for item in completed)

    theme_map: dict[str, dict[str, Any]] = {}
    for question in completed:
        answerability_status = _safe_str(_safe_dict(question.get("answerability")).get("status"))
        if answerability_status == "certain":
            continue
        gap_analysis = _safe_dict(question.get("gap_analysis"))
        text = " ".join(
            [
                _safe_str(gap_analysis.get("summary")),
                " ".join(_safe_list(gap_analysis.get("missing_concepts"))),
                _safe_str(gap_analysis.get("proposed_fix")),
            ]
        ).strip()
        if not text:
            continue
        theme_id, theme_name = _classify_theme(text)
        entry = theme_map.setdefault(
            theme_id,
            {
                "theme_id": theme_id,
                "theme_name": theme_name,
                "question_ids": set(),
                "partial_question_ids": set(),
                "insufficient_question_ids": set(),
                "suggestion_ids": set(),
                "source_exams": set(),
                "directions": Counter(),
                "representative_gaps": [],
                "representative_suggestions": [],
            },
        )
        question_id = _safe_str(question.get("question_id"))
        entry["question_ids"].add(question_id)
        entry["source_exams"].add(_safe_str(question.get("exam_id")))
        if answerability_status == "partial":
            entry["partial_question_ids"].add(question_id)
        if answerability_status == "insufficient":
            entry["insufficient_question_ids"].add(question_id)
        gap_summary = _safe_str(gap_analysis.get("summary"))
        if gap_summary and gap_summary not in entry["representative_gaps"] and len(entry["representative_gaps"]) < 3:
            entry["representative_gaps"].append(gap_summary)

    for suggestion in _safe_list(synthesis_payload.get("suggestions")):
        if not isinstance(suggestion, dict):
            continue
        text = " ".join(
            [
                _safe_str(suggestion.get("proposal")),
                " ".join(_safe_list(suggestion.get("pros"))),
                " ".join(_safe_list(suggestion.get("cons"))),
            ]
        ).strip()
        theme_id, theme_name = _classify_theme(text)
        entry = theme_map.setdefault(
            theme_id,
            {
                "theme_id": theme_id,
                "theme_name": theme_name,
                "question_ids": set(),
                "partial_question_ids": set(),
                "insufficient_question_ids": set(),
                "suggestion_ids": set(),
                "source_exams": set(),
                "directions": Counter(),
                "representative_gaps": [],
                "representative_suggestions": [],
            },
        )
        entry["suggestion_ids"].add(_safe_str(suggestion.get("suggestion_id")))
        entry["source_exams"].update(_safe_list(suggestion.get("source_exams")))
        entry["directions"][_safe_str(suggestion.get("recommended_direction")) or "consider_instead"] += 1
        proposal = _safe_str(suggestion.get("proposal"))
        if proposal and proposal not in entry["representative_suggestions"] and len(entry["representative_suggestions"]) < 3:
            entry["representative_suggestions"].append(proposal)

    theme_rows = []
    for entry in theme_map.values():
        question_count = len(entry["question_ids"])
        suggestion_count = len(entry["suggestion_ids"])
        if question_count == 0 and suggestion_count == 0:
            continue
        theme_rows.append(
            {
                "theme_id": entry["theme_id"],
                "theme_name": entry["theme_name"],
                "priority": _priority_label(question_count, suggestion_count),
                "question_count": question_count,
                "partial_question_count": len(entry["partial_question_ids"]),
                "insufficient_question_count": len(entry["insufficient_question_ids"]),
                "suggestion_count": suggestion_count,
                "recommended_direction_counts": dict(entry["directions"]),
                "source_exam_count": len({exam for exam in entry["source_exams"] if exam}),
                "representative_gaps": entry["representative_gaps"],
                "representative_suggestions": entry["representative_suggestions"],
            }
        )
    theme_rows.sort(key=lambda row: (-row["question_count"], -row["suggestion_count"], row["theme_name"]))

    snippet_rows = _snippet_usage(completed, selectable_by_id)
    week_rows = _safe_list(analytics_payload.get("weeks"))
    top_weeks = sorted(week_rows, key=lambda row: (-int(row.get("minimal_set_unique_snippets") or 0), int(row.get("week") or 0)))
    review_sequence = []
    for index, row in enumerate(theme_rows[:10], start=1):
        direction_counts = row["recommended_direction_counts"]
        primary_direction = "add_this" if direction_counts.get("add_this", 0) >= direction_counts.get("consider_instead", 0) else "consider_instead"
        review_sequence.append(
            {
                "order": index,
                "theme_id": row["theme_id"],
                "theme_name": row["theme_name"],
                "priority": row["priority"],
                "question_count": row["question_count"],
                "suggestion_count": row["suggestion_count"],
                "suggested_direction": primary_direction,
            }
        )

    packet = {
        "schema_version": REVIEW_PACKET_SCHEMA,
        "generated_at": timestamp_utc(),
        "round": round_name,
        "ready_for_human_review": True,
        "input_paths": {
            "evaluations": portable_path(_evaluation_file(round_name)),
            "synthesis": portable_path(_synthesis_file(round_name)),
            "analytics": portable_path(_analytics_file(round_name)),
            "selectable_items": portable_path(SELECTABLE_ITEMS_FILE),
        },
        "summary": {
            "completed_evaluations": len(completed),
            "certain_count": int(answerability.get("certain", 0)),
            "partial_count": int(answerability.get("partial", 0)),
            "insufficient_count": int(answerability.get("insufficient", 0)),
            "theme_count": len(theme_rows),
            "top_snippet_count": len(snippet_rows),
        },
        "review_sequence": review_sequence,
        "themes": theme_rows,
        "top_existing_snippets": snippet_rows[:20],
        "week_summary": top_weeks,
        "recommendations": {
            "review_high_priority_themes_first": [row["theme_name"] for row in theme_rows if row["priority"] == "high"][:6],
            "hold_off_on_implementation_until_human_review": True,
            "likely_first_pass_focus": [row["theme_name"] for row in theme_rows[:5]],
        },
    }

    lines = [
        f"# Review Packet ({round_name})",
        "",
        "## What Needs Your Review",
        "",
        "- This packet condenses the round-1 synthesis into review themes instead of 151 isolated suggestions.",
        "- The goal is to decide which snippet edits/additions are worth implementing before the second evaluation round.",
        f"- Completed evaluations: `{packet['summary']['completed_evaluations']}`",
        f"- Answerability split: `certain={packet['summary']['certain_count']}`, `partial={packet['summary']['partial_count']}`, `insufficient={packet['summary']['insufficient_count']}`",
        "",
        "## Recommended Review Order",
        "",
    ]
    for row in review_sequence:
        lines.append(
            f"{row['order']}. **{row['theme_name']}** (`priority={row['priority']}`, `questions={row['question_count']}`, `suggestions={row['suggestion_count']}`, `direction={row['suggested_direction']}`)"
        )
    lines.extend(["", "## Priority Themes", ""])
    for row in theme_rows[:12]:
        direction_counts = row["recommended_direction_counts"]
        lines.append(f"### {row['theme_name']}")
        lines.append("")
        lines.append(f"- Priority: `{row['priority']}`")
        lines.append(f"- Affected questions: `{row['question_count']}` (`partial={row['partial_question_count']}`, `insufficient={row['insufficient_question_count']}`)")
        lines.append(f"- Related synthesized suggestions: `{row['suggestion_count']}`")
        lines.append(f"- Suggested direction mix: `{direction_counts}`")
        if row["representative_gaps"]:
            lines.append("- Representative gaps:")
            for gap in row["representative_gaps"]:
                lines.append(f"  - {gap}")
        if row["representative_suggestions"]:
            lines.append("- Representative suggestions:")
            for proposal in row["representative_suggestions"]:
                lines.append(f"  - {proposal}")
        lines.append("")
    lines.extend(["## Strong Existing Snippets", "", "| Rank | Snippet | Best single | Top 3 | Minimal set |", "|---|---|---:|---:|---:|"])
    for index, row in enumerate(packet["top_existing_snippets"][:15], start=1):
        lines.append(
            f"| {index} | `{row['item_id']}`<br>{row['label']} | {row['best_single_count']} | {row['top_three_count']} | {row['minimal_set_count']} |"
        )
    lines.extend(["", "## Week Coverage Snapshot", "", "| Week | Top 1 unique | Top 3 unique | Minimal-set unique | Minimal-set unused |", "|---|---:|---:|---:|---:|"])
    for row in top_weeks:
        lines.append(
            f"| {row['week']} | {row['top1_unique_snippets']} | {row['top3_unique_snippets']} | {row['minimal_set_unique_snippets']} | {row['minimal_set_unused_snippets']} |"
        )
    lines.extend(
        [
            "",
            "## Suggested Human Workflow",
            "",
            "1. Review the high-priority themes first and decide `add`, `edit existing`, or `skip`.",
            "2. Use the representative suggestions as examples, not as a forced one-to-one implementation list.",
            "3. Favor additions/edits that solve multiple question gaps rather than single-exam edge cases.",
            "4. Only after that review should the implementation round begin.",
            "",
        ]
    )
    return packet, "\n".join(lines)


def write_review_packet(
    *,
    round_name: str,
    selectable_items_path: Path = SELECTABLE_ITEMS_FILE,
) -> dict[str, Any]:
    packet, markdown = build_review_packet(
        round_name=round_name,
        synthesis_payload=_read_json(_synthesis_file(round_name)),
        analytics_payload=_read_json(_analytics_file(round_name)),
        evaluation_payload=_read_json(_evaluation_file(round_name)),
        selectable_items=_read_json(selectable_items_path),
    )
    _write_json(_packet_json_file(round_name), packet)
    _packet_markdown_file(round_name).parent.mkdir(parents=True, exist_ok=True)
    _packet_markdown_file(round_name).write_text(markdown + "\n", encoding="utf-8")
    return packet
