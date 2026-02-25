# AGENTS.md

Technical handoff for coding agents and contributors working on this repository.

## Project

`python-exam-cheat-sheet-generator` is a static web app for building exam cheat sheets from curated Python topic cards.

- Frontend only (`index.html`, `styles.css`, `app.js`)
- No backend/runtime services required
- Source dataset and generated card data are JSON files in repo

## Current Snapshot (2026-02-25)

- `topic_cards.json`: **28 total cards**
- Default exam deck (`only exam topics`): **21 cards**
- Duplicate normalized topic labels: **0**

Curation state:

- All 21 exam-topic cards were curated using an evidence-driven pass over exam + lecture + notebook + trap data.
- `key_points_to_remember` and `ai_examples` are intentionally **variable-length** by topic based on evidence coverage.
- There is no fixed per-topic cap for key points/examples.
- Exact duplicate key-point text and exact duplicate example code blocks across exam topics were removed.
- Example code blocks for exam topics were syntax-checked.

## App Behavior

- Swipe workflow for keep/reject topic cards
- Detail selection per card (key points, examples, snippets)
- 2-page A4 preview with draggable/resizable cards
- Export via print / PNG / PDF
- First-open splash screen + `Reset intro`
- Progress persistence in `localStorage`

Storage keys:

- `python_midterm_app_state_v1`
- `python_midterm_splash_seen_v1`

## Core Files

- `index.html`: app shell and major sections
- `styles.css`: all styling
- `app.js`: state, rendering, persistence, interactions, preview/export
- `topic_cards.json`: curated card dataset consumed by UI
- `study_data.json`: source dataset

Generation/processing scripts:

- `build_topic_cards.py`
- `generate_ai_sections.py`
- `generate_key_points_and_recommendations.py`
- `enrich_key_point_details.py`

Guides/docs:

- `TOPIC_MERGING_GUIDELINES.md`
- `DATASET_INFO.md`

Deploy:

- `.github/workflows/pages.yml`

## Data Pipeline

Regeneration order:

```bash
python3 build_topic_cards.py
python3 generate_ai_sections.py
python3 generate_key_points_and_recommendations.py
python3 enrich_key_point_details.py
```

After regeneration:

- Re-run manual semantic curation (see `TOPIC_MERGING_GUIDELINES.md`)
- Re-check overlaps and quality drift

## Curation Rules (Important)

When editing `topic_cards.json`:

- Use evidence-driven inclusion from course materials and exams.
- Do not enforce arbitrary fixed counts across all topics.
- Keep only important, exam-relevant content.
- Remove duplicates/near-duplicates.
- Keep example code coherent and syntactically valid.
- Keep `recommended_ids` valid against card-local source snippet IDs.

## Validation Checklist

```bash
node --check app.js
python3 -m py_compile build_topic_cards.py generate_ai_sections.py generate_key_points_and_recommendations.py enrich_key_point_details.py
```

Integrity check:

```bash
python3 - <<'PY'
import json, re
from collections import Counter

with open('topic_cards.json') as f:
    cards = json.load(f)['cards']

ids = [c['id'] for c in cards]
assert len(ids) == len(set(ids)), 'Duplicate card IDs found'

def norm_topic(s):
    s = (s or '').lower().replace('_', ' ').replace('-', ' ')
    s = re.sub(r'\s+', ' ', s).strip()
    if s.endswith('ies') and len(s) > 4:
        s = s[:-3] + 'y'
    elif s.endswith('s') and len(s) > 4 and not s.endswith('ss'):
        s = s[:-1]
    return s

print('cards:', len(cards))
print('duplicate-normalized-topics:', len([k for k, v in Counter(norm_topic(c['topic']) for c in cards).items() if v > 1]))

for card in cards:
    s = card['sections']
    for key in ['lecture_snippets', 'exam_questions', 'notebook_snippets', 'ai_examples', 'key_points_to_remember', 'recommended_ids']:
        assert isinstance(s.get(key), list), f"{card['id']}: {key} must be list"
    valid_ids = {
        item.get('id')
        for bucket in ['lecture_snippets', 'exam_questions', 'notebook_snippets']
        for item in s.get(bucket, [])
        if isinstance(item, dict)
    }
    for rid in s.get('recommended_ids', []):
        assert rid in valid_ids, f"{card['id']}: recommended id not found: {rid}"

print('integrity checks passed')
PY
```

Example syntax sanity check (exam topics):

```bash
python3 - <<'PY'
import json, ast

with open('topic_cards.json') as f:
    cards = [c for c in json.load(f)['cards'] if c['exam_stats']['total_hits'] > 0]

for card in cards:
    for ex in card['sections']['ai_examples']:
        ast.parse((ex.get('code') or '').strip())

print('example parse checks passed')
PY
```

## Manual Smoke Test

1. Splash shows once on first open
2. `Get Started` dismisses splash
3. `Reset intro` reopens splash
4. Refresh preserves progress
5. Swipe counts and filters behave correctly
6. Preview drag/resize persists
7. Print/PNG/PDF export works without console errors

## Contributor Notes

- Keep `app.js` and `styles.css` changes aligned.
- If schema changes, update rendering + draft selection + preview mapping together.
- If localStorage schema changes are intentional, bump storage key versions in `app.js`.
- If you adjust topic curation policy, update both this file and `TOPIC_MERGING_GUIDELINES.md`.
