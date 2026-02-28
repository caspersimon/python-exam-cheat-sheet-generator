# AGENTS.md

Technical handoff for coding agents and contributors working on this repository.

## Project

`python-exam-cheat-sheet-generator` is a static web app for building exam cheat sheets from curated Python topic cards.

- Frontend only (`index.html`, `app/*.js`, `styles.css` + `styles/*.css`)
- No backend/runtime services required
- Source dataset and generated card data are JSON files in repo

## Current Snapshot (2026-02-27)

- `topic_cards.json`: **28 total cards**
- Default exam deck (`only exam topics`): **21 cards**
- Duplicate normalized topic labels: **0**
- Exam-topic key points: **198**
- Exam-topic key points with optional details: **198/198**
- Optional key-point detail blocks: **247**

Curation state:

- All 21 exam-topic cards were curated using an evidence-driven pass over exam + lecture + notebook + trap data.
- `key_points_to_remember` and `ai_examples` are intentionally **variable-length** by topic based on evidence coverage.
- There is no fixed per-topic cap for key points/examples.
- Optional key-point `details` are enabled and intentionally selectable in the UI (example/table/explanation/commands).
- Exact duplicate key-point text and exact duplicate example code blocks across exam topics were removed.
- Example code blocks for exam topics and key-point detail code blocks were syntax-checked.
- A parallel Gemini generation+audit pass plus manual review was used to improve optional detail coverage and quality.

## App Behavior

- Swipe workflow for keep/reject topic cards
- Detail selection per card (key points, examples, snippets)
- 2-page A4 preview with draggable/resizable cards
- Preview editing controls for card/item edit+delete with undo (`Undo Edit`, `Ctrl/Cmd+Z`)
- Preview card lock/unlock control to freeze position/size while editing
- `Print` generates a PDF first and then prints that generated PDF
- Support prompt appears after PDF export and generated-PDF print
- Export via generated print / PNG / PDF
- First-open splash screen + `Reset intro`
- Progress persistence in `localStorage`

Storage keys:

- `python_midterm_app_state_v1`
- `python_midterm_splash_seen_v1`

## Core Files

- `index.html`: app shell and major sections
- `app/`: split frontend logic modules (loaded in order via deferred scripts)
- `scripts/smoke_ui_playwright.js`: browser smoke test (isolated Playwright install workflow)
- `scripts/stress_layout_playwright.js`: exhaustive layout stress test workflow
- `scripts/gemini_test_protocol.py`: complete automated UI QA protocol (hard gates + Gemini micro-audits)
- `scripts/gemini_capability_benchmark.py`: capability checks across JSON/code/vision/formatting tasks
- `scripts/gemini_prompt_experiments.py`: prompt-variant experiments for reliable Gemini code delegation
- `scripts/gemini_model_health.py`: lightweight model availability/quota checks before heavy Gemini runs
- `scripts/quality_dashboard.py`: aggregate health/status report across maintenance and Gemini QA artifacts
- `scripts/maintenance_audit.py`: leave-it-better maintenance audit and report generator
- `styles.css`: import root for split style modules in `styles/`
- `styles/`: split CSS by concern
- `topic_cards.json`: curated card dataset consumed by UI
- `data/study_db.json`: canonical structured source database
- `materials/`: raw lectures/notebooks/exam files

Generation/processing scripts:

- `build_topic_cards.py`
- `generate_ai_sections.py`
- `generate_key_points_and_recommendations.py`
- `enrich_key_point_details.py`

Pipeline modules:

- `pipelines/topic_cards/`
- `pipelines/ai_sections/`
- `pipelines/key_points/`
- `pipelines/key_point_details/`
- `pipelines/shared/` (shared text/json/LLM/chunk utilities)
  - `pipelines/shared/model_defaults.py` central Gemini model aliases (`fast gemini agent`, `smart gemini agent`)

Guides/docs:

- `docs/curation/TOPIC_MERGING_GUIDELINES.md`
- `docs/data/DATASET_INFO.md`
- `docs/MAINTENANCE_PROTOCOL.md`
- `docs/ROADMAP.md`
- `docs/GEMINI_PLAYBOOK.md`
- `docs/specs/`

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

- Re-run manual semantic curation (see `docs/curation/TOPIC_MERGING_GUIDELINES.md`)
- Re-check overlaps and quality drift

Week ingestion (AI-first curation):

```bash
python3 scripts/add_week_material.py --week-file data/templates/week_template.json
```

Useful flags:

