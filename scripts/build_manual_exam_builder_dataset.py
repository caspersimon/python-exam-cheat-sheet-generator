from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DRAFT_DIR = ROOT / "data" / "manual_curation_drafts"
OUTPUT_PATH = ROOT / "data" / "exam_builder_topics.json"

PARENT_TOPIC_ORDER = [
    ("python-foundations", "Python Foundations", "Core syntax, objects, operators, and condition rules that keep showing up in the early exam questions."),
    ("collections-and-iteration", "Collections and Iteration", "Lists, sets, dictionaries, loops, and comprehension patterns that help you read Python data flow quickly."),
    ("functions-and-program-flow", "Functions and Program Flow", "Function headers, calling rules, scope, returns, and higher-order patterns."),
    ("strings-and-output", "Strings and Output", "String mechanics, common methods, and compact output-formatting patterns."),
    ("pandas-data-work", "Pandas Data Work", "The small set of DataFrame and Series patterns that matter most under exam pressure."),
    ("datetime-and-time-logic", "Datetime and Time Logic", "Parsing, formatting, and doing date arithmetic without turning datetimes into strings too early."),
    ("object-oriented-python", "Object-Oriented Python", "Class fundamentals, comparison logic, and inheritance patterns."),
]

MAIN_TOPIC_META = {
    "python-basics": {"main_week": 1, "related_weeks": [1], "topic_order": 1},
    "objects-and-names": {"main_week": 1, "related_weeks": [1, 2], "topic_order": 2},
    "operators-and-truth": {"main_week": 1, "related_weeks": [1, 2], "topic_order": 3},
    "conditions": {"main_week": 2, "related_weeks": [2, 3], "topic_order": 4},
    "lists-and-sets": {"main_week": 2, "related_weeks": [1, 2], "topic_order": 5},
    "dictionaries-and-mappings": {"main_week": 2, "related_weeks": [2, 6], "topic_order": 6},
    "loops": {"main_week": 2, "related_weeks": [2, 6], "topic_order": 7},
    "comprehensions": {"main_week": 6, "related_weeks": [2, 6], "topic_order": 8},
    "functions-and-imports": {"main_week": 3, "related_weeks": [1, 3], "topic_order": 9},
    "flexible-arguments-and-kwargs": {"main_week": 3, "related_weeks": [3], "topic_order": 10},
    "scope-and-return-behavior": {"main_week": 3, "related_weeks": [3], "topic_order": 11},
    "lambda-and-higher-order-patterns": {"main_week": 3, "related_weeks": [3], "topic_order": 12},
    "string-fundamentals": {"main_week": 4, "related_weeks": [1, 4], "topic_order": 13},
    "string-operations-and-methods": {"main_week": 4, "related_weeks": [4], "topic_order": 14},
    "output-formatting": {"main_week": 4, "related_weeks": [3, 4], "topic_order": 15},
    "pandas-core-structures": {"main_week": 5, "related_weeks": [5], "topic_order": 16},
    "inspecting-and-selecting-data": {"main_week": 5, "related_weeks": [5], "topic_order": 17},
    "working-with-values": {"main_week": 5, "related_weeks": [5], "topic_order": 18},
    "datetime-parsing-and-formatting": {"main_week": 6, "related_weeks": [6], "topic_order": 19},
    "datetime-arithmetic-and-comparisons": {"main_week": 6, "related_weeks": [6], "topic_order": 20},
    "oop-fundamentals": {"main_week": 4, "related_weeks": [4], "topic_order": 21},
    "oop-comparison-logic": {"main_week": 4, "related_weeks": [4], "topic_order": 22},
    "inheritance-and-class-relationships": {"main_week": 4, "related_weeks": [4], "topic_order": 23},
}

SECTION_META = {
    "must_know": ("Must Know", "The fastest, densest references you should reach for first.", 4),
    "exam_patterns": ("Exam Patterns", "Recurring traps, worked comparisons, and exam-style patterns worth recognizing quickly.", 4),
    "useful_backup": ("Useful Backup", "Support material to add when a narrower question still leaves a gap.", 3),
}


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "item"


def load_parent_drafts() -> list[dict[str, Any]]:
    drafts: list[dict[str, Any]] = []
    for path in sorted(DRAFT_DIR.glob("*.json")):
        raw = json.loads(path.read_text(encoding="utf-8"))
        drafts.extend(normalize_parent_draft(raw, path.name))
    return drafts


