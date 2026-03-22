#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pipelines.lecture_first_outline import match_outline_target, outline_for_week
from pipelines.shared.study_database import load_study_db, write_study_db
from pipelines.study_database.raw_sources import extract_pdf_text
STUDY_DB_FILE = ROOT / "data" / "study_db.json"
TOPIC_CARDS_FILE = ROOT / "topic_cards.json"
OUTPUT_FILE = ROOT / "data" / "quality" / "source_coverage_report.json"
MIDTERM_DIR = ROOT / "materials" / "exams"
POST_MIDTERM_DIR = ROOT / "materials" / "post_midterm"
PRACTICE_DIR = POST_MIDTERM_DIR / "practice_exams_previous_years"
ASSESSMENT_PAYLOAD_DIR = ROOT / "data" / "import_payloads" / "post_midterm_assessments"

HOMEWORK_FILES = [
    Path("/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/course files/Solutions week 1.txt"),
    Path("/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/course files/Solutions week 2.txt"),
    Path("/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/course files/Solutions week 3.txt"),
    Path("/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/course_files_after_midterm/Solutions week 4.txt"),
    Path("/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/course_files_after_midterm/Solutions week 5.txt"),
    Path("/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/course_files_after_midterm/Solutions week 6.txt"),
]

OLD_MIDTERM_SPECS = [
    {
        "path": MIDTERM_DIR / "trial midterm.pdf",
        "exam_label": "trial_midterm",
        "year": "2024-2025",
        "note": "Rebuilt from actual source PDF via pdftotext.",
    },
    {
        "path": MIDTERM_DIR / "2023.pdf",
        "exam_label": "midterm_2023",
        "year": "2022-2023",
        "note": "Rebuilt from actual source PDF via pdftotext.",
    },
    {
        "path": MIDTERM_DIR / "2024.pdf",
        "exam_label": "midterm_2024",
        "year": "2023-2024",
        "note": "Rebuilt from actual source PDF via pdftotext.",
    },
]

QUESTION_START_RE = re.compile(r"^Question\s+(\d+)\b(.*)$", re.IGNORECASE)
FOOTER_RE = re.compile(
    r"(?:Page \d+/\d+ .*|Downloaded by .*|Studocu.*|lOMoARcPSD\|\d+|messages\..*|Scan to open on Studocu)",
    re.IGNORECASE,
)
EXERCISE_SPLIT_RE = re.compile(r"^\s*Exercise\s+(\d+)\s*:\s*$", re.IGNORECASE | re.MULTILINE)
GENERIC_TITLE_RE = re.compile(r"^(?:notebook cell \d+|advanced_optional)\b", re.IGNORECASE)


@dataclass(slots=True)
class SourceUnit:
    unit_id: str
    source_file: str
    source_kind: str
    question_or_exercise_number: int
    prompt: str
    code_context: str
    answer_or_explanation: str
    week: int | None
    topic_id: str
    topic_title: str
    subtopic_id: str
    subtopic_title: str
    pattern_tags: list[str]


