from __future__ import annotations

import json
import re
from typing import Any

from pipelines.vision_exam_pipeline_shared import _safe_dict, _safe_list, _safe_str, snippet_identity_for_item


_TOKEN_RE = re.compile(r"[a-zA-Z_]{3,}")


def _tokenize(text: str) -> set[str]:
    return {token.lower() for token in _TOKEN_RE.findall(text or "")}


def candidate_snippet_families_for_question(
    *,
    question: dict[str, Any],
    selectable_items: list[dict[str, Any]],
    limit: int = 14,
    max_pieces_per_family: int = 6,
) -> list[dict[str, Any]]:
    snapshot = _safe_dict(question.get("question_snapshot"))
    seed_context = _safe_dict(question.get("seed_context"))
    prioritized = {
        _safe_str(item_id)
        for item_id in _safe_list(seed_context.get("available_seed_snippet_ids"))
        if _safe_str(item_id)
    }
    question_text = "\n".join(
        [
            _safe_str(snapshot.get("topic")),
            _safe_str(snapshot.get("question")),
            json.dumps(_safe_dict(snapshot.get("options")), ensure_ascii=False),
            _safe_str(snapshot.get("code_context")),
        ]
    )
    question_tokens = _tokenize(question_text)
    families: dict[str, dict[str, Any]] = {}
    for item in selectable_items:
        if not isinstance(item, dict):
            continue
        item_id = _safe_str(item.get("item_id"))
        if not item_id:
            continue
        snippet_id = _safe_str(item.get("snippet_id"))
        snippet_label = _safe_str(item.get("snippet_label"))
        if not snippet_id:
            snippet_id, snippet_label = snippet_identity_for_item(item)
        item_text = " ".join(
            [
                _safe_str(item.get("topic")),
                _safe_str(item.get("subtopic_title")),
                _safe_str(item.get("search_text")),
            ]
        )
        score = len(question_tokens & _tokenize(item_text))
        if item_id in prioritized:
            score += 20
        if _safe_str(snapshot.get("topic")) and _safe_str(snapshot.get("topic")).lower() in item_text.lower():
            score += 4
        if item.get("bucket") == "recommended":
            score += 2
        if item.get("item_type") in {"key_point", "key_point_detail", "ai_common_question"}:
            score += 1
        family = families.setdefault(
            snippet_id,
            {
                "snippet_id": snippet_id,
                "snippet_label": snippet_label or _safe_str(item.get("subtopic_title")) or _safe_str(item.get("topic")) or snippet_id,
                "week": int(item.get("week") or 0),
                "topic": _safe_str(item.get("topic")),
                "score": 0,
                "pieces": [],
            },
        )
        family["score"] = max(int(family["score"]), score)
        family["pieces"].append(
            (
                score,
                {
                    "item_id": item_id,
                    "item_type": _safe_str(item.get("item_type")),
                    "bucket": _safe_str(item.get("bucket")),
                    "topic": _safe_str(item.get("topic")),
                    "subtopic_title": _safe_str(item.get("subtopic_title")),
                    "search_text": _safe_str(item.get("search_text"))[:280],
                },
            )
        )
    ranked = sorted(
        families.values(),
        key=lambda row: (-int(row["score"]), len(row["pieces"]), _safe_str(row["snippet_id"])),
    )
    payload = []
    for family in ranked[:limit]:
        pieces = [piece for _, piece in sorted(family["pieces"], key=lambda row: (-row[0], _safe_str(row[1]["item_id"])))[:max_pieces_per_family]]
        payload.append(
            {
                "snippet_id": _safe_str(family.get("snippet_id")),
                "snippet_label": _safe_str(family.get("snippet_label")),
                "week": int(family.get("week") or 0),
                "topic": _safe_str(family.get("topic")),
                "pieces": pieces,
            }
        )
    return payload


