from __future__ import annotations

import argparse
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COURSE_DIR = ROOT.parent / "course_files_after_midterm"
PRACTICE_EXAMS_DIR = COURSE_DIR / "practice_exams_previous_years"
DEFAULT_TMP_DIR = ROOT / "tmp" / "exam_coverage_audit"
TOPIC_CARDS_PATH = ROOT / "topic_cards.json"

EXAM_SOURCES = [
    {
        "exam_id": "sample-final-plus-answers",
        "title": "2025 Sample Final Plus Answers",
        "pdf_path": COURSE_DIR / "Sample Final plus answers.pdf",
        "expected_questions": 24,
        "group": "current-year",
    },
    {
        "exam_id": "final-exam-solutions-for-python-programming-62oop21",
        "title": "2022 Final Exam",
        "pdf_path": PRACTICE_EXAMS_DIR / "final-exam-solutions-for-python-programming-62oop21.pdf",
        "expected_questions": 24,
        "group": "previous-years",
    },
    {
        "exam_id": "final-exam-solutions-for-python-programming-course-code-308088-308234",
        "title": "2022 Final Exam Duplicate Copy",
        "pdf_path": PRACTICE_EXAMS_DIR / "final-exam-solutions-for-python-programming-course-code-308088-308234.pdf",
        "expected_questions": 24,
        "group": "previous-years",
        "duplicate_of": "final-exam-solutions-for-python-programming-62oop21",
    },
    {
        "exam_id": "final-exam-study-guide-trial-python-basics-2023",
        "title": "2023 Trial Final Study Guide",
        "pdf_path": PRACTICE_EXAMS_DIR / "final-exam-study-guide-trial-python-basics-2023.pdf",
        "expected_questions": 24,
        "group": "previous-years",
    },
    {
        "exam_id": "introduction-to-python-trial-final-exam-solutions-py22",
        "title": "2024 Trial Final",
        "pdf_path": PRACTICE_EXAMS_DIR / "introduction-to-python-trial-final-exam-solutions-py22.pdf",
        "expected_questions": 24,
        "group": "previous-years",
    },
    {
        "exam_id": "resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023",
        "title": "2023 Resit Exam Guidelines",
        "pdf_path": PRACTICE_EXAMS_DIR / "resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023.pdf",
        "expected_questions": 24,
        "group": "previous-years",
    },
    {
        "exam_id": "resit-solutions-for-introduction-to-python-35761538",
        "title": "2023 Resit Solutions",
        "pdf_path": PRACTICE_EXAMS_DIR / "resit-solutions-for-introduction-to-python-35761538.pdf",
        "expected_questions": 24,
        "group": "previous-years",
    },
    {
        "exam_id": "trial-final-exam-solutions-introduction-to-python-3077951",
        "title": "Trial Final Later-Course Focus",
        "pdf_path": PRACTICE_EXAMS_DIR / "trial-final-exam-solutions-introduction-to-python-3077951.pdf",
        "expected_questions": 24,
        "group": "previous-years",
    },
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Prepare and validate the vision-first exam coverage audit.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare = subparsers.add_parser("prepare", help="Render unique exam PDFs and write selectable-item audit packets.")
    prepare.add_argument("--tmp-dir", type=Path, default=DEFAULT_TMP_DIR)
    prepare.add_argument("--dpi", type=int, default=160)
    prepare.add_argument("--overwrite", action="store_true")

    summary = subparsers.add_parser("summary", help="Print selectable-item counts and unique exam metadata.")
    summary.add_argument("--tmp-dir", type=Path, default=DEFAULT_TMP_DIR)

    validate = subparsers.add_parser("validate-findings", help="Validate a findings JSON file against selectable item IDs.")
    validate.add_argument("--input", type=Path, required=True)

    return parser.parse_args()


def normalize_newlines(text: str | None) -> str:
    return str(text or "").replace("\r\n", "\n").replace("\r", "\n")


def looks_code_like(text: str | None) -> bool:
    value = str(text or "").strip()
    if not value:
        return False
    if "\n" in value:
        return True
    code_signals = ["=", "(", ")", "[", "]", "{", "}", ":", "+", "-", "*", "/", "%", "."]
    code_keywords = ["print", "for ", "if ", "while ", "def ", "return", "import ", "from ", "lambda", "range", "len", "sorted"]
    lower = value.lower()
    return any(signal in value for signal in code_signals) or any(lower.startswith(kw) or f" {kw}" in lower for kw in code_keywords)


def is_low_value_snippet(text: str | None) -> bool:
    value = str(text or "").strip()
    if not value:
        return True
    if "\n" in value:
        return False
    lower = value.lower()
    if lower.startswith("#"):
        return True
    low_phrases = [
        "below you will find",
        "the following",
        "function definitions start",
        "you call functions",
        "dictionaries are",
        "global and local names",
    ]
    if any(phrase in lower for phrase in low_phrases) and not looks_code_like(value):
        return True
    return not looks_code_like(value) and len(value.split()) <= 8


def load_topic_cards(path: Path = TOPIC_CARDS_PATH) -> list[dict]:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)["cards"]