def normalize_parent_draft(raw: Any, filename: str) -> list[dict[str, Any]]:
    if isinstance(raw, list):
        parents: list[dict[str, Any]] = []
        for entry in raw:
            if isinstance(entry, dict):
                parents.append(
                    {
                        "id": String(entry.get("id") or slugify(entry.get("title") or filename)),
                        "title": String(entry.get("title") or "Topic Group"),
                        "summary": String(entry.get("summary") or ""),
                        "main_topics": entry.get("main_topics", []),
                        "source_refs": {"draft_file": filename},
                    }
                )
        return parents

    if not isinstance(raw, dict):
        return []

    if "topics" in raw:
        main_topics = []
        for topic in raw.get("topics", []):
            section_keys = [
                key
                for key, value in topic.items()
                if key not in {"id", "title", "summary", "source_refs", "source_ids"} and isinstance(value, list)
            ]
            main_topics.append(
                {
                    "id": topic["id"],
                    "title": topic["title"],
                    "summary": topic.get("summary", ""),
                    "sections": {key: topic.get(key, []) for key in section_keys},
                    "source_refs": {
                        "draft_file": filename,
                        "source_ids": topic.get("source_ids", []),
                    },
                }
            )
        return [
            {
                "id": raw.get("parent_topic_id") or slugify(raw.get("parent_topic_title") or filename),
                "title": raw.get("parent_topic_title") or "Topic Group",
                "summary": raw.get("summary", ""),
                "main_topics": main_topics,
                "source_refs": {"draft_file": filename},
            }
        ]

    return [
        {
            "id": raw.get("id") or raw.get("parent_topic_id") or slugify(raw.get("title") or raw.get("parent_topic_title") or filename),
            "title": raw.get("title") or raw.get("parent_topic_title") or "Topic Group",
            "summary": raw.get("summary") or "",
            "main_topics": raw.get("main_topics", []),
            "source_refs": {"draft_file": filename},
        }
    ]


def String(value: Any) -> str:
    return str(value or "").strip()


def build_parent_topic(parent_id: str, title: str, summary: str, draft_lookup: dict[str, dict[str, Any]]) -> dict[str, Any]:
    draft = draft_lookup.get(parent_id, {})
    source_refs = draft.get("source_refs", {})
    main_topics = draft.get("main_topics", [])
    return {
        "id": parent_id,
        "title": title,
        "summary": String(draft.get("summary") or summary),
        "source_refs": source_refs,
        "main_topics": [build_main_topic(parent_id, title, topic) for topic in main_topics],
    }


def build_main_topic(parent_id: str, parent_title: str, topic: dict[str, Any]) -> dict[str, Any]:
    topic_id = String(topic.get("id"))
    meta = MAIN_TOPIC_META.get(topic_id, {"main_week": 0, "related_weeks": [], "topic_order": 999})
    raw_sections = topic.get("sections", {})
    sections = []
    for key, section_payload in iterate_section_payloads(raw_sections):
        raw_items = extract_section_items(section_payload)
        normalized_items = normalize_section_items(raw_items)
        if not normalized_items:
            continue
        title_label, description, default_visible = section_defaults(key, section_payload)
        snippets = [build_snippet(parent_title, topic.get("title"), key, idx + 1, item) for idx, item in enumerate(normalized_items)]
        sections.append(
            {
                "key": key,
                "title": title_label,
                "description": description,
                "initial_visible_count": min(default_visible, len(snippets)),
                "snippets": snippets,
            }
        )

    search_chunks = [topic.get("title", ""), topic.get("summary", "")]
    for section in sections:
        for snippet in section["snippets"]:
            search_chunks.append(snippet["title"])
            search_chunks.append(snippet.get("summary", ""))

    return {
        "id": topic_id,
        "title": String(topic.get("title")),
        "summary": String(topic.get("summary")),
        "parent_topic": parent_title,
        "main_week": meta["main_week"],
        "related_weeks": meta["related_weeks"],
        "topic_order": meta["topic_order"],
        "search_text": " ".join(chunk for chunk in search_chunks if chunk).strip(),
        "source_refs": topic.get("source_refs", {}),
        "sections": sections,
    }


def iterate_section_payloads(raw_sections: Any) -> list[tuple[str, Any]]:
    if isinstance(raw_sections, dict):
        return [(String(key), value) for key, value in raw_sections.items()]
    return []


