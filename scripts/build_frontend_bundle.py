#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
NEW_DB_ROOT = ROOT / "new_database"
DB_PATH = NEW_DB_ROOT / "db" / "snippet_bank.sqlite"
CONTENT_ROOT = NEW_DB_ROOT / "content"
EXPORTS_ROOT = NEW_DB_ROOT / "exports"
BUNDLE_PATH = EXPORTS_ROOT / "frontend_bundle.json"


@dataclass
class Block:
    type: str
    payload: dict

    def to_dict(self) -> dict:
        return {"type": self.type, **self.payload}


def normalize_newlines(text: str) -> str:
    return str(text or "").replace("\r\n", "\n").replace("\r", "\n")


def split_table_row(line: str) -> list[str]:
    stripped = line.strip()
    if stripped.startswith("|"):
        stripped = stripped[1:]
    if stripped.endswith("|"):
        stripped = stripped[:-1]
    return [cell.strip() for cell in stripped.split("|")]


def is_table_separator(line: str) -> bool:
    cells = split_table_row(line)
    if not cells:
        return False
    return all(re.fullmatch(r":?-{3,}:?", cell or "") for cell in cells)


def parse_markdown_blocks(markdown: str) -> list[dict]:
    text = normalize_newlines(markdown).strip("\n")
    if not text.strip():
        return []

    lines = text.split("\n")
    blocks: list[Block] = []
    index = 0

    while index < len(lines):
        line = lines[index]
        stripped = line.strip()

        if not stripped:
            index += 1
            continue

        if stripped.startswith("```"):
            language = stripped[3:].strip()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].strip().startswith("```"):
                code_lines.append(lines[index])
                index += 1
            if index < len(lines):
                index += 1
            blocks.append(Block("code", {"language": language, "code": "\n".join(code_lines).rstrip()}))
            continue

        if (
            index + 1 < len(lines)
            and "|" in stripped
            and "|" in lines[index + 1]
            and is_table_separator(lines[index + 1])
        ):
            header = split_table_row(lines[index])
            rows: list[list[str]] = []
            index += 2
            while index < len(lines) and lines[index].strip() and "|" in lines[index]:
                rows.append(split_table_row(lines[index]))
                index += 1
            blocks.append(Block("table", {"headers": header, "rows": rows}))
            continue

        unordered_match = re.match(r"^\s*[-*+]\s+(.*)$", line)
        ordered_match = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if unordered_match or ordered_match:
            ordered = bool(ordered_match)
            items = [unordered_match.group(1).strip() if unordered_match else ordered_match.group(1).strip()]
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if not candidate.strip():
                    break
                next_unordered = re.match(r"^\s*[-*+]\s+(.*)$", candidate)
                next_ordered = re.match(r"^\s*\d+[.)]\s+(.*)$", candidate)
                if ordered and next_ordered:
                    items.append(next_ordered.group(1).strip())
                    index += 1
                    continue
                if not ordered and next_unordered:
                    items.append(next_unordered.group(1).strip())
                    index += 1
                    continue
                if re.match(r"^\s{2,}\S", candidate):
                    items[-1] = f"{items[-1]}\n{candidate.strip()}"
                    index += 1
                    continue
                break
            blocks.append(Block("list", {"ordered": ordered, "items": items}))
            continue

        paragraph_lines = [stripped.removeprefix("> ").strip()]
        index += 1
        while index < len(lines):
            candidate = lines[index]
            candidate_stripped = candidate.strip()
            if not candidate_stripped:
                break
            if candidate_stripped.startswith("```"):
                break
            if (
                index + 1 < len(lines)
                and "|" in candidate_stripped
                and "|" in lines[index + 1]
                and is_table_separator(lines[index + 1])
            ):
                break
            if re.match(r"^\s*[-*+]\s+", candidate) or re.match(r"^\s*\d+[.)]\s+", candidate):
                break
            paragraph_lines.append(candidate_stripped.removeprefix("> ").strip())
            index += 1
        blocks.append(Block("paragraph", {"text": "\n".join(paragraph_lines).strip()}))

    return [block.to_dict() for block in blocks if block.payload]


def read_markdown(path: Path) -> str:
    if not path.exists():
        raise FileNotFoundError(f"Markdown file is missing: {path}")
    return path.read_text(encoding="utf-8")


def list_lookup(connection: sqlite3.Connection, query: str) -> dict[str, list[str]]:
    results: dict[str, list[str]] = {}
    for owner, value in connection.execute(query):
        results.setdefault(str(owner), []).append(str(value))
    return results


