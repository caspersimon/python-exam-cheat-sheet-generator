# AGENTS.md

Technical handoff for coding agents and contributors working on this repository.

## Project

`python-exam-cheat-sheet-generator` is an advanced static frontend project for building a personalized Python exam cheat sheet from selectable, curated snippets.

Current primary runtime stack:

- `index.html` and `styles.css` + `styles/*.css`
- `app/*.js` for a modular frontend runtime
- `new_database/exports/frontend_bundle.json` as the app payload (generated from SQLite + Markdown snippet content)
- optional legacy `topic_cards.json`/`data/study_db.json` for ingestion, curation, and QA pipelines

## Current Runbook Pointers

When doing completion/coverage work in the short-term pipeline, start from:

- `docs/curation/SNIPPET_COMPLETENESS_EXECUTION_CHECKLIST.md`
- `docs/curation/OVERNIGHT_AGENT_RUNBOOK.md`
- `data/vision_exam_pipeline/OVERNIGHT_EXECUTION_BOARD.md`
- `data/vision_exam_pipeline/plan_after_manual_synthesis.md`
- `data/vision_exam_pipeline/review_packets/round1_manual_synthesis.md`
- `python3 scripts/vision_exam_pipeline.py status --round round1`

Hard constraints for this phase:

- prioritize snippet completeness over unrelated UI/topic architecture changes
- avoid semantic drift in evidence mapping
- do not prune aggressively before the next grading pass
- do not use OCR / `pdftotext` / deterministic text-layer extraction for exam-question capture in the vision workflow

## Current Snapshot (2026-03-25)

Runtime bundle (`new_database/exports/frontend_bundle.json`):

- `bundle_version`: `new-database-v1`
- `topics`: **8**
- `subtopics`: **23**
- `snippets`: **51**
- `pieces`: **163**
- `presets`: **5**

Legacy materialization (`topic_cards.json`) in this repo is currently:

- `cards`: **27**
- `deck_groups`: **6** (`week-1` through `week-6`)
- exam-topic cards (`exam_stats.total_hits > 0`): **18**
- study DB (`data/study_db.json`): schema `3.0`, **6** weeks, **27** canonical topics

## App Behavior (Current)

- Left sidebar topic explorer with nested subtopics
- Global search + filters for `course_phase` and `recurrence_level`
- piece-first selection model (`topic -> subtopic -> snippet -> piece`)
- staged snippet panel for drag-and-drop workflow
- two-page printable preview canvas with card resize/drag/reorder/lock
- detach + re-add individual pieces as independent cards
- preview edit/delete with undo (`Ctrl/Cmd+Z` and explicit Undo)
- smart layout toggles (`auto grid`, manual columns/rows, page landscape controls)
- built-in preset packs and preset switching
- export flows: PDF, PNG, and generated-PDF print
- first-open splash with starter presets and `Reset intro` action
- progress persistence in browser storage

Storage keys:

- `python_midterm_app_state_v12`
- `python_midterm_splash_seen_v3`

## Core Files

Frontend:

- `index.html`: app shell and event wiring
- `styles.css`: root stylesheet and imports
- `styles/*.css`: split styling by feature
- `app/*.js`: startup, state, data loading, rendering, selection, preview, layout, and export

Data/build:

- `new_database/db/snippet_bank.sqlite`: SQLite content source (snippet + piece + metadata)
- `new_database/content/`: markdown piece bodies
- `new_database/exports/frontend_bundle.json`: generated payload consumed by frontend
- `scripts/build_frontend_bundle.py`: regenerates runtime bundle
- `topic_cards.json`: legacy generated card dataset
- `data/study_db.json`: canonical lecture-week-subtopic study DB (`schema 3.0`)
- `new_database/exports/preset_items.tsv`, `traps`, `keywords`, etc.

Validation / QA tooling:

- `scripts/smoke_ui_playwright.js`
- `scripts/full_ui_playwright.js`
- `scripts/stress_layout_playwright.js`
- `scripts/export_canvas_guard_playwright.js`
- `scripts/gemini_test_protocol.py`
- `scripts/gemini_capability_benchmark.py`
- `scripts/gemini_prompt_experiments.py`
- `scripts/gemini_model_health.py`
- `scripts/quality_dashboard.py`
- `scripts/maintenance_audit.py`

Generation & processing entrypoints:

- `build_topic_cards.py`
- `generate_ai_sections.py`
- `generate_key_points_and_recommendations.py`
- `enrich_key_point_details.py`
- `scripts/build_exam_builder_dataset.py`
- `scripts/build_manual_exam_builder_dataset.py` (legacy/manual dataset entrypoint)
- `scripts/ingest_raw_materials.py`
- `scripts/validate_extracted_material.py`
- `scripts/import_extracted_materials.py`
- `scripts/add_week_material.py`

Pipeline modules:

- `pipelines/topic_cards/`
- `pipelines/ai_sections/`
- `pipelines/key_points/`
- `pipelines/key_point_details/`
- `pipelines/exam_builder_dataset/`
- `pipelines/study_database/` (raw ingestion + validators + curation + lecture-first model)
- `pipelines/shared/` (`text.py`, `json_tools.py`, `llm.py`, `model_defaults.py`, `iterables.py`)

Guides:

- `docs/ARCHITECTURE.md`
- `docs/MAINTENANCE_PROTOCOL.md`
- `docs/ROADMAP.md`
- `docs/GEMINI_PLAYBOOK.md`
- `docs/TESTING.md`
- `docs/VISION_EXAM_PIPELINE.md`
- `docs/specs/`

Deploy:

- `.github/workflows/ci.yml`
- `.github/workflows/pages.yml`

## Data Pipelines

### Legacy study/curation pipeline

