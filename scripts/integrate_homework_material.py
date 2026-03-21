#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import sys
from typing import Any
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from pipelines.shared import (  # noqa: E402
    flatten_study_db_for_pipeline,
    load_study_db,
    recompute_topic_analysis,
    write_study_db,
)
from pipelines.topic_cards.core import (  # noqa: E402
    clean_notebook_source,
    compact_text,
    dedupe_list,
    is_relevant,
    make_id,
    topic_key,
)
DEFAULT_HOMEWORK_DIR = ROOT / "materials" / "homework"
DEFAULT_STUDY_DB = ROOT / "data" / "study_db.json"
DEFAULT_TOPIC_CARDS = ROOT / "topic_cards.json"
DEFAULT_REPORT_FILE = ROOT / "data" / "curation_reports" / "homework_integration_report.json"
WEEK_DIR_RE = re.compile(r"^week\s+(\d+)$", re.IGNORECASE)
SOLUTION_BLOCK_RE = re.compile(r"^\s*Exercise\s+(\d+)\s*:\s*$", re.IGNORECASE)
EXERCISE_FILENAME_RE = re.compile(r"^Exercise(?:[_ ](?:(\d+)\.)?(\d+))?\.py$", re.IGNORECASE)
HOMEWORK_TOPIC_MAP: dict[int, dict[int, str]] = {
    1: {
        1: "arithmetic_operators",
        2: "arithmetic_operators",
        3: "arithmetic_operators",
        4: "strings",
        5: "boolean_operators",
        6: "type_conversion",
        7: "indexing",
        8: "indexing",
        9: "slicing",
    },
    2: {
        1: "dictionaries",
        2: "while_loops",
        3: "dictionaries",
        4: "enumerate",
        5: "zip",
        6: "dictionaries",
        7: "truthy_falsy",
        8: "conditions",
        9: "for_loops",
    },
    3: {
        1: "nested_loops",
        2: "keyword_args",
        3: "args_star",
        4: "default_args",
        5: "args_star",
        6: "function_factories",
        7: "default_args",
        8: "zip",
        9: "lambda",
    },
}
BONUS_TOPIC_MAP: dict[int, str] = {
    1: "indexing",
}
@dataclass(frozen=True)
class CandidateCell:
    week: int
    topic: str
    source_text: str
    origin: str
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Integrate homework solution snippets into study_db homework_cells and topic_cards homework_snippets."
    )
    parser.add_argument(
        "--homework-dir",
        type=Path,
        default=DEFAULT_HOMEWORK_DIR,
        help=f"Homework root directory (default: {DEFAULT_HOMEWORK_DIR}).",
    )
    parser.add_argument(
        "--study-db",
        type=Path,
        default=DEFAULT_STUDY_DB,
        help=f"Path to study_db JSON (default: {DEFAULT_STUDY_DB}).",
    )
    parser.add_argument(
        "--topic-cards",
        type=Path,
        default=DEFAULT_TOPIC_CARDS,
        help=f"Path to topic_cards JSON (default: {DEFAULT_TOPIC_CARDS}).",
    )
    parser.add_argument(
        "--report-file",
        type=Path,
        default=DEFAULT_REPORT_FILE,
        help=f"Integration report output path (default: {DEFAULT_REPORT_FILE}).",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build integration result and report without writing data files.",
    )
    return parser.parse_args()
def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
def _normalize_source(value: str) -> str:
    return value.replace("\r\n", "\n").replace("\u00a0", " ").strip()
def _strip_docstring_prefix(source: str) -> str:
    text = source.lstrip()
    if text.startswith('"""') or text.startswith("'''"):
        quote = text[:3]
        end = text.find(quote, 3)
        if end != -1:
            return text[end + 3 :].lstrip()
    return source.strip()
def _clean_solution_block(lines: list[str]) -> str:
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    cleaned: list[str] = []
    for raw in lines:
        line = raw.replace("\u00a0", " ")
        if set(line.strip()) == {"="}:
            continue
        cleaned.append(line.rstrip())
    text = "\n".join(cleaned).strip()
    return _normalize_source(text)
