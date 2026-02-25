# Topic Merging Guidelines

This document is a handoff guide for strict manual topic curation in `topic_cards.json`.

## Why This Exists

The repository already went through one large duplicate-topic consolidation pass, but that pass was mostly heuristic (quality scoring + dedupe), not fully manual for every topic.

Use this guide when you need to:

- manually merge or split topic cards,
- improve content quality after regeneration,
- ensure each swipe topic is exam-relevant and non-redundant.

## Current Baseline

At the time this guide was written:

- `topic_cards.json` has **28** cards.
- default swipe deck (`only exam topics`) has **21** cards.
- exact duplicate normalized topic labels are **0**.

Important: even with exact duplicates removed, semantic overlap can still exist.

## Quality Bar

Every final topic card should be:

- focused on one core exam concept,
- written in clean, complete language (no dangling ellipses),
- free from obvious overlap with another card,
- consistent in structure and metadata.

## Recommended Workflow

### 1) Create a Safety Baseline

```bash
git checkout -b codex/topic-manual-curation
cp topic_cards.json topic_cards.backup.json
```

### 2) Generate an Audit Snapshot

Use this before edits to understand current topic spread:

```bash
python3 - <<'PY'
import json
with open("topic_cards.json") as f:
    cards = json.load(f)["cards"]
for c in sorted(cards, key=lambda x: (-x["exam_stats"]["total_hits"], x["topic"].lower())):
    print(f'{c["topic"]} | id={c["id"]} | hits={c["exam_stats"]["total_hits"]} | weeks={c["weeks"]} | canonical={c["canonical_topic"]}')
PY
```

### 3) Pick a Curation Batch

Start with highest-impact cards (highest exam hits), then low-hit cards.

Suggested review bundles:

1. `For Loops`, `Range()`
2. `Conditions`, `truthy_falsy`, `Boolean operators`, `comparison_operators`, `walrus_operator`
3. `Functions`, `Return / None`, `Default arguments`, `*args`, `*args / **kwargs`
4. `mutable_immutable`, `mutable args`, `mutable_default`, `Objects`, `Names`
5. `Dictionaries`, `Sets`, `dict / average`
6. `Indexing`, `Slicing`, `Strings`
7. `Lambda`, `Enumerate`, `Zip`

These are semantic-review bundles, not mandatory merges.

### 4) For Each Bundle, Decide Merge vs Keep-Separate

For each candidate pair/group, explicitly decide:

- `merge`: one card is enough for exam prep.
- `keep separate`: concepts are distinct enough and both are useful.
- `split`: current card mixes too many ideas and should be separated.

Write the decision in your PR/commit notes.

### 5) Manual Card Curation Rules (Field by Field)

When merging cards manually, curate each section intentionally:

#### `topic`, `canonical_topic`, `id`

- `topic`: user-facing title (clean and readable).
- `canonical_topic`: normalized internal label.
- `id`: stable unique ID; keep anchor ID where possible to preserve localStorage compatibility.

#### `weeks`, `related_topics`, `trap_patterns`

- union relevant weeks; drop noisy/unrelated ones.
- keep `related_topics` meaningful and deduped.
- dedupe trap patterns by `(pattern, trap)` content.

#### `sections.lecture_snippets`, `sections.exam_questions`, `sections.notebook_snippets`

- union by content/ID and dedupe.
- remove low-value snippets (headers, fluff, repetitive tiny notes).
- keep the strongest sources first.

#### `sections.ai_summary.content`

- rewrite manually if needed.
- keep concise and exam-focused.
- avoid incomplete endings (`...` / `…`).

#### `sections.ai_common_questions.bullets`

- keep 5-8 strong exam-style questions.
- remove duplicates and vague wording.

#### `sections.key_points_to_remember`

- keep 5-10 concrete points.
- each point should be testable and specific.
- keep only useful details (`code`, `table`, `explanation`), remove weak filler.
- reassign IDs sequentially: `kp-1`, `kp-1-d1`, etc.

