from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export partial/insufficient evaluation questions as a readable Markdown packet.")
    parser.add_argument("--round", required=True, help="Evaluation round name, for example round2")
    parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Optional output path. Defaults to data/vision_exam_pipeline/review_packets/<round>_partial_and_insufficient.md",
    )
    return parser.parse_args()


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _exam_label(exam_id: str) -> str:
    return exam_id.replace("-", " ")


def _snippet_label(item_id: str, items_by_id: dict[str, dict]) -> str:
    item = items_by_id.get(item_id) or {}
    snippet_label = (item.get("snippet_label") or "").strip()
    card_id = (item.get("card_id") or "").strip()
    if snippet_label and card_id:
        return f"{snippet_label} [{card_id}]"
    if snippet_label:
        return snippet_label
    if card_id:
        return card_id
    return item_id


def _format_options(options: dict[str, str]) -> list[str]:
    lines: list[str] = []
    for key in sorted(options):
        value = (options.get(key) or "").strip()
        lines.append(f"- `{key}`: {value}")
    return lines


def _format_ranked_items(title: str, entries: list[dict], items_by_id: dict[str, dict]) -> list[str]:
    lines = [f"**{title}**"]
    if not entries:
        lines.append("- None recorded.")
        return lines
    for entry in entries:
        item_id = (entry.get("item_id") or "").strip()
        rationale = (entry.get("rationale") or "").strip()
        label = _snippet_label(item_id, items_by_id)
        lines.append(f"- `{item_id}`: {label}")
        if rationale:
            lines.append(f"  Why: {rationale}")
    return lines


def _format_missing_concepts(missing_concepts: list[str]) -> str:
    cleaned = [concept.strip() for concept in missing_concepts if concept and concept.strip()]
    if not cleaned:
        return "None explicitly listed."
    return "; ".join(cleaned)


