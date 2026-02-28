# Architecture

## Overview

The app is still a static frontend with JSON-backed content, but the codebase is now split into focused modules to keep files small and easier to evolve.

## Frontend

- `index.html`: app shell and script/style boot order.
- `app/`: JavaScript modules loaded in order (classic deferred scripts).
  - `state-and-init.js`: global state, refs, boot, top-level event binding.
  - `splash-storage.js`: splash + localStorage hydration/persistence.
  - `preview-pointer.js`: preview drag/resize pointer mechanics.
  - `view-and-data.js`: filtering, deck selection, draft initialization.
  - `render-card-sections.js`: swipe-card rendering and source section rendering.
  - `text-render-utils.js`: inline/text/code parsing and render helpers.
  - `card-interactions.js`: input/click handlers, swipe decisions, undo.
  - `preview-card-render.js`: preview card/item rendering with edit/delete controls.
  - `preview-editing.js`: preview item/card edit/delete actions.
  - `preview-render.js`: 2-page preview rendering and selected-content projection.
  - `preview-history.js`: preview edit/delete undo snapshots.
  - `layout-export-utils.js`: layout variables, PNG export, shared helpers.
  - `pdf-export-utils.js`: generated-PDF export + generated-PDF print flow.
  - `main.js`: final bootstrap (`init()`).

## Styling

- `styles.css`: import-only root stylesheet.
- `styles/`: split by concern.
  - `01-foundation.css`
  - `02-topic-card.css`
  - `03-content-controls.css`
  - `04-preview.css`
  - `05-overlays-responsive-print.css`
  - `06-preview-editing.css`

## Data Pipelines

Root scripts are now thin entrypoints that delegate to `pipelines/`:

- `build_topic_cards.py` -> `pipelines/topic_cards/`
- `generate_ai_sections.py` -> `pipelines/ai_sections/`
- `generate_key_points_and_recommendations.py` -> `pipelines/key_points/`
- `enrich_key_point_details.py` -> `pipelines/key_point_details/`

For `key_point_details`, the large rule chain is split into ordered matcher modules (`rules_part1.py` ... `rules_part4.py`) to preserve behavior while avoiding oversized files.

Canonical study data now lives in `data/study_db.json` (week-structured database). The topic-card pipeline materializes this DB into the shape needed for card generation at runtime.

Week ingestion flow:

- `scripts/add_week_material.py`: adds one week payload to `data/study_db.json`.
- `pipelines/study_database/curation.py`: AI-first curation via `gemini-cli` (concept cleaning, notebook cell filtering/scoring).
- `pipelines/study_database/validators.py`: payload preflight validation and source-path checks.
- `data/curation_reports/`: manual-review artifacts for each ingestion run.

Testing/QA automation:

- `scripts/smoke_ui_playwright.js`: browser smoke flow + screenshot/probe generation.
- `scripts/export_canvas_guard_playwright.js`: dedicated export-canvas clipping guard with artifact output.
- `scripts/gemini_test_protocol.py`: deterministic gates + Gemini micro-audits for UI/export quality.
- `scripts/gemini_capability_benchmark.py`: model capability checks for JSON/code/vision/format contracts.
- `scripts/gemini_prompt_experiments.py`: prompt-variant A/B experiments for Gemini code delegation.
- `scripts/gemini_model_health.py`: fast availability/quota checks to pick a viable model route.
- `scripts/quality_dashboard.py`: aggregated cross-report project health summary.
- `scripts/maintenance_audit.py`: repository maintenance system audit (`leave-it-better` checks + actionable report).
- `data/test_reports/`: generated QA reports.

## Shared Utilities

Cross-pipeline utility logic is centralized in `pipelines/shared/`:

- `text.py`: compact/trimming/normalization helpers.
- `json_tools.py`: JSON blob extraction from LLM output.
- `llm.py`: gemini-cli invocation wrapper.
- `model_defaults.py`: centralized Gemini model aliases (`FAST_GEMINI_AGENT`, `SMART_GEMINI_AGENT`) for pipelines/scripts.
- `iterables.py`: chunking helpers.

This removes duplicated implementations across `ai_sections`, `key_points`, and `topic_cards`.

## Quality Gates

- `scripts/check_file_lengths.py`: enforces max 500 lines for code files.
- `scripts/maintenance_audit.py`: enforces maintenance-system invariants and quality drift detection.
- `Makefile`: unified commands for syntax checks, policy checks, and tests.
- `.github/workflows/ci.yml`: CI runs `make validate` on push/PR.

## Maintenance System

- `docs/MAINTENANCE_PROTOCOL.md`: mandatory post-task cleanup protocol for agents.
- `docs/GEMINI_PLAYBOOK.md`: dated Gemini model routing + prompting/supervision policy.
- `docs/ROADMAP.md`: tracked larger issues and improvements.
- `docs/specs/`: implementation specs linked from roadmap entries.
