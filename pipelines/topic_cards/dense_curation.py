from __future__ import annotations

import re
from typing import Any

from pipelines.shared import compact_text
from pipelines.topic_cards.curation_utils import safe_list, safe_str, structured_question_item
from pipelines.topic_cards.study_text import infer_pattern_label, normalize_rule_text, pattern_hint, question_summary_text


def looks_generic_title(title: str) -> bool:
    return bool(re.fullmatch(r"(advanced_optional|Notebook cell \d+|intro|comments|strings?)", safe_str(title), re.IGNORECASE))


def best_code_label(code: str, fallback: str) -> str:
    for line in safe_str(code).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        return compact_text(stripped, 70)
    return fallback


def retitle_notebook_snippet(snippet: dict[str, Any]) -> dict[str, Any]:
    title = safe_str(snippet.get("title"))
    if looks_generic_title(title):
        title = best_code_label(snippet.get("source", ""), "Worked source example")
    item = dict(snippet)
    item["title"] = title or "Worked source example"
    return item


def notebook_priority(snippet: dict[str, Any]) -> tuple[int, int, int]:
    source_type = safe_str(snippet.get("source_type"))
    outputs = safe_list(snippet.get("outputs"))
    source = safe_str(snippet.get("source"))
    score = 0
    if source_type == "homework":
        score += 5
    if outputs:
        score += 4
    if "print(" in source:
        score += 2
    if any(token in source for token in ["zip(", "enumerate(", ".loc", ".iloc", "strftime", "strptime", "replace(", "find("]):
        score += 2
    if len(source.splitlines()) <= 10:
        score += 1
    return (-score, len(source), int(snippet.get("cell_index") or 0))


def curate_notebook_snippets(topic: dict[str, Any], notebook_snippets: list[dict[str, Any]], norm_fn) -> list[dict[str, Any]]:
    by_code: dict[str, dict[str, Any]] = {}
    for snippet in notebook_snippets:
        source = safe_str(snippet.get("source"))
        if not source:
            continue
        item = retitle_notebook_snippet(snippet)
        key = norm_fn(source)
        current = by_code.get(key)
        if current is None or notebook_priority(item) < notebook_priority(current):
            by_code[key] = item
    curated = sorted(by_code.values(), key=notebook_priority)
    if topic.get("id") in {"w4-string-fundamentals", "w5-pandas-core-structures"}:
        return curated[:10]
    return curated[:8]


def question_summary(text: str) -> str:
    return question_summary_text(text)


def compact_code_block(code: Any, max_lines: int = 12) -> str:
    lines = [line.rstrip() for line in safe_str(code).splitlines()]
    if not lines:
        return ""
    trimmed: list[str] = []
    code_like_lines = 0
    for line in lines:
        if re.fullmatch(r"[A-D]", line.strip()):
            break
        if re.match(r"^[A-D]\s{2,}", line):
            break
        trimmed.append(line)
        if re.search(r"[=:()\[\]{}]|^\s*(def |class |for |while |if |elif |else:|print\(|return\b|import\b|from\b)", line):
            code_like_lines += 1
        if len(trimmed) >= max_lines:
            break
    while trimmed and not trimmed[-1].strip():
        trimmed.pop()
    blob = "\n".join(trimmed).strip()
    if len(blob) > 420:
        return ""
    if trimmed and code_like_lines == 0 and len(trimmed) > 4:
        return ""
    return blob