def parse_solution_blocks(solution_file: Path) -> dict[int, str]:
    lines = solution_file.read_text(encoding="utf-8").replace("\u00a0", " ").splitlines()
    by_exercise: dict[int, str] = {}
    current: int | None = None
    buf: list[str] = []
    def flush() -> None:
        nonlocal buf
        if current is None:
            return
        parsed = _clean_solution_block(buf)
        if parsed:
            by_exercise[current] = parsed
        buf = []
    for line in lines:
        match = SOLUTION_BLOCK_RE.match(line)
        if match:
            flush()
            current = int(match.group(1))
            continue
        if current is not None:
            buf.append(line)
    flush()
    return by_exercise
def parse_exercise_id(file_name: str) -> int | None:
    match = EXERCISE_FILENAME_RE.match(file_name)
    if not match:
        return None
    return int(match.group(2) or 0) or None
def _week_dirs(homework_dir: Path) -> list[tuple[int, Path]]:
    out: list[tuple[int, Path]] = []
    for child in homework_dir.iterdir():
        if not child.is_dir():
            continue
        match = WEEK_DIR_RE.match(child.name.strip())
        if not match:
            continue
        out.append((int(match.group(1)), child))
    return sorted(out, key=lambda item: item[0])
def _relative(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)
def _extract_bonus_source(path: Path) -> str:
    text = _normalize_source(path.read_text(encoding="utf-8"))
    stripped = _strip_docstring_prefix(text)
    return stripped or text
def build_candidates(homework_dir: Path) -> tuple[list[CandidateCell], dict[int, list[str]]]:
    all_candidates: list[CandidateCell] = []
    week_sources: dict[int, list[str]] = {}
    for week, week_dir in _week_dirs(homework_dir):
        files = sorted(path for path in week_dir.iterdir() if path.is_file() and not path.name.startswith("."))
        week_sources[week] = [_relative(path) for path in files]
        solution_file = next((path for path in files if path.name.lower().startswith("solutions week ")), None)
        solution_blocks = parse_solution_blocks(solution_file) if solution_file else {}
        for path in files:
            if path.name.lower().startswith("solutions week "):
                continue
            if path.name.lower().endswith("bonus_exercise_solved.py"):
                source_text = _extract_bonus_source(path)
                topic = BONUS_TOPIC_MAP.get(week, "homework")
                if source_text:
                    all_candidates.append(
                        CandidateCell(
                            week=week,
                            topic=topic,
                            source_text=source_text,
                            origin=_relative(path),
                        )
                    )
                continue
            exercise_id = parse_exercise_id(path.name)
            if exercise_id is None:
                continue
            topic = HOMEWORK_TOPIC_MAP.get(week, {}).get(exercise_id, "homework")
            source_text = solution_blocks.get(exercise_id)
            if not source_text:
                continue
            tagged_source = f"# source: {_relative(path)}\n{source_text}"
            all_candidates.append(
                CandidateCell(
                    week=week,
                    topic=topic,
                    source_text=_normalize_source(tagged_source),
                    origin=_relative(path),
                )
            )
    return all_candidates, week_sources
def _index_weeks(db: dict[str, Any]) -> dict[int, dict[str, Any]]:
    out: dict[int, dict[str, Any]] = {}
    weeks = [item for item in _safe_list(db.get("weeks")) if isinstance(item, dict)]
    db["weeks"] = weeks
    for week in weeks:
        try:
            week_num = int(week.get("week"))
        except (TypeError, ValueError):
            continue
        out[week_num] = week
    return out
def _source_signature(topic: str, source: str) -> tuple[str, str]:
    return (topic.strip().lower(), _normalize_source(source))
def _append_unique_sources(week_rec: dict[str, Any], new_sources: list[str]) -> int:
    existing = [src for src in _safe_list(week_rec.get("sources")) if isinstance(src, str)]
    seen = {src.lower() for src in existing}
    added = 0
    for src in new_sources:
        if not src.strip():
            continue
        key = src.lower()
        if key in seen:
            continue
        existing.append(src)
        seen.add(key)
        added += 1
    week_rec["sources"] = existing
    return added