def evaluation_prompt(*, question: dict[str, Any], candidates: list[dict[str, Any]]) -> str:
    return f"""
You are evaluating which selectable snippets help a student answer a Python exam question with almost zero prior Python knowledge.

Important model:
- A snippet family is a logical snippet bundle.
- Pieces are the selectable items inside that snippet family.
- First identify any near-identical past exam pieces.
- Then exclude those near-identical past exam pieces from your best-general-snippet and minimal-set judgments whenever possible.

Question JSON:
{json.dumps(_safe_dict(question.get("question_snapshot")), ensure_ascii=False)}

Candidate snippet families:
{json.dumps(candidates, ensure_ascii=False)}

Return ONLY one JSON object with EXACT keys:
{{
  "near_identical_past_exam_pieces": [
    {{"item_id": "", "snippet_id": "", "rationale": ""}}
  ],
  "best_snippet_family": {{
    "snippet_id": "",
    "rationale": "",
    "critical_piece_ids": [""]
  }},
  "supporting_snippet_families": [
    {{
      "snippet_id": "",
      "rationale": "",
      "critical_piece_ids": [""]
    }}
  ],
  "minimal_snippet_families": [
    {{
      "snippet_id": "",
      "rationale": "",
      "needed_piece_ids": [""]
    }}
  ],
  "answerability": {{
    "status": "certain|partial|insufficient",
    "confidence": "high|medium|low",
    "rationale": "",
    "usable_without_prior_python_knowledge": true
  }},
  "gap_analysis": {{
    "summary": "",
    "missing_concepts": [""],
    "proposed_fix": ""
  }},
  "suggested_changes": [
    {{
      "kind": "edit_existing|add_new",
      "target_item_id": "",
      "proposal": "",
      "why_helpful": "",
      "why_maybe_unnecessary": "",
      "recommended_direction": "add_this|consider_instead|skip"
    }}
  ]
}}

Rules:
- Only choose `snippet_id` and `item_id` values that appear in the candidate list.
- `near_identical_past_exam_pieces` should only include past-exam pieces that are near-identical to the current question.
- `best_snippet_family` must contain exactly 1 snippet family, unless no useful non-identical family exists.
- `best_snippet_family.critical_piece_ids` must contain 1-3 item ids from that family.
- `supporting_snippet_families` must contain 1-2 unique snippet families.
- `minimal_snippet_families` must contain 1-6 unique snippet families.
- `minimal_snippet_families.needed_piece_ids` must only include pieces from that family.
- If the snippets are not enough, still choose the closest useful items and explain the gap.
- If no existing snippet should be edited, leave `target_item_id` as "" for an `add_new` suggestion.
- If no changes are needed, return `suggested_changes: []`.
- Keep rationales concise and specific.
""".strip()


def normalize_piece_ids(values: Any, *, valid_ids: set[str], max_items: int) -> list[str]:
    items = []
    seen: set[str] = set()
    for value in _safe_list(values):
        item_id = _safe_str(value)
        if not item_id or item_id in seen or item_id not in valid_ids:
            continue
        seen.add(item_id)
        items.append(item_id)
        if len(items) >= max_items:
            break
    return items


def normalize_family_selection(
    entry: Any,
    *,
    valid_snippet_ids: set[str],
    valid_piece_ids: set[str],
    piece_field: str,
    max_piece_count: int,
) -> dict[str, Any]:
    item = _safe_dict(entry)
    snippet_id = _safe_str(item.get("snippet_id"))
    if snippet_id not in valid_snippet_ids:
        return {}
    return {
        "snippet_id": snippet_id,
        "rationale": _safe_str(item.get("rationale")),
        piece_field: normalize_piece_ids(item.get(piece_field), valid_ids=valid_piece_ids, max_items=max_piece_count),
    }


def normalize_near_identical_pieces(values: Any, *, valid_piece_ids: set[str], valid_snippet_ids: set[str]) -> list[dict[str, Any]]:
    items = []
    seen: set[str] = set()
    for value in _safe_list(values):
        entry = _safe_dict(value)
        item_id = _safe_str(entry.get("item_id"))
        if not item_id or item_id in seen or item_id not in valid_piece_ids:
            continue
        snippet_id = _safe_str(entry.get("snippet_id"))
        if snippet_id and snippet_id not in valid_snippet_ids:
            snippet_id = ""
        seen.add(item_id)
        items.append(
            {
                "item_id": item_id,
                "snippet_id": snippet_id,
                "rationale": _safe_str(entry.get("rationale")),
            }
        )
    return items