- `--dry-run`: validate+curate and emit report without writing `data/study_db.json`
- `--allow-missing-sources`: bypass strict source-path existence checks
- `--replace-existing`: replace an existing week entry

## Curation Rules (Important)

When editing `topic_cards.json`:

- Use evidence-driven inclusion from course materials and exams.
- Do not enforce arbitrary fixed counts across all topics.
- Keep only important, exam-relevant content.
- Prefer full key-point detail coverage when details materially improve understanding (do not skip useful detail because of arbitrary limits).
- Remove duplicates/near-duplicates.
- Keep example code coherent and syntactically valid.
- Keep `recommended_ids` valid against card-local source snippet IDs.
- If a detail is correct and useful general Python knowledge but weakly represented in source snippets, keep it only when it does not conflict with course material.
- New week integration must run Gemini curation (`scripts/add_week_material.py`) and review the generated curation report before merge.

## GenAI QA Workflow (Current)

- Generate optional key-point details from card-local evidence (`exam_questions`, `lecture_snippets`, `notebook_snippets`, traps).
- Audit generated details for:
  - alignment to evidence
  - completeness
  - quality
- Re-generate flagged cards with audit feedback.
- Manually review remaining flagged details instead of blindly deleting all weakly linked items.

## Leave-It-Better Protocol (Mandatory)

Every implementation task must include a cleanup/improvement pass, not only the requested change.

Required sequence:

1. Implement the requested change.
2. Add at least one improvement from one category:
   - QoL
   - testing
   - structure/refactor
   - reliability bug fix
   - docs alignment
   - data quality cleanup
   - roadmap/spec planning for deferred larger issues
3. Run the matching validation command set:
   - non-UI tasks: `make leave-better`
   - UI/export tasks: `make leave-better-ui`
4. If a larger issue cannot be solved in-scope, add/update:
   - `docs/ROADMAP.md`
   - spec file under `docs/specs/`
5. Summarize both:
   - what was requested and delivered
   - what was additionally improved

Reference docs:

- `docs/MAINTENANCE_PROTOCOL.md`
- `docs/ROADMAP.md`
- `docs/specs/SPEC_TEMPLATE.md`

## Validation Checklist

```bash
node --check app/*.js
python3 -m py_compile build_topic_cards.py generate_ai_sections.py generate_key_points_and_recommendations.py enrich_key_point_details.py
python3 -m py_compile $(find pipelines -name '*.py' -type f)
python3 scripts/check_file_lengths.py
python3 scripts/maintenance_audit.py
python3 -m unittest discover -s tests -v
make smoke-ui
make stress-layout-ui
make gemini-ui-protocol
make gemini-benchmark
make gemini-prompt-experiments
make gemini-health
make quality-dashboard
make leave-better
make leave-better-ui
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

Detail coverage check (exam topics):

```bash
python3 - <<'PY'
import json

with open('topic_cards.json') as f:
    cards = [c for c in json.load(f)['cards'] if c['exam_stats']['total_hits'] > 0]

kp_total = sum(len(c['sections']['key_points_to_remember']) for c in cards)
kp_with_details = sum(1 for c in cards for kp in c['sections']['key_points_to_remember'] if kp.get('details'))
detail_total = sum(len(kp.get('details') or []) for c in cards for kp in c['sections']['key_points_to_remember'])

print('exam cards:', len(cards))
print('exam key points:', kp_total)
print('key points with details:', kp_with_details)
print('detail blocks:', detail_total)
PY
```

## Manual Smoke Test

1. Splash shows once on first open
2. `Get Started` dismisses splash
3. `Reset intro` reopens splash
4. Refresh preserves progress
5. Swipe counts and filters behave correctly
6. Preview drag/resize persists
7. Preview edit/delete actions can be undone via button and `Ctrl/Cmd+Z`; modal text edits keep native in-field undo behavior
8. `Print` generates and prints a PDF (not raw page print)
9. PDF export/print both show custom support prompt only after successful save/print trigger (not before)
10. Exported cheat sheet view has no wasted chrome: no edit/delete/resize controls and no oversized title bars.
11. Gemini protocol report (`data/test_reports/gemini_ui_test_report.json`) is green and has no fail checks.

## Contributor Notes

- Keep `app/` and `styles/` changes aligned.
- If schema changes, update rendering + draft selection + preview mapping together.
- If localStorage schema changes are intentional, bump storage key versions in `app/state-and-init.js`.
- If you adjust topic curation policy, update both this file and `docs/curation/TOPIC_MERGING_GUIDELINES.md`.
- If you defer a larger issue, track it in `docs/ROADMAP.md` and add/update a spec in `docs/specs/`.