def _append_unique_homework_cells(week_rec: dict[str, Any], candidates: list[CandidateCell]) -> int:
    cells = [cell for cell in _safe_list(week_rec.get("homework_cells")) if isinstance(cell, dict)]
    week_rec["homework_cells"] = cells
    seen = set()
    max_index = 0
    for cell in cells:
        topic = str(cell.get("topic") or "")
        source = str(cell.get("source") or "")
        seen.add(_source_signature(topic, source))
        try:
            max_index = max(max_index, int(cell.get("cell_index") or 0))
        except (TypeError, ValueError):
            continue
    added = 0
    for candidate in candidates:
        signature = _source_signature(candidate.topic, candidate.source_text)
        if signature in seen:
            continue
        max_index += 1
        cells.append(
            {
                "cell_index": max_index,
                "week": candidate.week,
                "cell_type": "code",
                "topic": candidate.topic,
                "is_advanced_optional": False,
                "source": candidate.source_text,
                "outputs": [],
                "source_origin": candidate.origin,
            }
        )
        seen.add(signature)
        added += 1
    return added
def _update_meta(db: dict[str, Any]) -> None:
    meta = db.setdefault("meta", {})
    meta.setdefault("schema_version", "2.0")
    meta["last_updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    weeks_covered = sorted(
        {
            int(item.get("week"))
            for item in _safe_list(db.get("weeks"))
            if isinstance(item, dict) and str(item.get("week", "")).isdigit()
        }
    )
    meta["weeks_covered"] = weeks_covered
    sources = [source for source in _safe_list(meta.get("sources")) if isinstance(source, str)]
    seen = {source.lower() for source in sources}
    for week in _safe_list(db.get("weeks")):
        if not isinstance(week, dict):
            continue
        for source in _safe_list(week.get("sources")):
            if not isinstance(source, str):
                continue
            key = source.lower()
            if key in seen:
                continue
            sources.append(source)
            seen.add(key)
    for exam in _safe_list(db.get("assessments", {}).get("exams")):
        if not isinstance(exam, dict):
            continue
        source = exam.get("source")
        if not isinstance(source, str):
            continue
        key = source.lower()
        if key in seen:
            continue
        sources.append(source)
        seen.add(key)
    meta["sources"] = sources
def integrate_homework_into_study_db(
    *,
    db: dict[str, Any],
    homework_dir: Path,
) -> dict[str, Any]:
    candidates, week_sources = build_candidates(homework_dir)
    by_week: dict[int, list[CandidateCell]] = {}
    for candidate in candidates:
        by_week.setdefault(candidate.week, []).append(candidate)
    week_index = _index_weeks(db)
    report: dict[str, Any] = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "homework_dir": str(homework_dir),
        "weeks": [],
        "summary": {
            "total_candidate_homework_cells": len(candidates),
            "total_added_homework_cells": 0,
            "total_added_sources": 0,
        },
    }
    for week in sorted(set(list(week_sources.keys()) + list(by_week.keys()))):
        week_rec = week_index.get(week)
        if not week_rec:
            report["weeks"].append(
                {
                    "week": week,
                    "status": "missing_week_in_study_db",
                    "candidate_homework_cells": len(by_week.get(week, [])),
                    "added_homework_cells": 0,
                    "added_sources": 0,
                }
            )
            continue
        added_sources = _append_unique_sources(week_rec, week_sources.get(week, []))
        added_homework = _append_unique_homework_cells(week_rec, by_week.get(week, []))
        report["summary"]["total_added_homework_cells"] += added_homework
        report["summary"]["total_added_sources"] += added_sources
        report["weeks"].append(
            {
                "week": week,
                "status": "updated",
                "candidate_homework_cells": len(by_week.get(week, [])),
                "added_homework_cells": added_homework,
                "added_sources": added_sources,
                "total_week_sources": len(_safe_list(week_rec.get("sources"))),
                "total_week_homework_cells": len(_safe_list(week_rec.get("homework_cells"))),
            }
        )
    _update_meta(db)
    knowledge = db.setdefault("knowledge", {})
    knowledge["topic_analysis"] = recompute_topic_analysis(flatten_study_db_for_pipeline(db))
    return report