#### `sections.ai_examples`

- target 4-6 examples.
- include both `correct` and `incorrect`.
- prefer examples that explain common traps clearly.
- ensure every example has `title`, `code`, `why`, `kind`.

#### `sections.recommended_ids`

- must reference IDs that exist in the card’s own source snippet buckets.
- prioritize exam snippets first, then lecture, then notebook.

### 6) Recompute/Repair Metadata

After each merge:

- recompute `exam_stats.total_hits`, `exam_stats.by_exam`, `exam_stats.coverage_count` from merged `exam_questions`.
- ensure `weeks` are sorted integers.
- ensure all IDs are unique globally.

### 7) Validate Data Integrity

Run this after each curation batch:

```bash
python3 - <<'PY'
import json, re
from collections import Counter

with open("topic_cards.json") as f:
    data = json.load(f)
cards = data["cards"]

ids = [c["id"] for c in cards]
assert len(ids) == len(set(ids)), "Duplicate card IDs found"

def norm_topic(s):
    s = (s or "").lower().replace("_", " ").replace("-", " ")
    s = re.sub(r"\s+", " ", s).strip()
    if s.endswith("ies") and len(s) > 4:
        s = s[:-3] + "y"
    elif s.endswith("s") and len(s) > 4 and not s.endswith("ss"):
        s = s[:-1]
    return s

dups = [k for k, v in Counter(norm_topic(c["topic"]) for c in cards).items() if v > 1]
print("cards:", len(cards))
print("duplicate-normalized-topics:", len(dups))

for card in cards:
    s = card["sections"]
    for key in ["lecture_snippets", "exam_questions", "notebook_snippets", "ai_examples", "key_points_to_remember", "recommended_ids"]:
        assert isinstance(s.get(key), list), f'{card["id"]}: {key} must be list'
    assert isinstance(s.get("ai_summary"), dict), f'{card["id"]}: ai_summary must be object'
    assert isinstance(s.get("ai_common_questions"), dict), f'{card["id"]}: ai_common_questions must be object'

    valid_ids = {
        item.get("id")
        for bucket in ["lecture_snippets", "exam_questions", "notebook_snippets"]
        for item in s.get(bucket, [])
        if isinstance(item, dict)
    }
    for rid in s.get("recommended_ids", []):
        assert rid in valid_ids, f'{card["id"]}: recommended id not found: {rid}'

print("integrity checks passed")
PY
```

### 8) Validate UI Behavior

Run local app and verify:

```bash
python3 -m http.server 8000
```

Manual checks:

1. Swipe count is reasonable.
2. No clearly duplicated concepts with same user-facing label.
3. Cards read cleanly (no clipped/truncated summary lines).
4. Key-point detail blocks and examples still render in swipe view and preview/export cards.
5. Existing localStorage behavior still works after refresh.

## Merge Strategy Notes

### Anchor Card Selection

Use the strongest anchor card by:

1. highest `exam_stats.total_hits`,
2. richest exam/lecture/notebook evidence,
3. best existing wording quality.

Then curate manually by pulling strongest parts from other cards.

### Preferred Topic Count

Aim for a practical deck size where students can review without fatigue.

- If default deck (`only exam topics`) feels too large, continue semantic merges.
- If cards become too broad, split back into focused exam concepts.

## What Not To Do

- do not rely only on automatic string similarity for final decisions.
- do not keep stale `recommended_ids` that point to removed snippets.
- do not preserve low-quality generated text just because it already exists.
- do not change IDs casually for cards that users may already have decisions on unless necessary.

## Handoff Checklist for Next Agent

Before finishing, include in your summary:

1. which bundles were reviewed,
2. which were merged vs kept separate (with reasons),
3. final card counts (`total` and `exam-hit`),
4. integrity check result,
5. any open quality concerns.
