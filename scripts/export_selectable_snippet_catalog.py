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
    parser = argparse.ArgumentParser(description="Export the full selectable snippet catalog as a readable Markdown file.")
    parser.add_argument(
        "--snapshot",
        type=Path,
        default=ROOT / "data/vision_exam_pipeline/selectable_items_snapshot.json",
        help="Path to the selectable items snapshot JSON.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "data/vision_exam_pipeline/review_packets/selectable_snippet_catalog.md",
        help="Output Markdown path.",
    )
    parser.add_argument("--preview-chars", type=int, default=220, help="Maximum preview characters per piece.")
    return parser.parse_args()


def _load_items(path: Path) -> list[dict]:
    return json.loads(path.read_text(encoding="utf-8"))


def _preview(text: str, limit: int) -> str:
    cleaned = " ".join((text or "").split())
    if len(cleaned) <= limit:
        return cleaned
    return cleaned[: limit - 1].rstrip() + "…"


def build_catalog(snapshot_path: Path, *, preview_chars: int) -> str:
    items = _load_items(snapshot_path)
    family_groups: dict[str, dict] = {}
    week_counts = Counter()
    bucket_counts = Counter()

    for item in items:
        snippet_id = (item.get("snippet_id") or "").strip()
        if not snippet_id:
            continue
        entry = family_groups.setdefault(
            snippet_id,
            {
                "snippet_id": snippet_id,
                "snippet_label": (item.get("snippet_label") or "").strip() or snippet_id,
                "card_id": (item.get("card_id") or "").strip(),
                "topic": (item.get("topic") or "").strip(),
                "week": item.get("week"),
                "pieces": [],
            },
        )
        entry["pieces"].append(item)
        if item.get("week") is not None:
            week_counts[item.get("week")] += 1
        bucket_counts[(item.get("bucket") or "unknown").strip() or "unknown"] += 1

    grouped_by_week: dict[int | str, list[dict]] = defaultdict(list)
    for family in family_groups.values():
        grouped_by_week[family.get("week") if family.get("week") is not None else "unknown"].append(family)

    lines: list[str] = []
    lines.append("# Selectable Snippet Catalog")
    lines.append("")
    lines.append("Human-readable export of the full selectable snippet snapshot used by the evaluation pipeline.")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Selectable pieces: **{len(items)}**")
    lines.append(f"- Snippet families: **{len(family_groups)}**")
    lines.append(f"- Weeks represented: **{', '.join(str(week) for week in sorted(grouped_by_week, key=lambda value: (999 if value == 'unknown' else value)))}**")
    lines.append("")
    lines.append("### Piece Counts By Bucket")
    lines.append("")
    for bucket, count in sorted(bucket_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"- `{bucket}`: {count}")
    lines.append("")
    lines.append("### Piece Counts By Week")
    lines.append("")
    for week, count in sorted(week_counts.items()):
        lines.append(f"- Week {week}: {count}")
    lines.append("")

    week_keys = sorted(grouped_by_week, key=lambda value: (999 if value == "unknown" else value, str(value)))
    for week in week_keys:
        families = grouped_by_week[week]
        families.sort(key=lambda family: ((family.get("topic") or "").lower(), (family.get("snippet_label") or "").lower(), family["snippet_id"]))
        header = f"Week {week}" if week != "unknown" else "Unknown Week"
        lines.append(f"## {header}")
        lines.append("")
        lines.append(f"Snippet families in this group: **{len(families)}**")
        lines.append("")
        for family in families:
            topic = family.get("topic") or "Unknown topic"
            card_id = family.get("card_id") or "unknown-card"
            lines.append(f"### {family['snippet_label']}")
            lines.append("")
            lines.append(f"- Snippet ID: `{family['snippet_id']}`")
            lines.append(f"- Topic: {topic}")
            lines.append(f"- Card ID: `{card_id}`")
            lines.append(f"- Piece count: `{len(family['pieces'])}`")
            lines.append("")
            for piece in sorted(family["pieces"], key=lambda item: ((item.get("bucket") or ""), (item.get("item_id") or ""))):
                item_id = (piece.get("item_id") or "").strip()
                bucket = (piece.get("bucket") or "unknown").strip() or "unknown"
                item_type = (piece.get("item_type") or "unknown").strip() or "unknown"
                subtopic_title = (piece.get("subtopic_title") or "").strip()
                preview_text = _preview(piece.get("search_text") or "", preview_chars)
                lines.append(f"- `{item_id}`")
                lines.append(f"  Bucket: `{bucket}` | Type: `{item_type}`")
                if subtopic_title:
                    lines.append(f"  Subtopic: {subtopic_title}")
                if preview_text:
                    lines.append(f"  Preview: {preview_text}")
            lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = _parse_args()
    markdown = build_catalog(args.snapshot, preview_chars=args.preview_chars)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(markdown, encoding="utf-8")
    print(
        json.dumps(
            {
                "snapshot": str(args.snapshot.relative_to(ROOT)),
                "output": str(args.output.relative_to(ROOT)),
            },
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