def build_gap_report(round_name: str) -> tuple[str, Path]:
    evaluation_path = ROOT / "data/vision_exam_pipeline/evaluations" / f"{round_name}.json"
    evaluation_payload = _load_json(evaluation_path)
    items_path = ROOT / "data/vision_exam_pipeline/selectable_items_snapshot.json"
    items = _load_json(items_path)
    items_by_id = {
        (item.get("item_id") or "").strip(): item
        for item in items
        if isinstance(item, dict) and (item.get("item_id") or "").strip()
    }

    questions = [
        question
        for question in evaluation_payload.get("questions", [])
        if isinstance(question, dict)
        and (question.get("answerability") or {}).get("status") in {"partial", "insufficient"}
    ]

    status_counts = Counter((question.get("answerability") or {}).get("status", "unknown") for question in questions)
    exam_status_counts: dict[str, Counter] = defaultdict(Counter)
    topic_status_counts: dict[str, Counter] = defaultdict(Counter)
    for question in questions:
        exam_status_counts[question.get("exam_id") or "unknown"][(question.get("answerability") or {}).get("status", "unknown")] += 1
        topic = ((question.get("question_snapshot") or {}).get("topic") or "Unknown topic").strip()
        topic_status_counts[topic][(question.get("answerability") or {}).get("status", "unknown")] += 1

    lines: list[str] = []
    lines.append(f"# {round_name.upper()} Partial and Insufficient Questions")
    lines.append("")
    lines.append(f"Generated from `data/vision_exam_pipeline/evaluations/{round_name}.json`.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Weak questions total: **{len(questions)}**")
    lines.append(f"- Partial: **{status_counts.get('partial', 0)}**")
    lines.append(f"- Insufficient: **{status_counts.get('insufficient', 0)}**")
    lines.append("")
    lines.append("## By Exam")
    lines.append("")
    for exam_id in sorted(exam_status_counts):
        counter = exam_status_counts[exam_id]
        lines.append(
            f"- `{exam_id}`: {counter.get('partial', 0)} partial, {counter.get('insufficient', 0)} insufficient"
        )
    lines.append("")
    lines.append("## By Topic")
    lines.append("")
    for topic, counter in sorted(
        topic_status_counts.items(),
        key=lambda item: (-(item[1].get("partial", 0) + item[1].get("insufficient", 0)), item[0].lower()),
    ):
        lines.append(
            f"- {topic}: {counter.get('partial', 0)} partial, {counter.get('insufficient', 0)} insufficient"
        )
    lines.append("")

    grouped: dict[str, list[dict]] = {"partial": [], "insufficient": []}
    for question in questions:
        grouped[(question.get("answerability") or {}).get("status", "unknown")].append(question)

    for status in ("insufficient", "partial"):
        group = grouped[status]
        lines.append(f"## {status.title()} Questions")
        lines.append("")
        lines.append(f"Count: **{len(group)}**")
        lines.append("")
        for question in sorted(group, key=lambda item: ((item.get("exam_id") or ""), int(item.get("question_number") or 0))):
            snapshot = question.get("question_snapshot") or {}
            answerability = question.get("answerability") or {}
            gap = question.get("gap_analysis") or {}
            qid = question.get("question_id") or ""
            exam_id = question.get("exam_id") or ""
            question_number = question.get("question_number")
            topic = snapshot.get("topic") or "Unknown topic"
            lines.append(f"### {qid}")
            lines.append("")
            lines.append(f"- Exam: `{exam_id}`")
            lines.append(f"- Question number: `{question_number}`")
            lines.append(f"- Topic: {topic}")
            lines.append(f"- Status: **{status}**")
            lines.append(f"- Confidence: `{answerability.get('confidence', 'unknown')}`")
            lines.append("")
            lines.append("**Question**")
            lines.append("")
            lines.append(snapshot.get("question", "").strip())
            lines.append("")
            if snapshot.get("options"):
                lines.append("**Options**")
                lines.extend(_format_options(snapshot.get("options") or {}))
                lines.append("")
            lines.append(f"**Correct answer:** `{snapshot.get('correct', '').strip()}`")
            explanation = (snapshot.get("explanation") or "").strip()
            if explanation:
                lines.append("")
                lines.append(f"**Official explanation:** {explanation}")
            lines.append("")
            lines.append(f"**Why not certain:** {(answerability.get('rationale') or '').strip() or 'No rationale recorded.'}")
            lines.append("")
            lines.append(f"**Gap summary:** {(gap.get('summary') or '').strip() or 'No gap summary recorded.'}")
            lines.append("")
            lines.append(f"**Missing concepts:** {_format_missing_concepts(gap.get('missing_concepts') or [])}")
            proposed_fix = (gap.get("proposed_fix") or "").strip()
            lines.append(f"**Suggested fix:** {proposed_fix or 'No proposed fix recorded.'}")
            lines.append("")
            lines.extend(_format_ranked_items("Best snippet", [question.get("best_single_snippet") or {}], items_by_id))
            lines.append("")
            lines.extend(_format_ranked_items("Top 3 snippets", question.get("top_three_snippets") or [], items_by_id))
            lines.append("")
            lines.extend(_format_ranked_items("Minimal sufficient snippets", question.get("minimal_sufficient_snippets") or [], items_by_id))
            lines.append("")
            near_identical = question.get("near_identical_past_exam_pieces") or []
            lines.append("**Near-identical past-exam pieces excluded from ranking**")
            if near_identical:
                for entry in near_identical:
                    item_id = (entry.get("item_id") or "").strip()
                    label = _snippet_label(item_id, items_by_id)
                    rationale = (entry.get("rationale") or "").strip()
                    lines.append(f"- `{item_id}`: {label}")
                    if rationale:
                        lines.append(f"  Why excluded: {rationale}")
            else:
                lines.append("- None recorded.")
            lines.append("")

    markdown = "\n".join(lines).rstrip() + "\n"
    return markdown, evaluation_path


def main() -> int:
    args = _parse_args()
    output = args.output or ROOT / "data/vision_exam_pipeline/review_packets" / f"{args.round}_partial_and_insufficient.md"
    markdown, evaluation_path = build_gap_report(args.round)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(markdown, encoding="utf-8")
    print(
        json.dumps(
            {
                "round": args.round,
                "evaluation_path": str(evaluation_path.relative_to(ROOT)),
                "output_path": str(output.relative_to(ROOT)),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