def sync_topic_cards_homework(
    *,
    db: dict[str, Any],
    topic_cards_path: Path,
) -> dict[str, Any]:
    payload = json.loads(topic_cards_path.read_text(encoding="utf-8"))
    cards = [card for card in _safe_list(payload.get("cards")) if isinstance(card, dict)]
    materialized = flatten_study_db_for_pipeline(db)
    homeworks = [cell for cell in _safe_list(materialized.get("homeworks")) if isinstance(cell, dict)]
    added_total = 0
    by_card_counts: dict[str, int] = {}
    for card in cards:
        sections = card.setdefault("sections", {})
        sections["homework_snippets"] = []
        canonical = str(card.get("canonical_topic") or "").strip()
        if not canonical:
            canonical = topic_key(str(card.get("topic") or ""))
        snippets: list[dict[str, Any]] = []
        for cell in homeworks:
            if cell.get("is_advanced_optional"):
                continue
            topic = str(cell.get("topic") or "")
            if not topic:
                continue
            source_key = topic_key(topic)
            if not is_relevant(canonical, source_key, threshold=0.6):
                continue
            cleaned_source = clean_notebook_source(str(cell.get("source") or ""), str(cell.get("cell_type") or "code"))
            if not cleaned_source:
                continue
            snippet = {
                "id": make_id("hw", f"{cell.get('week')}-{cell.get('cell_index')}-{topic}"),
                "week": cell.get("week"),
                "cell_index": cell.get("cell_index"),
                "cell_type": cell.get("cell_type"),
                "topic": topic,
                "source": cleaned_source,
                "outputs": [compact_text(out, 400) for out in (cell.get("outputs") or [])[:2] if out and str(out).strip()],
                "source_origin": cell.get("source_origin", ""),
            }
            snippets.append(snippet)
        deduped = dedupe_list(snippets, ["id"])[:12]
        sections["homework_snippets"] = deduped
        recommended_count = min(4, max(1, (len(deduped) + 1) // 2)) if deduped else 0
        sections["homework_recommended_ids"] = [snippet.get("id") for snippet in deduped[:recommended_count] if snippet.get("id")]
        by_card_counts[str(card.get("id") or "")] = len(deduped)
        added_total += len(deduped)
    payload["cards"] = cards
    topic_cards_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    cards_with_homework = len([count for count in by_card_counts.values() if count > 0])
    return {
        "cards_total": len(cards),
        "cards_with_homework_snippets": cards_with_homework,
        "total_homework_snippets_attached": added_total,
    }
def main() -> None:
    args = parse_args()
    homework_dir = args.homework_dir.resolve()
    if not homework_dir.exists() or not homework_dir.is_dir():
        raise FileNotFoundError(f"Homework directory not found or not a directory: {homework_dir}")
    if not args.topic_cards.exists():
        raise FileNotFoundError(f"topic_cards file not found: {args.topic_cards}")
    db = load_study_db(args.study_db)
    db_before = json.loads(json.dumps(db))
    cards_before = args.topic_cards.read_text(encoding="utf-8")
    db_report = integrate_homework_into_study_db(db=db, homework_dir=homework_dir)
    if args.dry_run:
        cards_report = sync_topic_cards_homework(db=db, topic_cards_path=args.topic_cards)
        args.topic_cards.write_text(cards_before, encoding="utf-8")
        db = db_before
    else:
        write_study_db(db, args.study_db)
        cards_report = sync_topic_cards_homework(db=db, topic_cards_path=args.topic_cards)
    report = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "dry_run": bool(args.dry_run),
        "study_db": str(args.study_db),
        "topic_cards": str(args.topic_cards),
        "homework_dir": str(homework_dir),
        "study_db_integration": db_report,
        "topic_cards_sync": cards_report,
    }
    args.report_file.parent.mkdir(parents=True, exist_ok=True)
    args.report_file.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        ("Dry-run completed:" if args.dry_run else "Homework integration completed:"),
        f"added_homework_cells={db_report['summary']['total_added_homework_cells']}",
        f"added_sources={db_report['summary']['total_added_sources']}",
        f"cards_with_homework={cards_report['cards_with_homework_snippets']}",
        f"report={args.report_file}",
    )
if __name__ == "__main__":
    main()