def useful_lecture_snippets(card: dict) -> list[dict]:
    useful = []
    for snippet in card.get("sections", {}).get("lecture_snippets", []):
        filtered_examples = [example for example in snippet.get("code_examples", []) if not is_low_value_snippet(example.get("code", ""))]
        item = {**snippet, "code_examples": filtered_examples}
        if item.get("explanation") or item.get("question") or filtered_examples:
            useful.append(item)
    return useful


def useful_notebook_snippets(card: dict) -> list[dict]:
    useful = []
    for snippet in card.get("sections", {}).get("notebook_snippets", []):
        source = str(snippet.get("source", ""))
        has_print_call = "print(" in source
        has_outputs = bool(snippet.get("outputs"))
        if not is_low_value_snippet(source) and (not has_print_call or has_outputs):
            useful.append(snippet)
    return useful


def normalize_common_questions(card: dict) -> list[dict]:
    section = card.get("sections", {}).get("ai_common_questions", {}) or {}
    items = section.get("items", [])
    if items:
        normalized = []
        for index, item in enumerate(items, start=1):
            if not isinstance(item, dict):
                continue
            summary = str(item.get("summary") or item.get("question") or "").strip()
            detail = str(item.get("detail") or item.get("answer") or "").strip()
            extra = str(item.get("extra") or item.get("additional_info") or item.get("why") or "").strip()
            code = normalize_newlines(item.get("code")).strip()
            table = item.get("table") if isinstance(item.get("table"), dict) else None
            if not any([summary, detail, extra, code, table]):
                continue
            normalized.append(
                {
                    "id": str(item.get("id") or f"aiq-{index}"),
                    "summary": summary,
                    "detail": detail,
                    "extra": extra,
                    "code": code,
                    "table": table,
                }
            )
        return normalized
    return [
        {"id": f"aiq-{index}", "summary": str(bullet).strip(), "detail": "", "extra": "", "code": "", "table": None}
        for index, bullet in enumerate(section.get("bullets", []), start=1)
        if str(bullet).strip()
    ]


def key_point_groups(card: dict) -> list[dict]:
    groups = []
    for index, item in enumerate(card.get("sections", {}).get("key_points_to_remember", []), start=1):
        text = str(item.get("text") or "").strip()
        if not text:
            continue
        point_id = str(item.get("id") or f"kp-{index}").strip()
        details = []
        for detail_index, detail in enumerate(item.get("details") or [], start=1):
            if not isinstance(detail, dict):
                continue
            detail_id = str(detail.get("id") or f"{point_id}-d{detail_index}").strip()
            detail_text = str(detail.get("text") or "").strip()
            detail_code = normalize_newlines(detail.get("code")).strip()
            detail_table = detail.get("table") if isinstance(detail.get("table"), dict) else None
            if not detail_id or not any([detail_text, detail_code, detail_table]):
                continue
            details.append(
                {
                    "id": detail_id,
                    "title": str(detail.get("title") or "Optional detail").strip(),
                    "kind": str(detail.get("kind") or "example").strip(),
                    "text": detail_text,
                    "code": detail_code,
                    "table": detail_table,
                }
            )
        groups.append(
            {
                "id": point_id,
                "text": text,
                "subtopic_id": str(item.get("subtopic_id") or "").strip(),
                "subtopic_title": str(item.get("subtopic_title") or "").strip(),
                "details": details,
            }
        )
    return groups