```bash
python3 scripts/add_week_material.py --week-file data/templates/week_template.json
python3 scripts/ingest_raw_materials.py
python3 scripts/validate_extracted_material.py
python3 scripts/import_extracted_materials.py
```

Useful flags for week ingestion:

- `--dry-run` checks + writes report
- `--allow-missing-sources`
- `--replace-existing`
- `--report-file` for audit artifact

Canonical regenerate order for legacy cards:

```bash
python3 build_topic_cards.py
python3 generate_ai_sections.py
python3 generate_key_points_and_recommendations.py
python3 enrich_key_point_details.py
```

### New frontend bundle pipeline

```bash
python3 scripts/build_frontend_bundle.py
```

Bundle shape is always `topic -> subtopic -> snippet -> piece` and must be validated by tests and app normalization logic.

### Vision exam review workflow

See `docs/TESTING.md` and `docs/VISION_EXAM_PIPELINE.md`.

Primary commands:

```bash
python3 scripts/vision_exam_pipeline.py prepare-pages
python3 scripts/vision_exam_pipeline.py seed-question-bank
python3 scripts/vision_exam_pipeline.py audit-completeness
python3 scripts/vision_exam_pipeline.py dispatch-evaluations --round round1
python3 scripts/vision_exam_pipeline.py synthesize-suggestions --round round1
python3 scripts/vision_exam_pipeline.py generate-ranking-analytics --round round1
python3 scripts/vision_exam_pipeline.py generate-review-packet --round round1
python3 scripts/vision_exam_pipeline.py status --round round1
```

## Curation Policy (Important)

When editing `topic_cards.json`:

- keep only evidence-grounded, exam-relevant material
- do not force fixed per-topic caps
- dedupe exact overlaps and obvious near-duplicates
- keep `recommended_ids` valid against source buckets
- allow richer details where they materially improve retention value
- include defaults only if they survive correctness checks

For `new_database` edits:

- keep hierarchy intact: `topic -> subtopic -> snippet -> piece`
- avoid changing `new_database` schema casually without a migration plan
- ensure SQL TSV/CSV/metadata updates match Markdown body references
- preserve `body_path` file integrity for all piece records

## Leave-It-Better Protocol (Mandatory)

Every implementation task should include an explicit cleanup/improvement pass.

1. Implement requested change.
2. Add at least one improvement from:
   - QoL
   - testing
   - structure/refactor
   - reliability
   - docs alignment
   - data quality cleanup
   - roadmap/spec planning
3. Run the matching validation command(s).
4. Update docs/roadmap/spec if architecture or behavior changed.
5. Report both requested and additional improvements.

Required commands:

- non-UI tasks: `make leave-better`
- UI/export tasks: `make leave-better-ui`

## Validation Checklist

```bash
make validate
make leave-better
make leave-better-ui
make gemini-ui-protocol
make gemini-benchmark
make gemini-prompt-experiments
make gemini-health
make quality-dashboard
make smoke-ui
make full-ui
make stress-layout-ui
make export-canvas-guard-ui
```

## Integrity Checks

Legacy topic cards:

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
    sections = card['sections']
    for key in ['lecture_snippets', 'exam_questions', 'notebook_snippets', 'ai_examples', 'key_points_to_remember', 'recommended_ids']:
        assert isinstance(sections.get(key), list), f"{card['id']}: {key} must be list"

for card in cards:
    valid_ids = {item.get('id') for bucket in ['lecture_snippets', 'exam_questions', 'notebook_snippets'] for item in card['sections'].get(bucket, []) if isinstance(item, dict)}
    for rid in card['sections'].get('recommended_ids', []):
        assert rid in valid_ids, f"{card['id']}: recommended id not found: {rid}"

print('legacy topic_cards integrity checks passed')
PY
```

Frontend bundle checks:

```bash
python3 - <<'PY'
import json

with open('new_database/exports/frontend_bundle.json') as f:
    payload = json.load(f)

piece_ids = set()
for topic in payload['topics']:
    for subtopic in topic['subtopics']:
        for snippet in subtopic['snippets']:
            for piece in snippet['pieces']:
                pid = piece['piece_id']
                assert pid not in piece_ids, f'duplicate piece id: {pid}'
                piece_ids.add(pid)

for preset in payload.get('presets', []):
    for item in preset.get('items', []):
        assert item['piece_id'] in piece_ids, f"preset item references unknown piece_id: {item['piece_id']}"

print('frontend bundle integrity checks passed', len(piece_ids), 'unique pieces')
PY
```

## Manual Smoke Test (Minimal)

1. First open shows splash, `Get Started` opens app.
2. `Reset intro` restores first-open splash.
3. Search + topic/subtopic navigation work.
4. Filters for phase/recurrence update visible snippets.
5. Selecting pieces updates staged list and progress counters.
6. Preview updates only from selected content.
7. Drag snippet from staged to preview and resize/reposition card.
8. Edit/delete/undo on preview are coherent.
9. Detached piece flow can create and remove stand-alone cards.
10. Export PDF/PNG/Print works; print uses generated PDF flow.
11. `data/test_reports/gemini_ui_test_report.json` should be clean after full protocol runs.

## Contributor Notes

- Keep `app/` and `styles/` changes synchronized.
- If frontend state schema changes, bump storage keys in `app/state-and-init.js`.
- If `new_database/exports/frontend_bundle.json` schema changes, update:
  - `app/state-and-init.js`
  - `app/exam-builder-data.js`
  - dataset tests in `tests/test_exam_builder_dataset.py`
- If curation policy changes, update this file plus:
  - `docs/curation/TOPIC_MERGING_GUIDELINES.md`
  - `docs/specs/`
- If behavior changes, update `README.md`, this `AGENTS.md`, and `docs/TESTING.md`.

@RTK.md
