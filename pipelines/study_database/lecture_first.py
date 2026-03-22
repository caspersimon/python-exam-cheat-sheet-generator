from __future__ import annotations

import copy
import hashlib
import re
from collections import Counter
from datetime import datetime
from typing import Any

from pipelines.lecture_first_outline import match_outline_target, outline_for_week

def _safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []

def _safe_str(value: Any) -> str:
    return str(value or "").strip()


def _norm(text: Any) -> str:
    value = _safe_str(text).lower()
    value = value.replace("&", " and ")
    value = re.sub(r"[^a-z0-9*+.# ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def _slugify(text: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", _norm(text))
    return value.strip("-") or "item"


def _stable_id(prefix: str, *parts: Any) -> str:
    base = " | ".join(_safe_str(part) for part in parts if _safe_str(part))
    digest = hashlib.sha1(base.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{digest}"


def _find_week_sources(week_record: dict[str, Any], needle: str) -> list[str]:
    matches = []
    for source in _safe_list(week_record.get("sources")):
        text = _safe_str(source)
        if text and needle.lower() in text.lower():
            matches.append(text)
    return matches


def _dedupe_code_examples(examples: list[dict[str, Any]]) -> list[dict[str, str]]:
    seen: set[tuple[str, str]] = set()
    deduped: list[dict[str, str]] = []
    for example in examples:
        description = _safe_str(example.get("description")) or "Code example"
        code = _safe_str(example.get("code"))
        if not code:
            continue
        key = (_norm(description), code)
        if key in seen:
            continue
        seen.add(key)
        deduped.append({"description": description, "code": code})
    return deduped


def _snippet_source_ref(source: str, source_type: str, **extra: Any) -> dict[str, Any]:
    payload = {"source": source, "source_type": source_type}
    payload.update({key: value for key, value in extra.items() if value not in (None, "", [], {})})
    return payload


def _looks_low_value_text(text: str) -> bool:
    value = _safe_str(text)
    if not value:
        return True
    if "\n" in value:
        return False
    lower = value.lower()
    if lower.startswith("#"):
        return True
    if len(value.split()) <= 8:
        return True
    for phrase in [
        "below you will find",
        "the following",
        "function definitions start",
        "you call functions",
        "dictionaries are",
        "global and local names",
    ]:
        if phrase in lower:
            return True
    return False


def _make_knowledge_snippet(
    *,
    week: int,
    source: str,
    source_type: str,
    title: str,
    content: str,
    code_examples: list[dict[str, Any]] | None = None,
    original_id: str,
    confidence: int,
    matched_tags: list[str],
    migrated_from: str,
) -> dict[str, Any]:
    return {
        "id": _stable_id("ks", week, source_type, original_id, title, content[:120]),
        "kind": "knowledge",
        "title": _safe_str(title) or "Knowledge snippet",
        "content": _safe_str(content),
        "source_type": source_type,
        "source_refs": [_snippet_source_ref(source, source_type, original_id=original_id, migrated_from=migrated_from)],
        "curation_meta": {
            "confidence": confidence,
            "matched_tags": matched_tags,
            "migrated_from": migrated_from,
        },
        "merged_from_source_ids": [original_id],
        "code_examples": _dedupe_code_examples(code_examples or []),
    }


def _make_code_snippet(
    *,
    week: int,
    source: str,
    source_type: str,
    title: str,
    content: str,
    outputs: list[str] | None,
    original_id: str,
    confidence: int,
    matched_tags: list[str],
    migrated_from: str,
) -> dict[str, Any]:
    return {
        "id": _stable_id("cs", week, source_type, original_id, title, content[:120]),
        "kind": "code",
        "title": _safe_str(title) or "Code snippet",
        "content": _safe_str(content),
        "source_type": source_type,
        "source_refs": [_snippet_source_ref(source, source_type, original_id=original_id, migrated_from=migrated_from)],
        "curation_meta": {
            "confidence": confidence,
            "matched_tags": matched_tags,
            "migrated_from": migrated_from,
        },
        "merged_from_source_ids": [original_id],
        "language": "python",
        "outputs": [_safe_str(item) for item in _safe_list(outputs) if _safe_str(item)],
    }


def _make_question_snippet(
    *,
    week: int | None,
    source: str,
    source_type: str,
    title: str,
    content: str,
    options: dict[str, Any],
    correct: str,
    explanation: str,
    code_context: str,
    original_id: str,
    confidence: int,
    matched_tags: list[str],
    migrated_from: str,
) -> dict[str, Any]:
    return {
        "id": _stable_id("qs", week or "x", source_type, original_id, title, content[:120]),
        "kind": "question",
        "title": _safe_str(title) or "Question snippet",
        "content": _safe_str(content),
        "source_type": source_type,
        "source_refs": [_snippet_source_ref(source, source_type, original_id=original_id, migrated_from=migrated_from)],
        "curation_meta": {
            "confidence": confidence,
            "matched_tags": matched_tags,
            "migrated_from": migrated_from,
        },
        "merged_from_source_ids": [original_id],
        "options": {str(key): _safe_str(value) for key, value in (options or {}).items() if _safe_str(value)},
        "correct": _safe_str(correct),
        "explanation": _safe_str(explanation),
        "code_context": _safe_str(code_context),
    }


def _merge_knowledge_snippets(snippets: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    merged: list[dict[str, Any]] = []
    merge_report: list[dict[str, Any]] = []
    for snippet in snippets:
        norm_content = _norm(snippet.get("content"))
        if not norm_content:
            continue
        match = None
        for existing in merged:
            existing_norm = _norm(existing.get("content"))
            if norm_content == existing_norm:
                match = existing
                reason = "exact_match"
                break
            if norm_content in existing_norm or existing_norm in norm_content:
                match = existing
                reason = "containment"
                break
        if not match:
            merged.append(copy.deepcopy(snippet))
            continue
        if len(snippet.get("content", "")) > len(match.get("content", "")):
            match["content"] = snippet["content"]
        match["source_refs"].extend(snippet.get("source_refs", []))
        match["merged_from_source_ids"].extend(snippet.get("merged_from_source_ids", []))
        match["code_examples"] = _dedupe_code_examples(match.get("code_examples", []) + snippet.get("code_examples", []))
        merge_report.append(
            {
                "kept_id": match["id"],
                "merged_id": snippet["id"],
                "reason": reason,
            }
        )
    for item in merged:
        item["merged_from_source_ids"] = sorted(set(item.get("merged_from_source_ids", [])))
    return merged, merge_report


def _dedupe_snippet_bucket(snippets: list[dict[str, Any]], *, content_key: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    deduped: list[dict[str, Any]] = []
    for snippet in snippets:
        marker = _norm(snippet.get(content_key))
        if not marker:
            continue
        if marker in seen:
            continue
        seen.add(marker)
        deduped.append(snippet)
    return deduped


def normalize_v3_week_payload(payload: dict[str, Any]) -> dict[str, Any]:
    week = int(payload["week"])
    outline = outline_for_week(week)
    week_out = {
        "week": week,
        "title": _safe_str(payload.get("title")) or outline["title"],
        "topics": [],
        "sources": [_safe_str(source) for source in _safe_list(payload.get("sources")) if _safe_str(source)],
    }
    if isinstance(payload.get("curation_meta"), dict):
        week_out["curation_meta"] = copy.deepcopy(payload["curation_meta"])
    for topic_index, topic in enumerate(_safe_list(payload.get("topics")), start=1):
        if not isinstance(topic, dict):
            continue
        week_out["topics"].append(
            {
                "id": _safe_str(topic.get("id")) or f"w{week}-topic-{topic_index}",
                "title": _safe_str(topic.get("title")) or f"Topic {topic_index}",
                "order": int(topic.get("order") or topic_index),
                "lecture_refs": [copy.deepcopy(ref) for ref in _safe_list(topic.get("lecture_refs")) if isinstance(ref, dict)],
                "subtopics": [
                    {
                        "id": _safe_str(subtopic.get("id")) or f"w{week}-topic-{topic_index}-subtopic-{subtopic_index}",
                        "title": _safe_str(subtopic.get("title")) or f"Subtopic {subtopic_index}",
                        "order": int(subtopic.get("order") or subtopic_index),
                        "knowledge_snippets": [copy.deepcopy(item) for item in _safe_list(subtopic.get("knowledge_snippets")) if isinstance(item, dict)],
                        "code_snippets": [copy.deepcopy(item) for item in _safe_list(subtopic.get("code_snippets")) if isinstance(item, dict)],
                        "question_snippets": [copy.deepcopy(item) for item in _safe_list(subtopic.get("question_snippets")) if isinstance(item, dict)],
                    }
                    for subtopic_index, subtopic in enumerate(_safe_list(topic.get("subtopics")), start=1)
                    if isinstance(subtopic, dict)
                ],
            }
        )
    return week_out


def convert_flat_week_to_v3(week_record: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    week = int(week_record["week"])
    outline = outline_for_week(week)
    report = {
        "week": week,
        "merged_snippet_decisions": [],
        "low_confidence_assignments": [],
        "unassigned_snippets": [],
        "source_type_counts": Counter(),
    }
    topic_map = {
        topic["id"]: {
            "id": topic["id"],
            "title": topic["title"],
            "order": index,
            "lecture_refs": [{"source": source} for source in _find_week_sources(week_record, "lecture")],
            "subtopics": [
                {
                    "id": subtopic["id"],
                    "title": subtopic["title"],
                    "order": subtopic_index,
                    "knowledge_snippets": [],
                    "code_snippets": [],
                    "question_snippets": [],
                }
                for subtopic_index, subtopic in enumerate(topic["subtopics"], start=1)
            ],
        }
        for index, topic in enumerate(outline["topics"], start=1)
    }
    subtopic_map = {
        subtopic["id"]: topic_entry["subtopics"][subtopic_index]
        for topic in outline["topics"]
        for topic_entry in [topic_map[topic["id"]]]
        for subtopic_index, subtopic in enumerate(topic["subtopics"])
    }

    lecture_source = _find_week_sources(week_record, "lecture")[:1]
    lecture_source_value = lecture_source[0] if lecture_source else f"materials/lectures/Lecture Week {week}.pptx"
    notebook_source = _find_week_sources(week_record, "notebook")[:1]
    notebook_source_value = notebook_source[0] if notebook_source else f"materials/notebooks/Notebook Week {week}.ipynb"

    for index, concept in enumerate(_safe_list(week_record.get("lecture", {}).get("concepts")), start=1):
        if not isinstance(concept, dict):
            continue
        topic, subtopic, confidence, matched_tags = match_outline_target(
            week,
            concept.get("topic"),
            concept.get("explanation"),
        )
        snippet = _make_knowledge_snippet(
            week=week,
            source=lecture_source_value,
            source_type="lecture",
            title=_safe_str(concept.get("topic")),
            content=_safe_str(concept.get("explanation")),
            code_examples=_safe_list(concept.get("code_examples")),
            original_id=f"lecture-concept-{index}",
            confidence=confidence,
            matched_tags=matched_tags,
            migrated_from="lecture.concepts",
        )
        if not snippet["content"]:
            report["unassigned_snippets"].append({"kind": "lecture_knowledge", "original_id": f"lecture-concept-{index}"})
            continue
        subtopic_map[subtopic["id"]]["knowledge_snippets"].append(snippet)
        report["source_type_counts"]["lecture_knowledge"] += 1
        if confidence == 0:
            report["low_confidence_assignments"].append({"original_id": f"lecture-concept-{index}", "target_subtopic": subtopic["id"]})

    for index, question in enumerate(_safe_list(week_record.get("lecture", {}).get("lecture_questions")), start=1):
        if not isinstance(question, dict):
            continue
        topic, subtopic, confidence, matched_tags = match_outline_target(
            week,
            question.get("topic"),
            question.get("question"),
            question.get("explanation"),
        )
        snippet = _make_question_snippet(
            week=week,
            source=lecture_source_value,
            source_type="lecture",
            title=_safe_str(question.get("topic")) or f"Lecture question {index}",
            content=_safe_str(question.get("question")),
            options=question.get("options", {}),
            correct=_safe_str(question.get("correct")),
            explanation=_safe_str(question.get("explanation")),
            code_context="",
            original_id=f"lecture-question-{index}",
            confidence=confidence,
            matched_tags=matched_tags,
            migrated_from="lecture.lecture_questions",
        )
        if not snippet["content"]:
            report["unassigned_snippets"].append({"kind": "lecture_question", "original_id": f"lecture-question-{index}"})
            continue
        subtopic_map[subtopic["id"]]["question_snippets"].append(snippet)
        report["source_type_counts"]["lecture_question"] += 1

    for cell in _safe_list(week_record.get("notebook_cells")):
        if not isinstance(cell, dict):
            continue
        cell_index = int(cell.get("cell_index") or 0)
        source_text = _safe_str(cell.get("source"))
        if not source_text:
            report["unassigned_snippets"].append({"kind": "notebook", "original_id": f"cell-{cell_index}"})
            continue
        topic, subtopic, confidence, matched_tags = match_outline_target(
            week,
            cell.get("topic"),
            source_text,
            " ".join(_safe_list(cell.get("outputs"))),
        )
        original_id = f"notebook-cell-{cell_index}"
        cell_type = _safe_str(cell.get("cell_type")).lower() or "code"
        if cell_type == "code":
            snippet = _make_code_snippet(
                week=week,
                source=notebook_source_value,
                source_type="notebook",
                title=_safe_str(cell.get("topic")) or f"Notebook cell {cell_index}",
                content=source_text,
                outputs=_safe_list(cell.get("outputs")),
                original_id=original_id,
                confidence=confidence,
                matched_tags=matched_tags,
                migrated_from="notebook_cells",
            )
            subtopic_map[subtopic["id"]]["code_snippets"].append(snippet)
            report["source_type_counts"]["notebook_code"] += 1
        else:
            if _looks_low_value_text(source_text):
                continue
            snippet = _make_knowledge_snippet(
                week=week,
                source=notebook_source_value,
                source_type="notebook",
                title=_safe_str(cell.get("topic")) or f"Notebook note {cell_index}",
                content=source_text,
                original_id=original_id,
                confidence=confidence,
                matched_tags=matched_tags,
                migrated_from="notebook_cells",
            )
            subtopic_map[subtopic["id"]]["knowledge_snippets"].append(snippet)
            report["source_type_counts"]["notebook_knowledge"] += 1
        if confidence == 0:
            report["low_confidence_assignments"].append({"original_id": original_id, "target_subtopic": subtopic["id"]})

    for topic in topic_map.values():
        for subtopic in topic["subtopics"]:
            merged, merge_report = _merge_knowledge_snippets(subtopic["knowledge_snippets"])
            subtopic["knowledge_snippets"] = merged
            subtopic["code_snippets"] = _dedupe_snippet_bucket(subtopic["code_snippets"], content_key="content")
            subtopic["question_snippets"] = _dedupe_snippet_bucket(subtopic["question_snippets"], content_key="content")
            report["merged_snippet_decisions"].extend(merge_report)

    dense_subtopics = []
    for topic in topic_map.values():
        for subtopic in topic["subtopics"]:
            total = sum(len(subtopic[key]) for key in ["knowledge_snippets", "code_snippets", "question_snippets"])
            if total >= 14:
                dense_subtopics.append({"subtopic_id": subtopic["id"], "snippet_count": total})
    report["dense_subtopics"] = dense_subtopics

    week_payload = {
        "week": week,
        "title": outline["title"],
        "topics": list(topic_map.values()),
        "sources": [_safe_str(source) for source in _safe_list(week_record.get("sources")) if _safe_str(source)],
    }
    if isinstance(week_record.get("curation_meta"), dict):
        week_payload["curation_meta"] = copy.deepcopy(week_record["curation_meta"])
    return week_payload, report


def coerce_week_payload_to_v3(week_payload: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    topics = _safe_list(week_payload.get("topics"))
    if topics and isinstance(topics[0], dict) and "subtopics" in topics[0]:
        week = normalize_v3_week_payload(week_payload)
        return week, {
            "week": int(week["week"]),
            "merged_snippet_decisions": [],
            "low_confidence_assignments": [],
            "unassigned_snippets": [],
            "dense_subtopics": [],
            "source_type_counts": {},
        }
    return convert_flat_week_to_v3(week_payload)


def migrate_study_db_to_v3(db: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    migrated_weeks = []
    migration_reports = []
    for week_record in _safe_list(db.get("weeks")):
        if not isinstance(week_record, dict):
            continue
        week_payload, report = coerce_week_payload_to_v3(week_record)
        migrated_weeks.append(week_payload)
        migration_reports.append(report)

    meta = copy.deepcopy(db.get("meta", {})) if isinstance(db.get("meta"), dict) else {}
    meta["schema_version"] = "3.0"
    meta["last_updated"] = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    meta["weeks_covered"] = [week["week"] for week in migrated_weeks]

    migrated = {
        "meta": meta,
        "weeks": migrated_weeks,
        "assessments": copy.deepcopy(db.get("assessments", {})),
        "knowledge": copy.deepcopy(db.get("knowledge", {})),
    }
    summary = {
        "schema_version": "3.0",
        "weeks": len(migrated_weeks),
        "source_type_counts": dict(sum((Counter(dict(report.get("source_type_counts", {}))) for report in migration_reports), Counter())),
        "unassigned_snippets": sum(len(report.get("unassigned_snippets", [])) for report in migration_reports),
        "low_confidence_assignments": sum(len(report.get("low_confidence_assignments", [])) for report in migration_reports),
        "merged_snippet_decisions": sum(len(report.get("merged_snippet_decisions", [])) for report in migration_reports),
    }
    return migrated, {"summary": summary, "weeks": migration_reports}