def _norm(text: Any) -> str:
    value = str(text or "").lower()
    value = re.sub(r"`+", "", value)
    value = re.sub(r"[^a-z0-9\s]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _compact(text: Any, limit: int = 240) -> str:
    value = re.sub(r"\s+", " ", str(text or "")).strip()
    if len(value) <= limit:
        return value
    return f"{value[: limit - 3].rstrip()}..."


def _safe_rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _extract_question_block_prompt(lines: list[str]) -> tuple[str, dict[str, str]]:
    prompt_lines: list[str] = []
    options: dict[str, str] = {}
    idx = 0
    while idx < len(lines):
        line = lines[idx].strip()
        if re.fullmatch(r"[A-D]", line):
            key = line
            idx += 1
            option_lines: list[str] = []
            while idx < len(lines):
                candidate = lines[idx].strip()
                if re.fullmatch(r"[A-D]", candidate):
                    break
                option_lines.append(candidate)
                idx += 1
            options[key] = re.sub(r"\s+", " ", " ".join(option_lines)).strip()
            continue
        prompt_lines.append(line)
        idx += 1
    prompt = "\n".join(line for line in prompt_lines if line).strip()
    return prompt, options


def _split_prompt_and_code(text: str) -> tuple[str, str]:
    lines = [line.rstrip() for line in str(text or "").splitlines()]
    if not lines:
        return "", ""
    prompt_lines: list[str] = []
    code_lines: list[str] = []
    code_started = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if code_started and code_lines and code_lines[-1] != "":
                code_lines.append("")
            elif prompt_lines and prompt_lines[-1] != "":
                prompt_lines.append("")
            continue
        looks_like_code = bool(
            re.search(r"[=:()\[\]{}]|^\s*(def |class |for |while |if |elif |else:|print\(|return\b|import\b|from\b)", line)
        )
        if code_started or looks_like_code:
            code_started = True
            code_lines.append(line)
        else:
            prompt_lines.append(line)
    prompt = "\n".join(prompt_lines).strip()
    code = "\n".join(code_lines).strip()
    return prompt, code


def _best_outline_match(*texts: Any, week_hint: int | None = None) -> tuple[int | None, dict[str, Any], dict[str, Any], int, list[str]]:
    weeks = [week_hint] if week_hint else list(range(1, 7))
    best: tuple[int | None, dict[str, Any], dict[str, Any], int, list[str]] | None = None
    for week in weeks:
        if not week:
            continue
        topic, subtopic, score, hits = match_outline_target(week, *texts)
        if best is None or score > best[3]:
            best = (week, topic, subtopic, score, hits)
    if best is not None:
        return best
    topic = outline_for_week(1)["topics"][0]
    subtopic = topic["subtopics"][0]
    return None, topic, subtopic, 0, []


def _clean_pdf_text(text: str) -> str:
    cleaned_lines = []
    for raw_line in str(text or "").replace("\x0c", "\n").splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            cleaned_lines.append("")
            continue
        if FOOTER_RE.search(line.strip()):
            continue
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def parse_old_midterm_pdf(path: Path, exam_label: str, year: str, note: str) -> dict[str, Any]:
    text = _clean_pdf_text(extract_pdf_text(path))
    questions: list[dict[str, Any]] = []
    current_number: int | None = None
    current_header = ""
    current_lines: list[str] = []

    def flush_current() -> None:
        nonlocal current_number, current_header, current_lines
        if current_number is None:
            return
        prompt, options = _extract_question_block_prompt(current_lines)
        week, topic, subtopic, _, hits = _best_outline_match(current_header, prompt)
        prompt_text, code_context = _split_prompt_and_code(prompt)
        questions.append(
            {
                "number": current_number,
                "topic": " / ".join(hits) if hits else subtopic["title"],
                "week": week,
                "question": prompt_text or prompt,
                "code_context": code_context,
                "options": options,
                "correct": "",
                "explanation": "",
                "note": f"Rebuilt from {path.name}; answer key not embedded in source PDF.",
            }
        )
        current_number = None
        current_header = ""
        current_lines = []

    for raw_line in text.splitlines():
        line = raw_line.strip()
        match = QUESTION_START_RE.match(line)
        if match:
            flush_current()
            current_number = int(match.group(1))
            current_header = match.group(2).strip(" -–—")
            continue
        if current_number is not None:
            current_lines.append(raw_line.rstrip())
    flush_current()

    return {
        "source": _safe_rel(path),
        "exam_label": exam_label,
        "year": year,
        "note": note,
        "questions": questions,
    }


def normalize_assessment_payload(payload_path: Path) -> dict[str, Any]:
    payload = json.loads(payload_path.read_text(encoding="utf-8"))
    source = str(payload.get("source") or "").strip()
    if source.startswith("practice_exams_previous_years/"):
        source = f"materials/post_midterm/{source}"
    elif source == "Sample Final plus answers.pdf":
        source = "materials/post_midterm/Sample Final plus answers.pdf"
    payload["source"] = source
    payload.setdefault("questions", [])
    return payload


def parse_homework_units() -> list[SourceUnit]:
    units: list[SourceUnit] = []
    for path in HOMEWORK_FILES:
        if not path.exists():
            continue
        match = re.search(r"week\s+(\d+)", path.name, re.IGNORECASE)
        week = int(match.group(1)) if match else None
        text = path.read_text(encoding="utf-8", errors="ignore")
        splits = list(EXERCISE_SPLIT_RE.finditer(text))
        for idx, found in enumerate(splits):
            start = found.end()
            end = splits[idx + 1].start() if idx + 1 < len(splits) else len(text)
            body = text[start:end].strip()
            if not body:
                continue
            prompt, code_context = _split_prompt_and_code(body)
            inferred_week, topic, subtopic, _, hits = _best_outline_match(body, week_hint=week)
            unit_id = f"hw-w{week}-ex{found.group(1)}"
            units.append(
                SourceUnit(
                    unit_id=unit_id,
                    source_file=path.as_posix(),
                    source_kind="homework_solution",
                    question_or_exercise_number=int(found.group(1)),
                    prompt=prompt or f"Homework week {week} exercise {found.group(1)}",
                    code_context=code_context,
                    answer_or_explanation=body,
                    week=inferred_week,
                    topic_id=topic["id"],
                    topic_title=topic["title"],
                    subtopic_id=subtopic["id"],
                    subtopic_title=subtopic["title"],
                    pattern_tags=hits,
                )
            )
    return units


def load_assessment_units(db: dict[str, Any]) -> list[SourceUnit]:
    units: list[SourceUnit] = []
    for exam in db.get("assessments", {}).get("exams", []):
        source = str(exam.get("source") or "").strip()
        label = str(exam.get("exam_label") or source)
        for question in exam.get("questions", []):
            week_hint = question.get("week")
            prompt = str(question.get("question") or "").strip()
            code_context = str(question.get("code_context") or "").strip()
            inferred_week, topic, subtopic, _, hits = _best_outline_match(
                question.get("topic"),
                prompt,
                question.get("explanation"),
                code_context,
                week_hint=week_hint if isinstance(week_hint, int) else None,
            )
            number = int(question.get("number") or 0)
            units.append(
                SourceUnit(
                    unit_id=f"exam-{label}-{number}",
                    source_file=source,
                    source_kind="assessment",
                    question_or_exercise_number=number,
                    prompt=prompt,
                    code_context=code_context,
                    answer_or_explanation=str(question.get("explanation") or "").strip(),
                    week=inferred_week,
                    topic_id=topic["id"],
                    topic_title=topic["title"],
                    subtopic_id=subtopic["id"],
                    subtopic_title=subtopic["title"],
                    pattern_tags=hits,
                )
            )
    return units


def rebuild_assessments(db: dict[str, Any]) -> dict[str, Any]:
    payloads_by_source: dict[str, dict[str, Any]] = {}
    for payload_path in sorted(ASSESSMENT_PAYLOAD_DIR.glob("*.json")):
        payload = normalize_assessment_payload(payload_path)
        source = str(payload.get("source") or "").strip()
        if source:
            payloads_by_source[source] = payload

    rebuilt: list[dict[str, Any]] = []
    seen_sources: set[str] = set()

    for spec in OLD_MIDTERM_SPECS:
        exam = parse_old_midterm_pdf(spec["path"], spec["exam_label"], spec["year"], spec["note"])
        rebuilt.append(exam)
        seen_sources.add(exam["source"])

    for exam in db.get("assessments", {}).get("exams", []):
        source = str(exam.get("source") or "").strip()
        if not source or source in seen_sources:
            continue
        if source in payloads_by_source:
            rebuilt.append(payloads_by_source[source])
            seen_sources.add(source)
            continue
        rebuilt.append(exam)
        seen_sources.add(source)

    for source, payload in payloads_by_source.items():
        if source not in seen_sources:
            rebuilt.append(payload)
            seen_sources.add(source)

    db.setdefault("assessments", {})["exams"] = rebuilt
    db.setdefault("knowledge", {}).setdefault("topic_analysis", {})
    db["knowledge"]["topic_analysis"]["exam_question_counts"] = {
        str(exam.get("exam_label") or exam.get("source") or "unknown"): len(exam.get("questions", []))
        for exam in rebuilt
    }
    db["knowledge"]["topic_analysis"]["exam_question_counts"]["total"] = sum(
        len(exam.get("questions", [])) for exam in rebuilt
    )
    return db


def _collect_card_items(card: dict[str, Any], subtopic_id: str) -> list[tuple[str, str]]:
    sections = card.get("sections", {})
    items: list[tuple[str, str]] = []
    for item in sections.get("key_points_to_remember", []):
        if item.get("subtopic_id") in {"", subtopic_id} or not item.get("subtopic_id"):
            items.append((str(item.get("id") or ""), "key_point"))
    common = sections.get("ai_common_questions", {})
    for item in common.get("items", []):
        if item.get("subtopic_id") in {"", subtopic_id} or not item.get("subtopic_id"):
            items.append((str(item.get("id") or ""), "common_question"))
    for item in sections.get("ai_examples", []):
        if item.get("subtopic_id") in {"", subtopic_id} or not item.get("subtopic_id"):
            items.append((str(item.get("id") or ""), "example"))
    for item in sections.get("exam_questions", []):
        if item.get("subtopic_id") == subtopic_id:
            items.append((str(item.get("id") or ""), "exam_question"))
    for item in sections.get("lecture_snippets", []):
        if item.get("subtopic_id") == subtopic_id:
            items.append((str(item.get("id") or ""), "lecture"))
    for item in sections.get("notebook_snippets", []):
        if item.get("subtopic_id") == subtopic_id and not GENERIC_TITLE_RE.match(str(item.get("title") or "")):
            items.append((str(item.get("id") or ""), "source_original"))
    return [(item_id, kind) for item_id, kind in items if item_id]


def _compression_type_from_kinds(kinds: list[str]) -> str:
    if "common_question" in kinds:
        return "question_pattern"
    if "example" in kinds:
        return "code_output_example"
    if "key_point" in kinds:
        return "pattern_recipe"
    if "source_original" in kinds:
        return "source_original"
    if "lecture" in kinds:
        return "exam_trap_block"
    return "unmapped"


def build_coverage_report(db: dict[str, Any], topic_cards: dict[str, Any]) -> dict[str, Any]:
    cards_by_topic = {card.get("id"): card for card in topic_cards.get("cards", [])}
    source_units = parse_homework_units() + load_assessment_units(db)
    rows = []
    uncovered = 0

    for unit in source_units:
        card = cards_by_topic.get(unit.topic_id)
        item_pairs = _collect_card_items(card, unit.subtopic_id) if card else []
        item_ids = [item_id for item_id, _ in item_pairs[:10]]
        kinds = [kind for _, kind in item_pairs]
        covered = bool(item_ids)
        if not covered:
            uncovered += 1
        rows.append(
            {
                "unit_id": unit.unit_id,
                "source_file": unit.source_file,
                "source_kind": unit.source_kind,
                "question_or_exercise_number": unit.question_or_exercise_number,
                "prompt": unit.prompt,
                "code_context": unit.code_context,
                "answer_or_explanation": unit.answer_or_explanation,
                "week": unit.week,
                "topic": unit.topic_title,
                "subtopic": unit.subtopic_title,
                "pattern_tags": unit.pattern_tags,
                "coverage_targets": {
                    "card_id": unit.topic_id if card else "",
                    "subtopic_id": unit.subtopic_id if card else "",
                    "item_ids": item_ids,
                },
                "coverage_status": "covered" if covered else "unmapped",
                "compression_type": _compression_type_from_kinds(kinds),
            }
        )

    return {
        "meta": {
            "generated_from": ["data/study_db.json", "topic_cards.json"],
            "total_units": len(rows),
            "uncovered_units": uncovered,
        },
        "units": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Rebuild assessment coverage and update study_db/source_coverage_report.")
    parser.add_argument("--skip-db-update", action="store_true", help="Only rebuild the coverage report; do not rewrite study_db.")
    parser.add_argument("--output", type=Path, default=OUTPUT_FILE, help="Coverage report output path.")
    args = parser.parse_args()

    db = load_study_db(STUDY_DB_FILE)
    if not args.skip_db_update:
        db = rebuild_assessments(db)
        write_study_db(db, STUDY_DB_FILE)

    topic_cards = json.loads(TOPIC_CARDS_FILE.read_text(encoding="utf-8")) if TOPIC_CARDS_FILE.exists() else {"cards": []}
    report = build_coverage_report(db, topic_cards)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Wrote {args.output} with {report['meta']['total_units']} source units; "
        f"{report['meta']['uncovered_units']} remain uncovered."
    )


if __name__ == "__main__":
    main()