def build_source_items(card: dict) -> list[dict]:
    items = []
    for item in card.get("sections", {}).get("exam_questions", []):
        items.append({"id": item.get("id"), "source_type": "exam", "priority": 0, "item": item})
    for item in useful_lecture_snippets(card):
        items.append({"id": item.get("id"), "source_type": "lecture", "priority": 1, "item": item})
    for item in useful_notebook_snippets(card):
        items.append({"id": item.get("id"), "source_type": "notebook", "priority": 2, "item": item})
    return sorted(items, key=lambda entry: entry["priority"])


def get_source_split(card: dict) -> tuple[list[dict], list[dict]]:
    all_items = build_source_items(card)
    by_id = {item["id"]: item for item in all_items if item.get("id")}
    recommended_ids = [item_id for item_id in card.get("sections", {}).get("recommended_ids", []) if item_id in by_id]
    recommended = []
    for item_id in recommended_ids:
        if not any(existing["id"] == item_id for existing in recommended):
            recommended.append(by_id[item_id])
    if not recommended and all_items:
        fallback = [item for item in all_items if item["source_type"] == "exam"][:4]
        extra = [item for item in all_items if item["source_type"] != "exam"][: max(0, 6 - len(fallback))]
        recommended = fallback + extra
    recommended_ids_set = {item["id"] for item in recommended}
    additional = [item for item in all_items if item["id"] not in recommended_ids_set]
    return recommended, additional


def table_to_text(table: dict | None) -> str:
    if not isinstance(table, dict):
        return ""
    headers = " | ".join(str(value or "").strip() for value in table.get("headers", []))
    rows = [" | ".join(str(value or "").strip() for value in row) for row in table.get("rows", []) if isinstance(row, list)]
    return "\n".join(filter(None, [headers, *rows]))


def stringify_item_payload(item_type: str, payload: dict) -> str:
    if item_type == "ai_common_question":
        return "\n".join(filter(None, [payload.get("summary"), payload.get("detail"), payload.get("extra"), payload.get("code"), table_to_text(payload.get("table"))]))
    if item_type == "key_point":
        return payload.get("text", "")
    if item_type == "key_point_detail":
        return "\n".join(filter(None, [payload.get("title"), payload.get("text"), payload.get("code"), table_to_text(payload.get("table"))]))
    if item_type == "ai_example":
        return "\n".join(filter(None, [payload.get("title"), payload.get("code"), payload.get("why"), payload.get("output")]))
    source_type = payload.get("source_type")
    source = payload.get("item", {})
    if source_type == "exam":
        options = "\n".join(source.get("options", []))
        return "\n".join(filter(None, [source.get("question"), options, source.get("correct"), source.get("explanation")]))
    if source_type == "lecture":
        examples = "\n".join(f"{example.get('description', '')}\n{example.get('code', '')}" for example in source.get("code_examples", []))
        return "\n".join(filter(None, [source.get("title"), source.get("explanation"), source.get("question"), examples]))
    outputs = "\n".join(source.get("outputs", []))
    return "\n".join(filter(None, [source.get("title"), source.get("source"), outputs]))


def iter_selectable_items(cards: list[dict]) -> list[dict]:
    items = []
    for card in cards:
        for item in normalize_common_questions(card):
            items.append(_selectable_item(card, "ai_common_question", item["id"], "aiQuestions", "direct", item))
        for group in key_point_groups(card):
            items.append(_selectable_item(card, "key_point", group["id"], "keyPoints", "direct", group))
            for detail in group["details"]:
                items.append(_selectable_item(card, "key_point_detail", detail["id"], "keyPoints", "detail", detail))
        for item in card.get("sections", {}).get("ai_examples", []):
            item_id = str(item.get("id") or "").strip()
            if item_id:
                items.append(_selectable_item(card, "ai_example", item_id, "aiExamples", "direct", item))
        recommended, additional = get_source_split(card)
        for bucket, source_items in [("recommended", recommended), ("additional", additional)]:
            for item in source_items:
                item_id = str(item.get("id") or "").strip()
                if item_id:
                    items.append(_selectable_item(card, f"source_{item['source_type']}", item_id, bucket, "source", item))
    return items


def _selectable_item(card: dict, item_type: str, item_id: str, bucket: str, selection_kind: str, payload: dict) -> dict:
    return {
        "item_id": item_id,
        "card_id": card["id"],
        "topic": card.get("topic", ""),
        "subtopic_id": payload.get("subtopic_id", ""),
        "subtopic_title": payload.get("subtopic_title", ""),
        "item_type": item_type,
        "bucket": bucket,
        "selection_kind": selection_kind,
        "search_text": stringify_item_payload(item_type, payload),
    }


