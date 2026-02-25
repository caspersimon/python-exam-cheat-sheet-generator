#!/usr/bin/env python3
import json
import re
import hashlib
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCE_FILE = ROOT / "study_data.json"
OUTPUT_FILE = ROOT / "topic_cards.json"

STOP_WORDS = {
    "vs",
    "versus",
    "and",
    "or",
    "the",
    "a",
    "an",
    "to",
    "of",
    "in",
    "on",
    "with",
    "for",
    "intro",
    "introduction",
    "basic",
    "basics",
    "types",
    "type",
    "question",
    "questions",
    "operators",
    "operator",
    "methods",
    "method",
    "statement",
    "statements",
    "model",
    "core",
    "properties",
    "examples",
    "example",
}

LOW_VALUE_PHRASES = {
    "below you will find",
    "the following",
    "function definitions start",
    "you call functions",
    "if you need more advanced structures",
    "dictionaries are",
    "global and local names",
    "indexing",
    "slicing",
    "for-loops",
    "while loop",
}


def normalize_text(value: str) -> str:
    text = (value or "").lower()
    text = text.replace("**", " double_star ")
    text = text.replace("*", " star ")
    text = re.sub(r"[_/|\\,:;()\[\]{}-]+", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def token_set(value: str) -> set[str]:
    text = normalize_text(value)
    tokens = [t for t in text.split(" ") if t and t not in STOP_WORDS]
    cleaned = []
    for token in tokens:
        if token.endswith("s") and len(token) > 4:
            token = token[:-1]
        cleaned.append(token)
    return set(cleaned)


def topic_key(value: str) -> str:
    tokens = sorted(token_set(value))
    if not tokens:
        return "misc"

    alias_join = " ".join(tokens)
    aliases = {
        "arg kwargs star": "args kwargs",
        "global scope": "scope global",
        "lambda map": "lambda map",
        "lambda reduce": "lambda reduce",
        "lambda sorted": "lambda sorted",
        "mutable default": "mutable default",
        "mutable immutable": "mutable immutable",
        "return none": "return none",
        "scope unboundlocalerror": "scope unboundlocalerror",
        "truthy falsy": "truthy falsy",
        "zip enumerate": "zip enumerate",
    }
    return aliases.get(alias_join, " ".join(tokens))


def make_id(prefix: str, content: str) -> str:
    digest = hashlib.md5(content.encode("utf-8")).hexdigest()[:10]
    return f"{prefix}-{digest}"


def similarity(key_a: str, key_b: str) -> float:
    a = set(key_a.split())
    b = set(key_b.split())
    if not a or not b:
        return 0.0
    inter = len(a & b)
    union = len(a | b)
    if union == 0:
        return 0.0
    return inter / union


def is_relevant(card_key: str, source_key: str, threshold: float = 0.5) -> bool:
    if card_key == source_key:
        return True
    if card_key in source_key or source_key in card_key:
        return True
    return similarity(card_key, source_key) >= threshold


def pretty_topic(key: str, fallback: str) -> str:
    if fallback and fallback.strip():
        return fallback.strip()
    words = key.split()
    return " ".join(word.capitalize() for word in words)


def compact_text(value: str, max_len: int = 500) -> str:
    txt = (value or "").strip()
    if len(txt) <= max_len:
        return txt
    return txt[: max_len - 1].rstrip() + "…"


def looks_like_python_code(value: str) -> bool:
    text = (value or "").strip()
    if not text:
        return False
    if "\n" in text:
        return True

    code_signals = (
        "=",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        ".",
        ":",
        "+",
        "-",
        "*",
        "/",
        "%",
    )
    code_keywords = (
        "print",
        "for ",
        "while ",
        "if ",
        "elif ",
        "else",
        "def ",
        "return",
        "import ",
        "from ",
        "lambda",
        "range",
        "len",
        "sorted",
        "map",
        "filter",
        "reduce",
    )

    lower = text.lower()
    if any(signal in text for signal in code_signals) and any(ch.isalpha() for ch in text):
        return True
    return any(lower.startswith(keyword) or f" {keyword}" in lower for keyword in code_keywords)


def is_low_value_single_line(value: str) -> bool:
    text = (value or "").strip()
    if not text:
        return True

    if "\n" in text:
        return False

    lower = text.lower().strip()

    if lower.startswith("#"):
        return True
    if lower.startswith("##") or lower.startswith("###"):
        return True

    if any(phrase in lower for phrase in LOW_VALUE_PHRASES) and not looks_like_python_code(text):
        return True

    if not looks_like_python_code(text):
        words = re.findall(r"[a-zA-Z]+", text)
        if len(words) <= 8:
            return True

    return False


def clean_code_example(code: str) -> str:
    text = (code or "").strip()
    if not text:
        return ""
    if is_low_value_single_line(text):
        return ""
    return compact_text(text, 1400)


def clean_notebook_source(source: str, cell_type: str) -> str:
    text = (source or "").strip()
    if not text:
        return ""

    if "\n" not in text:
        if cell_type == "markdown" and is_low_value_single_line(text):
            return ""
        if cell_type == "code" and text.startswith("#"):
            return ""
        if cell_type == "code" and is_low_value_single_line(text) and not looks_like_python_code(text):
            return ""

    if len(text) <= 4:
        return ""

    return compact_text(text, 1200)


def dedupe_list(items: list[dict], key_fields: list[str]) -> list[dict]:
    seen = set()
    out = []
    for item in items:
        key = tuple(item.get(k) for k in key_fields)
        if key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def collect_card_topics(data: dict) -> dict[str, dict]:
    cards = {}

    for lecture in data.get("lectures", []):
        week = lecture.get("week")
        for concept in lecture.get("concepts", []):
            topic = concept.get("topic", "")
            key = topic_key(topic)
            if key not in cards:
                cards[key] = {
                    "canonical_topic": key,
                    "topic": topic,
                    "weeks": set(),
                    "lecture_snippets": [],
                    "exam_questions": [],
                    "notebook_snippets": [],
                    "exam_counts": defaultdict(int),
                    "trap_patterns": [],
                    "sample_topics": set(),
                }
            cards[key]["weeks"].add(week)
            cards[key]["sample_topics"].add(topic)

    for item in data.get("topic_analysis", {}).get("topic_frequency_across_all_exams", []):
        if not isinstance(item, list) or len(item) != 2:
            continue
        topic = item[0]
        key = topic_key(topic)
        if key not in cards:
            cards[key] = {
                "canonical_topic": key,
                "topic": topic,
                "weeks": set(),
                "lecture_snippets": [],
                "exam_questions": [],
                "notebook_snippets": [],
                "exam_counts": defaultdict(int),
                "trap_patterns": [],
                "sample_topics": set(),
            }
        cards[key]["sample_topics"].add(topic)

    return cards


def attach_lecture_content(cards: dict[str, dict], data: dict) -> None:
    for lecture in data.get("lectures", []):
        week = lecture.get("week")

        for concept in lecture.get("concepts", []):
            concept_topic = concept.get("topic", "")
            concept_key = topic_key(concept_topic)
            snippet_obj = {
                "id": make_id("lec", f"{week}-{concept_topic}-{concept.get('explanation', '')[:60]}"),
                "week": week,
                "source": f"Lecture Week {week}",
                "topic": concept_topic,
                "explanation": compact_text(concept.get("explanation", ""), 700),
                "code_examples": [],
            }
            for code_ex in concept.get("code_examples", []):
                cleaned = clean_code_example(code_ex.get("code", ""))
                if not cleaned:
                    continue
                snippet_obj["code_examples"].append(
                    {
                        "description": code_ex.get("description", "Code example"),
                        "code": cleaned,
                    }
                )

            for card_key, card in cards.items():
                if is_relevant(card_key, concept_key, threshold=0.45):
                    card["weeks"].add(week)
                    card["sample_topics"].add(concept_topic)
                    card["lecture_snippets"].append(snippet_obj)

        for q in lecture.get("lecture_questions", []):
            q_topic = q.get("topic", "")
            q_key = topic_key(q_topic)
            snippet_obj = {
                "id": make_id("leq", f"{week}-{q.get('question', '')[:80]}"),
                "week": week,
                "source": f"Lecture Week {week}",
                "topic": q_topic,
                "question": compact_text(q.get("question", ""), 500),
                "options": q.get("options", {}),
                "correct": q.get("correct"),
                "explanation": compact_text(q.get("explanation", ""), 700),
            }

            for card_key, card in cards.items():
                if is_relevant(card_key, q_key, threshold=0.5):
                    card["weeks"].add(week)
                    card["sample_topics"].add(q_topic)
                    card["lecture_snippets"].append(snippet_obj)


def attach_exam_content(cards: dict[str, dict], data: dict) -> None:
    for exam in data.get("exams", []):
        exam_label = exam.get("exam_label", exam.get("source", "unknown"))
        source = exam.get("source", exam_label)
        year = exam.get("year")
        for q in exam.get("questions", []):
            topic = q.get("topic", "")
            q_key = topic_key(topic)
            correct = q.get("correct_override") or q.get("correct")
            snippet_obj = {
                "id": make_id("exm", f"{exam_label}-{q.get('number')}-{topic}-{q.get('question', '')[:60]}"),
                "exam_label": exam_label,
                "exam_source": source,
                "year": year,
                "number": q.get("number"),
                "week": q.get("week"),
                "topic": topic,
                "question": compact_text(q.get("question", ""), 1200),
                "code_context": compact_text(q.get("code_context", "").strip(), 1000),
                "options": q.get("options", {}),
                "correct": correct,
                "explanation": compact_text(q.get("explanation", ""), 1200),
            }

            for card_key, card in cards.items():
                if is_relevant(card_key, q_key, threshold=0.5):
                    if q.get("week"):
                        card["weeks"].add(q.get("week"))
                    card["sample_topics"].add(topic)
                    card["exam_questions"].append(snippet_obj)
                    card["exam_counts"][exam_label] += 1


def attach_notebook_content(cards: dict[str, dict], data: dict) -> None:
    for cell in data.get("notebooks", []):
        if cell.get("is_advanced_optional"):
            continue
        topic = cell.get("topic", "")
        if not topic:
            continue

        cleaned_source = clean_notebook_source(cell.get("source", ""), cell.get("cell_type", ""))
        if not cleaned_source:
            continue

        source_key = topic_key(topic)
        snippet_obj = {
            "id": make_id("nb", f"{cell.get('week')}-{cell.get('cell_index')}-{topic}"),
            "week": cell.get("week"),
            "cell_index": cell.get("cell_index"),
            "cell_type": cell.get("cell_type"),
            "topic": topic,
            "source": cleaned_source,
            "outputs": [compact_text(out, 400) for out in (cell.get("outputs") or [])[:2] if out and out.strip()],
        }

        for card_key, card in cards.items():
            if is_relevant(card_key, source_key, threshold=0.6):
                card["weeks"].add(cell.get("week"))
                card["sample_topics"].add(topic)
                card["notebook_snippets"].append(snippet_obj)


def attach_patterns(cards: dict[str, dict], data: dict) -> None:
    for pattern in data.get("key_exam_patterns_and_traps", []):
        p_key = topic_key(pattern.get("pattern", ""))
        pattern_obj = {
            "pattern": pattern.get("pattern", ""),
            "trap": pattern.get("trap", ""),
            "weeks": pattern.get("weeks", []),
            "appears_in_exams": pattern.get("appears_in_exams", []),
        }

        for card_key, card in cards.items():
            if is_relevant(card_key, p_key, threshold=0.45):
                for week in pattern_obj["weeks"]:
                    card["weeks"].add(week)
                card["trap_patterns"].append(pattern_obj)


def build_ai_placeholders(display_topic: str) -> dict:
    return {
        "ai_summary": {
            "status": "pending_generation",
            "content": f"PENDING: Generate AI summary for '{display_topic}'.",
        },
        "ai_common_questions": {
            "status": "pending_generation",
            "bullets": [
                f"PENDING: Add common exam questions/traps for '{display_topic}'.",
            ],
        },
        "ai_examples": [
            {
                "id": "ai-example-correct-1",
                "kind": "correct",
                "title": f"PENDING correct example for {display_topic}",
                "code": "# PENDING",
                "why": "PENDING",
                "status": "pending_generation",
            },
            {
                "id": "ai-example-incorrect-1",
                "kind": "incorrect",
                "title": f"PENDING incorrect example for {display_topic}",
                "code": "# PENDING",
                "why": "PENDING",
                "status": "pending_generation",
            },
        ],
    }


def sort_cards(cards: dict[str, dict]) -> list[dict]:
    card_list = []
    for key, card in cards.items():
        lecture_snippets = dedupe_list(card["lecture_snippets"], ["id"])[:12]
        exam_questions = dedupe_list(card["exam_questions"], ["id"])[:12]
        notebook_snippets = dedupe_list(card["notebook_snippets"], ["id"])[:12]

        if not lecture_snippets and not exam_questions and not notebook_snippets and not card["trap_patterns"]:
            continue

        weeks = sorted(w for w in card["weeks"] if isinstance(w, int))
        exam_counts = dict(sorted(card["exam_counts"].items(), key=lambda kv: (-kv[1], kv[0])))
        total_exam_hits = sum(exam_counts.values())

        title_topic = sorted(card["sample_topics"], key=len)[0] if card["sample_topics"] else card["topic"]
        display_topic = pretty_topic(key, title_topic)

        card_id = "topic-" + re.sub(r"[^a-z0-9]+", "-", key).strip("-")
        if not card_id or card_id == "topic-":
            card_id = make_id("topic", key)

        sections = {
            "lecture_snippets": lecture_snippets,
            "exam_questions": exam_questions,
            "notebook_snippets": notebook_snippets,
        }
        sections.update(build_ai_placeholders(display_topic))

        card_list.append(
            {
                "id": card_id,
                "topic": display_topic,
                "canonical_topic": key,
                "weeks": weeks,
                "exam_stats": {
                    "total_hits": total_exam_hits,
                    "by_exam": exam_counts,
                    "coverage_count": len(exam_counts),
                },
                "related_topics": sorted(card["sample_topics"]),
                "trap_patterns": card["trap_patterns"][:8],
                "sections": sections,
            }
        )

    card_list.sort(
        key=lambda c: (
            -c["exam_stats"]["total_hits"],
            99 if not c["weeks"] else min(c["weeks"]),
            c["topic"].lower(),
        )
    )
    return card_list


def main() -> None:
    data = json.loads(SOURCE_FILE.read_text(encoding="utf-8"))

    cards = collect_card_topics(data)
    attach_lecture_content(cards, data)
    attach_exam_content(cards, data)
    attach_notebook_content(cards, data)
    attach_patterns(cards, data)

    output = {
        "meta": {
            "generated_from": SOURCE_FILE.name,
            "generator": "build_topic_cards.py",
            "course": data.get("meta", {}).get("course"),
            "weeks_covered": data.get("meta", {}).get("weeks_covered", []),
            "total_cards": 0,
            "notes": [
                "Sections (1) lecture snippets, (2) exam Q&A, and (4) notebook snippets are sourced from study_data.json.",
                "Low-value one-line notebook/heading snippets are filtered out automatically.",
                "AI sections are generated separately (summary, common questions, examples).",
            ],
        },
        "cards": [],
    }

    output["cards"] = sort_cards(cards)
    output["meta"]["total_cards"] = len(output["cards"])

    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {OUTPUT_FILE} with {output['meta']['total_cards']} cards")


if __name__ == "__main__":
    main()