def dense_reference_table(topic: dict[str, Any]) -> dict[str, Any] | None:
    topic_id = safe_str(topic.get("id"))
    table_map: dict[str, dict[str, Any]] = {
        "w1-sequences-and-access": {
            "headers": ["Pattern", "Meaning", "Example"],
            "rows": [
                ["seq[i]", "single element", "x[-1]"],
                ["seq[a:b]", "start inclusive, stop exclusive", "x[1:4]"],
                ["seq[::-1]", "reverse copy", "x[::-1]"],
                ["seq[::2]", "step through every other item", "x[::2]"],
            ],
        },
        "w1-functions-and-imports": {
            "headers": ["Call", "Use", "Typical result"],
            "rows": [
                ["int('123')", "string to integer", "123"],
                ["float('123')", "string to float", "123.0"],
                ["str(123.0)", "number to string", "'123.0'"],
                ["round(x, 2)", "round for display/checking", "2 decimals"],
            ],
        },
        "w2-dictionaries-and-mappings": {
            "headers": ["Operation", "What it gives", "Exam note"],
            "rows": [
                ["d[key]", "value lookup", "Key must exist"],
                ["key in d", "membership on keys", "not values"],
                ["d.items()", "(key, value) pairs", "good for loops"],
                ["d.update(...)", "mutates dict", "returns None"],
            ],
        },
        "w3-higher-order-patterns": {
            "headers": ["Tool", "Returns", "Best for"],
            "rows": [
                ["map(f, seq)", "lazy transformed iterable", "same-length transform"],
                ["filter(f, seq)", "lazy filtered iterable", "keep matching items"],
                ["sorted(seq, key=...)", "new sorted list", "comparison key"],
                ["lambda x: ...", "anonymous function", "small inline transform"],
            ],
        },
        "w4-string-fundamentals": {
            "headers": ["Form", "What it means", "Exam use"],
            "rows": [
                ["'...'/\"...\"", "basic literals", "choose quote style"],
                ["\\n / \\t", "newline / tab", "predict printed output"],
                ["r'...'", "raw string", "slashes stay literal"],
                ["s[i:j:k]", "string slicing", "same rules as sequences"],
            ],
        },
        "w4-string-operations-and-methods": {
            "headers": ["Method", "Returns", "Trap"],
            "rows": [
                ["s.find(x)", "index or -1", "never raises"],
                ["s.index(x)", "index", "raises if missing"],
                ["s.replace(a, b)", "new string", "strings are immutable"],
                ["sep.join(seq)", "new joined string", "separator is the caller"],
            ],
        },
        "w5-pandas-core-structures": {
            "headers": ["Object", "Created from", "Common next step"],
            "rows": [
                ["pd.Series(...)", "1D labeled data", "inspect dtype/index"],
                ["pd.DataFrame(...)", "2D labeled table", "check columns/index"],
                ["df['col']", "column selection", "returns Series"],
                ["df[['a', 'b']]", "multiple columns", "returns DataFrame"],
            ],
        },
        "w5-inspecting-and-selecting-data": {
            "headers": ["Selector", "What it uses", "Result"],
            "rows": [
                ["df.loc[row, col]", "labels", "endpoint-inclusive slicing"],
                ["df.iloc[row, col]", "positions", "Python-style exclusive slice"],
                ["df.head(n)", "first rows", "quick inspect"],
                ["df[df['A'] > 0]", "boolean filter", "row subset"],
            ],
        },
        "w5-combining-data": {
            "headers": ["Operation", "Main axis/key idea", "When useful"],
            "rows": [
                ["pd.concat([...], axis=0)", "stack rows", "same columns"],
                ["pd.concat([...], axis=1)", "add columns", "aligned index"],
                ["df.merge(...)", "join on key(s)", "relational combine"],
                ["df.groupby(...)", "split/apply/combine", "aggregate by category"],
            ],
        },
        "w6-datetime": {
            "headers": ["Call", "Direction", "Example"],
            "rows": [
                ["datetime.now()", "object now", "current timestamp"],
                ["dt.strftime(fmt)", "datetime -> string", "'%Y-%m-%d'"],
                ["datetime.strptime(s, fmt)", "string -> datetime", "parse exam date"],
                ["dt + timedelta(...)", "date arithmetic", "shift days/hours"],
            ],
        },
    }
    return table_map.get(topic_id)


def common_questions(exam_questions: list[dict[str, Any]], traps: list[dict[str, Any]]) -> list[str]:
    bullets = []
    for question in exam_questions[:4]:
        prompt = compact_text(question.get("question", ""), 260)
        if prompt:
            bullets.append(prompt)
    for trap in traps[:3]:
        text = compact_text(trap.get("trap", ""), 260)
        if text and text not in bullets:
            bullets.append(text)
    return bullets[:6]