def unique_exam_sources() -> list[dict]:
    return [exam for exam in EXAM_SOURCES if not exam.get("duplicate_of")]


def portable_path(path: Path, *, relative_to: Path = ROOT) -> str:
    return Path(os.path.relpath(path, relative_to)).as_posix()


def render_exam_pages(exam: dict, output_dir: Path, dpi: int, overwrite: bool) -> list[Path]:
    exam_dir = output_dir / exam["exam_id"]
    exam_dir.mkdir(parents=True, exist_ok=True)
    prefix = exam_dir / "page"
    existing_pages = sorted(exam_dir.glob("page-*.png"))
    if existing_pages and not overwrite:
        return existing_pages
    if overwrite:
        for existing in existing_pages:
            existing.unlink()
    command = ["pdftoppm", "-png", "-r", str(dpi), str(exam["pdf_path"]), str(prefix)]
    subprocess.run(command, check=True)
    return sorted(exam_dir.glob("page-*.png"))


def write_prepare_outputs(tmp_dir: Path, dpi: int, overwrite: bool) -> None:
    tmp_dir.mkdir(parents=True, exist_ok=True)
    cards = load_topic_cards()
    items = iter_selectable_items(cards)
    page_root = tmp_dir / "pages"
    manifest = {
        "topic_cards_path": portable_path(TOPIC_CARDS_PATH),
        "selectable_items_path": portable_path(tmp_dir / "selectable_items.json"),
        "current_repo_cards": len(cards),
        "unique_exam_count": len(unique_exam_sources()),
        "excluded_duplicates": [
            {"exam_id": exam["exam_id"], "duplicate_of": exam["duplicate_of"], "pdf_path": portable_path(exam["pdf_path"])}
            for exam in EXAM_SOURCES
            if exam.get("duplicate_of")
        ],
        "exams": [],
    }
    for exam in unique_exam_sources():
        pages = render_exam_pages(exam, page_root, dpi=dpi, overwrite=overwrite)
        manifest["exams"].append(
            {
                "exam_id": exam["exam_id"],
                "title": exam["title"],
                "pdf_path": portable_path(exam["pdf_path"]),
                "expected_questions": exam["expected_questions"],
                "page_count": len(pages),
                "page_image_paths": [portable_path(path) for path in pages],
            }
        )
    (tmp_dir / "selectable_items.json").write_text(json.dumps(items, indent=2), encoding="utf-8")
    (tmp_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def print_summary(tmp_dir: Path) -> None:
    cards = load_topic_cards()
    items = iter_selectable_items(cards)
    counts = {}
    for item in items:
        counts[item["item_type"]] = counts.get(item["item_type"], 0) + 1
    print(json.dumps({"cards": len(cards), "selectable_items": len(items), "counts_by_type": counts, "unique_exams": unique_exam_sources()}, indent=2, default=str))
    if (tmp_dir / "manifest.json").exists():
        print(f"\nPrepared manifest: {tmp_dir / 'manifest.json'}")


def validate_findings(path: Path) -> None:
    cards = load_topic_cards()
    valid_item_ids = {item["item_id"] for item in iter_selectable_items(cards)}
    with path.open("r", encoding="utf-8") as handle:
        findings = json.load(handle)
    unknown = []
    for exam in findings.get("exams", []):
        for question in exam.get("questions", []):
            for item_id in question.get("evidence_item_ids", []):
                if item_id not in valid_item_ids:
                    unknown.append((exam.get("exam_id"), question.get("question_number"), item_id))
    if unknown:
        raise SystemExit("Unknown selectable item ids:\n" + "\n".join(f"{exam_id} Q{number}: {item_id}" for exam_id, number, item_id in unknown))
    print(f"Validated findings successfully: {path}")


def main() -> None:
    args = parse_args()
    if args.command == "prepare":
        write_prepare_outputs(args.tmp_dir, dpi=args.dpi, overwrite=args.overwrite)
        print(f"Prepared exam coverage audit packet in {args.tmp_dir}")
    elif args.command == "summary":
        print_summary(args.tmp_dir)
    elif args.command == "validate-findings":
        validate_findings(args.input)


if __name__ == "__main__":
    main()