def extract_section_items(section_payload: Any) -> Any:
    if isinstance(section_payload, dict) and "snippets" in section_payload:
        return section_payload.get("snippets", [])
    return section_payload


def section_defaults(section_key: str, section_payload: Any) -> tuple[str, str, int]:
    if isinstance(section_payload, dict):
        payload_title = String(section_payload.get("title"))
        payload_description = String(section_payload.get("description"))
        payload_visible = int(section_payload.get("initial_visible_count") or 0)
    else:
        payload_title = ""
        payload_description = ""
        payload_visible = 0

    fallback_title, fallback_description, fallback_visible = SECTION_META.get(
        section_key,
        (humanize_key(section_key), "", 3),
    )
    return (
        payload_title or fallback_title,
        payload_description or fallback_description,
        payload_visible or fallback_visible,
    )


def normalize_section_items(raw_items: Any) -> list[dict[str, Any]]:
    if isinstance(raw_items, dict) and isinstance(raw_items.get("snippets"), list):
        return [item for item in raw_items["snippets"] if isinstance(item, dict)]
    if isinstance(raw_items, dict):
        return [raw_items]
    if isinstance(raw_items, list):
        return [item for item in raw_items if isinstance(item, dict)]
    return []


def humanize_key(value: str) -> str:
    parts = [part for part in String(value).replace("_", " ").replace("-", " ").split() if part]
    return " ".join(part.capitalize() for part in parts) or "Section"


def build_snippet(parent_title: str, main_topic_title: str, section_key: str, order: int, item: dict[str, Any]) -> dict[str, Any]:
    snippet_title = String(item.get("title")) or f"{main_topic_title} snippet {order}"
    snippet_id = String(item.get("id")) or f"{slugify(main_topic_title)}-{section_key}-{slugify(snippet_title)}"
    piece_defs = item.get("pieces")
    if isinstance(piece_defs, list) and piece_defs:
        pieces = [build_piece_from_structured(snippet_id, idx + 1, piece) for idx, piece in enumerate(piece_defs) if isinstance(piece, dict)]
    else:
        pieces = build_pieces_from_item(snippet_id, snippet_title, item)
    return {
        "id": snippet_id,
        "title": snippet_title,
        "order": order,
        "snippet_type": infer_snippet_type(item, pieces),
        "parent_topic": parent_title,
        "main_topic": String(main_topic_title),
        "summary": String(item.get("summary")),
        "source_refs": gather_source_refs(item),
        "pieces": pieces,
    }


def gather_source_refs(item: dict[str, Any]) -> list[Any]:
    refs: list[Any] = []
    for key in ("source_refs", "source_ids", "source_basis", "source_snippet_ids"):
        value = item.get(key)
        if isinstance(value, list):
            refs.extend(value)
        elif isinstance(value, dict) and value:
            refs.append(value)
        elif value:
            refs.append(value)
    return refs


def build_piece_from_structured(snippet_id: str, order: int, piece: dict[str, Any]) -> dict[str, Any]:
    content = piece.get("content", {})
    if piece.get("piece_type") == "reference_table":
        content = {
            "text": decode_escaped_text(String(content.get("text"))),
            "headers": content.get("headers", []),
            "rows": content.get("rows", []),
        }
    elif piece.get("piece_type") == "code_example":
        content = {
            "text": decode_escaped_text(String(content.get("text") or content.get("note"))),
            "code": decode_escaped_code(String(content.get("code"))),
            "output": decode_escaped_text(String(content.get("output"))),
        }
    elif piece.get("piece_type") == "explanation":
        content = {"text": decode_escaped_text(String(content.get("text")))}
    return {
        "id": String(piece.get("id")) or f"{snippet_id}-piece-{order}",
        "piece_type": String(piece.get("piece_type")) or "explanation",
        "title": String(piece.get("title")) or f"Piece {order}",
        "order": order,
        "content": content,
        "selectable": piece.get("selectable", True),
        "source_refs": gather_source_refs(piece),
    }