def load_bundle() -> dict:
    if not DB_PATH.exists():
        raise FileNotFoundError(f"Missing SQLite database: {DB_PATH}")

    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    try:
        snippet_keywords = list_lookup(connection, "select snippet_slug, keyword from snippet_keywords order by keyword")
        snippet_traps = list_lookup(connection, "select snippet_slug, trap_slug from snippet_traps order by trap_slug")
        piece_traps = list_lookup(connection, "select piece_id, trap_slug from piece_traps order by trap_slug")

        trap_labels = {
            str(row["trap_slug"]): str(row["label"] or "").strip()
            for row in connection.execute("select trap_slug, label from trap_catalog")
        }

        pieces_by_snippet: dict[str, list[dict]] = {}
        for row in connection.execute("select * from pieces order by snippet_slug, sort_order, piece_id"):
            body_path = NEW_DB_ROOT / str(row["body_path"])
            body_markdown = read_markdown(body_path)
            piece_id = str(row["piece_id"])
            traps = piece_traps.get(piece_id, [])
            pieces_by_snippet.setdefault(str(row["snippet_slug"]), []).append(
                {
                    "piece_id": piece_id,
                    "piece_slug": str(row["piece_slug"]),
                    "sort_order": int(row["sort_order"] or 0),
                    "title": str(row["title"] or "").strip(),
                    "kind": str(row["kind"] or "").strip(),
                    "role": str(row["role"] or "").strip(),
                    "default_selected": bool(int(row["default_selected"] or 0)),
                    "question_ref_count": int(row["question_ref_count"] or 0),
                    "body_markdown": body_markdown,
                    "body_blocks": parse_markdown_blocks(body_markdown),
                    "trap_slugs": traps,
                    "trap_labels": [trap_labels.get(slug, slug.replace("-", " ")) for slug in traps],
                    "body_path": str(row["body_path"]),
                }
            )

        snippets_by_subtopic: dict[str, list[dict]] = {}
        for row in connection.execute("select * from snippets order by topic_slug, subtopic_slug, sort_order, snippet_slug"):
            readme_path = NEW_DB_ROOT / str(row["readme_path"])
            if not readme_path.exists():
                raise FileNotFoundError(f"Snippet README is missing: {readme_path}")

            snippet_slug = str(row["snippet_slug"])
            pieces = pieces_by_snippet.get(snippet_slug, [])
            snippet_trap_slugs = sorted({*snippet_traps.get(snippet_slug, []), *[slug for piece in pieces for slug in piece["trap_slugs"]]})
            snippets_by_subtopic.setdefault(str(row["subtopic_slug"]), []).append(
                {
                    "slug": snippet_slug,
                    "title": str(row["title"] or "").strip(),
                    "summary": str(row["summary"] or "").strip(),
                    "why": str(row["why"] or "").strip(),
                    "default_priority": int(row["default_priority"] or 0),
                    "difficulty": str(row["difficulty"] or "").strip(),
                    "course_phase": str(row["course_phase"] or "").strip(),
                    "recurrence_level": str(row["recurrence_level"] or "").strip(),
                    "exam_family_count": int(row["exam_family_count"] or 0),
                    "question_ref_count": int(row["question_ref_count"] or 0),
                    "piece_count": int(row["piece_count"] or len(pieces)),
                    "keywords": snippet_keywords.get(snippet_slug, []),
                    "trap_slugs": snippet_trap_slugs,
                    "trap_labels": [trap_labels.get(slug, slug.replace("-", " ")) for slug in snippet_trap_slugs],
                    "readme_path": str(row["readme_path"]),
                    "content_dir": str(row["content_dir"]),
                    "pieces": pieces,
                }
            )

        subtopics_by_topic: dict[str, list[dict]] = {}
        for row in connection.execute("select * from subtopics order by topic_slug, sort_order, subtopic_slug"):
            subtopics_by_topic.setdefault(str(row["topic_slug"]), []).append(
                {
                    "slug": str(row["subtopic_slug"]),
                    "title": str(row["title"] or "").strip(),
                    "description": str(row["description"] or "").strip(),
                    "sort_order": int(row["sort_order"] or 0),
                    "snippet_count": int(row["snippet_count"] or 0),
                    "snippets": snippets_by_subtopic.get(str(row["subtopic_slug"]), []),
                }
            )

        topics = []
        for row in connection.execute("select * from topics order by sort_order, topic_slug"):
            topic_slug = str(row["topic_slug"])
            topics.append(
                {
                    "topic_slug": topic_slug,
                    "title": str(row["title"] or "").strip(),
                    "description": str(row["description"] or "").strip(),
                    "sort_order": int(row["sort_order"] or 0),
                    "snippet_count": int(row["snippet_count"] or 0),
                    "subtopics": subtopics_by_topic.get(topic_slug, []),
                }
            )

        return {
            "bundle_version": "new-database-v1",
            "source": {
                "db_path": str(DB_PATH.relative_to(ROOT)),
                "content_root": str(CONTENT_ROOT.relative_to(ROOT)),
            },
            "topics": topics,
        }
    finally:
        connection.close()


def validate_bundle(bundle: dict) -> None:
    topic_count = 0
    subtopic_count = 0
    snippet_count = 0
    piece_count = 0
    seen_piece_ids: set[str] = set()

    for topic in bundle["topics"]:
        topic_count += 1
        for subtopic in topic["subtopics"]:
            subtopic_count += 1
            for snippet in subtopic["snippets"]:
                snippet_count += 1
                for piece in snippet["pieces"]:
                    piece_count += 1
                    piece_id = piece["piece_id"]
                    if piece_id in seen_piece_ids:
                        raise ValueError(f"Duplicate piece_id in bundle: {piece_id}")
                    seen_piece_ids.add(piece_id)

    print(
        json.dumps(
            {
                "topics": topic_count,
                "subtopics": subtopic_count,
                "snippets": snippet_count,
                "pieces": piece_count,
                "bundle_path": str(BUNDLE_PATH.relative_to(ROOT)),
            },
            indent=2,
        )
    )


def main() -> None:
    EXPORTS_ROOT.mkdir(parents=True, exist_ok=True)
    bundle = load_bundle()
    validate_bundle(bundle)
    BUNDLE_PATH.write_text(json.dumps(bundle, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