def build_key_points(
    topic: dict[str, Any],
    lecture_snippets: list[dict[str, Any]],
    exam_questions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    key_points = []
    index = 1
    for snippet in lecture_snippets:
        text = normalize_rule_text(snippet.get("explanation", ""))
        if not text:
            continue
        details = []
        for detail_index, example in enumerate(safe_list(snippet.get("code_examples"))[:2], start=1):
            code = safe_str(example.get("code"))
            if not code:
                continue
            details.append(
                {
                    "id": f"kp-{index}-d{detail_index}",
                    "kind": "example",
                    "title": safe_str(example.get("description")) or "Code example",
                    "code": code,
                }
            )
        key_points.append(
            {
                "id": f"kp-{index}",
                "text": text,
                "status": "curated",
                "generator": "lecture-first-build",
                "model": None,
                "subtopic_id": snippet.get("subtopic_id"),
                "subtopic_title": snippet.get("subtopic_title"),
                "details": details,
            }
        )
        index += 1
    if exam_questions:
        exam = exam_questions[0]
        option_text = safe_str(exam.get("options", {}).get(exam.get("correct")))
        if option_text:
            key_points.append(
                {
                    "id": f"kp-{index}",
                    "text": compact_text(f"Pattern to remember: {option_text}", 220),
                    "status": "curated",
                    "generator": "lecture-first-build",
                    "model": None,
                    "subtopic_id": exam.get("subtopic_id"),
                    "subtopic_title": exam.get("subtopic_title"),
                    "details": [],
                }
            )
            index += 1
    table = dense_reference_table(topic)
    if table:
        host = key_points[0] if key_points else None
        if host is not None:
            host.setdefault("details", []).append(
                {
                    "id": f"{host['id']}-d{len(host.get('details', [])) + 1}",
                    "kind": "table",
                    "title": "Dense reference table",
                    "table": table,
                }
            )
        else:
            subtopics = safe_list(topic.get("subtopics"))
            subtopic_id = subtopics[0].get("id") if subtopics else ""
            subtopic_title = subtopics[0].get("title") if subtopics else ""
            key_points.append(
                {
                    "id": f"kp-{index}",
                    "text": "Dense reference table for the core syntax patterns in this topic.",
                    "status": "curated",
                    "generator": "lecture-first-build",
                    "model": None,
                    "subtopic_id": subtopic_id,
                    "subtopic_title": subtopic_title,
                    "details": [{"id": f"kp-{index}-d1", "kind": "table", "title": "Dense reference table", "table": table}],
                }
            )
    return key_points[:10]


def build_examples(
    lecture_snippets: list[dict[str, Any]],
    notebook_snippets: list[dict[str, Any]],
    exam_questions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    examples = []
    index = 1
    for snippet in lecture_snippets:
        for example in safe_list(snippet.get("code_examples"))[:2]:
            code = safe_str(example.get("code"))
            if not code:
                continue
            raw_title = safe_str(example.get("description")) or "Lecture example"
            title = raw_title if (" " in raw_title and not re.fullmatch(r"[a-z0-9_]+", raw_title.lower())) else infer_pattern_label(raw_title, code)
            examples.append(
                {
                    "id": f"ai-example-{index}",
                    "kind": "correct",
                    "title": title,
                    "code": code,
                    "why": normalize_rule_text(snippet.get("explanation", "")) or pattern_hint(code, example.get("description")),
                    "output": "",
                    "status": "curated",
                    "subtopic_id": snippet.get("subtopic_id"),
                    "subtopic_title": snippet.get("subtopic_title"),
                }
            )
            index += 1
    for snippet in notebook_snippets[:6]:
        code = safe_str(snippet.get("source"))
        if not code:
            continue
        raw_title = safe_str(snippet.get("title")) or "Notebook example"
        examples.append(
            {
                "id": f"ai-example-{index}",
                "kind": "correct",
                "title": raw_title if (" " in raw_title and not re.fullmatch(r"[a-z0-9_]+", raw_title.lower())) else infer_pattern_label(raw_title, code, snippet.get("outputs")),
                "code": code,
                "why": pattern_hint(code, snippet.get("title"), "\n".join(safe_list(snippet.get("outputs"))[:3])),
                "output": "\n".join(safe_list(snippet.get("outputs"))[:3]),
                "status": "curated",
                "subtopic_id": snippet.get("subtopic_id"),
                "subtopic_title": snippet.get("subtopic_title"),
            }
        )
        index += 1
    for question in exam_questions[:2]:
        code = safe_str(question.get("code_context"))
        if not code:
            continue
        examples.append(
            {
                "id": f"ai-example-{index}",
                "kind": "incorrect",
                "title": f"Exam trap • Q{question.get('number') or '?'}",
                "code": code,
                "why": normalize_rule_text(question.get("explanation", "")) or pattern_hint(code, question.get("question")),
                "output": safe_str(question.get("options", {}).get(question.get("correct"))),
                "status": "curated",
                "subtopic_id": question.get("subtopic_id"),
                "subtopic_title": question.get("subtopic_title"),
            }
        )
        index += 1
    return examples[:8]


def build_common_question_items(
    topic: dict[str, Any],
    lecture_questions: list[dict[str, Any]],
    exam_questions: list[dict[str, Any]],
    traps: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for idx, question in enumerate(lecture_questions[:3], start=1):
        items.append(
            structured_question_item(
                item_id=f"aiq-{idx}",
                summary=question_summary_text(
                    question.get("content", ""),
                    code_context=question.get("code_context"),
                    title=question.get("title"),
                    explanation=question.get("explanation"),
                ),
                detail=normalize_rule_text(question.get("explanation", ""))
                or pattern_hint(question.get("code_context"), question.get("content"), question.get("title")),
                extra=f"Lecture question • {question.get('title') or topic.get('title')}",
                code=compact_code_block(question.get("code_context")),
                subtopic_id=safe_str(question.get("subtopic_id")),
                subtopic_title=safe_str(question.get("subtopic_title")),
            )
        )
    for exam in exam_questions[:3]:
        prompt = question_summary_text(
            exam.get("question", ""),
            code_context=exam.get("code_context"),
            title=exam.get("topic"),
            explanation=exam.get("explanation"),
        )
        detail = normalize_rule_text(exam.get("explanation", ""))
        extra = f"Exam • {exam.get('exam_label')} • Q{exam.get('number')}"
        items.append(
            structured_question_item(
                item_id=f"aiq-{len(items) + 1}",
                summary=prompt,
                detail=detail or pattern_hint(exam.get("code_context"), exam.get("question"), exam.get("options", {}).get(exam.get("correct"))),
                extra=extra,
                code=compact_code_block(exam.get("code_context")),
                subtopic_id=safe_str(exam.get("subtopic_id")),
                subtopic_title=safe_str(exam.get("subtopic_title")),
            )
        )
    table = dense_reference_table(topic)
    if table:
        subtopics = safe_list(topic.get("subtopics"))
        items.append(
            structured_question_item(
                item_id=f"aiq-{len(items) + 1}",
                summary=f"What compact reference should you scan first for {topic.get('title')} questions?",
                detail="Use this dense comparison block to recover the right pattern quickly under exam pressure.",
                table=table,
                subtopic_id=subtopics[0].get("id") if subtopics else "",
                subtopic_title=subtopics[0].get("title") if subtopics else "",
            )
        )
    for trap in traps[:2]:
        items.append(
            structured_question_item(
                item_id=f"aiq-{len(items) + 1}",
                summary=compact_text(trap.get("pattern", ""), 120),
                detail=compact_text(trap.get("trap", ""), 180),
            )
        )
    return items[:8]


def recommended_ids(
    lecture_snippets: list[dict[str, Any]],
    exam_questions: list[dict[str, Any]],
    notebook_snippets: list[dict[str, Any]],
) -> list[str]:
    ordered = [item["id"] for item in exam_questions[:4]]
    ordered.extend(item["id"] for item in lecture_snippets[:4])
    ordered.extend(item["id"] for item in notebook_snippets[:4])
    seen = set()
    out = []
    for item_id in ordered:
        if item_id in seen:
            continue
        seen.add(item_id)
        out.append(item_id)
    return out[:8]