def build_pieces_from_item(snippet_id: str, snippet_title: str, item: dict[str, Any]) -> list[dict[str, Any]]:
    content = item.get("content", {}) if isinstance(item.get("content"), dict) else {}
    pieces: list[dict[str, Any]] = []
    next_order = 1

    table = content.get("table") if isinstance(content.get("table"), dict) else None
    has_table = table or (isinstance(content.get("headers"), list) and isinstance(content.get("rows"), list))
    if has_table:
        table_data = table or {"headers": content.get("headers", []), "rows": content.get("rows", [])}
        pieces.append(
            {
                "id": f"{snippet_id}-table",
                "piece_type": "reference_table",
                "title": snippet_title,
                "order": next_order,
                "content": {
                    "text": decode_escaped_text(String(content.get("text"))),
                    "headers": table_data.get("headers", []),
                    "rows": table_data.get("rows", []),
                },
                "selectable": True,
                "source_refs": gather_source_refs(item),
            }
        )
        next_order += 1

    code_text_bits: list[str] = []
    direct_text = decode_escaped_text(String(item.get("text")))
    direct_code = decode_escaped_code(String(item.get("code")))
    if String(content.get("text")):
        code_text_bits.append(decode_escaped_text(String(content.get("text"))))
    elif direct_text:
        code_text_bits.append(direct_text)
    if String(content.get("note")):
        code_text_bits.append(f"Note: {decode_escaped_text(String(content.get('note')))}")
    if item.get("watch_out"):
        code_text_bits.append("Watch out: " + "; ".join(str(x) for x in item["watch_out"]))
    if String(content.get("anti_pattern")):
        code_text_bits.append(f"Avoid: {decode_escaped_text(String(content.get('anti_pattern')))}")

    code = decode_escaped_code(String(content.get("code") or direct_code or item.get("example") or item.get("pattern")))
    if code and looks_like_code(code):
        pieces.append(
            {
                "id": f"{snippet_id}-code",
                "piece_type": "code_example",
                "title": snippet_title,
                "order": next_order,
                "content": {
                    "text": " ".join(bit for bit in code_text_bits if bit).strip(),
                    "code": code,
                    "output": "",
                },
                "selectable": True,
                "source_refs": gather_source_refs(item),
            }
        )
        next_order += 1

    explanation_bits: list[str] = []
    for key in ("summary", "text", "why_kept", "why_backup"):
        value = item.get(key)
        if value:
            explanation_bits.append(decode_escaped_text(String(value)))
    if content.get("text") and not code:
        explanation_bits.append(decode_escaped_text(String(content.get("text"))))
    if code and not looks_like_code(code):
        explanation_bits.append(code)
    if String(item.get("anti_pattern")):
        explanation_bits.append(f"Avoid: {decode_escaped_text(String(item.get('anti_pattern')))}")
    if item.get("watch_out"):
        explanation_bits.append("Watch out: " + "; ".join(str(x) for x in item["watch_out"]))

    if not pieces or (explanation_bits and not table and not code):
        text = " ".join(bit for bit in explanation_bits if bit).strip()
        if text:
            pieces.append(
                {
                    "id": f"{snippet_id}-text",
                    "piece_type": "explanation",
                    "title": snippet_title,
                    "order": next_order,
                    "content": {"text": text},
                    "selectable": True,
                    "source_refs": gather_source_refs(item),
                }
            )

    return pieces


def infer_snippet_type(item: dict[str, Any], pieces: list[dict[str, Any]]) -> str:
    if any(piece["piece_type"] == "past_exam_piece" for piece in pieces):
        return "past_exam_question"
    return "general_snippet"


def decode_escaped_text(value: str) -> str:
    return (
        String(value)
        .replace("\\r\\n", "\n")
        .replace("\\n", "\n")
        .replace("\\t", "\t")
    )


def decode_escaped_code(value: str) -> str:
    return decode_escaped_text(value)


def looks_like_code(value: str) -> bool:
    text = String(value)
    if "\n" in text:
        return True
    return bool(
        re.search(
            r"(def |class |for |while |if |elif |else:|return\b|print\(|import\b|from\b|lambda\b|=|\.loc\[|\.iloc\[|\(|\)|\[|\])",
            text,
        )
    )


def main() -> None:
    draft_lookup = {draft["id"]: draft for draft in load_parent_drafts()}
    parent_topics = [
        build_parent_topic(parent_id, title, summary, draft_lookup)
        for parent_id, title, summary in PARENT_TOPIC_ORDER
    ]
    payload = {
        "schema_version": "2026-03-24-manual-curation-v1",
        "generated_at": "2026-03-24",
        "meta": {
            "authoring_mode": "agent-authored manual curation",
            "source_draft_dir": str(DRAFT_DIR.relative_to(ROOT)),
        },
        "parent_topics": parent_topics,
    }
    OUTPUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
