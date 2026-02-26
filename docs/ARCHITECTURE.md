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
  - `preview-render.js`: 2-page preview rendering and selected-content projection.
  - `layout-export-utils.js`: layout variables, PNG/PDF export, shared utils.
  - `main.js`: final bootstrap (`init()`).

## Styling

- `styles.css`: import-only root stylesheet.
- `styles/`: split by concern.
  - `01-foundation.css`
  - `02-topic-card.css`
  - `03-content-controls.css`
  - `04-preview.css`
  - `05-overlays-responsive-print.css`

## Data Pipelines

Root scripts are now thin entrypoints that delegate to `pipelines/`:

- `build_topic_cards.py` -> `pipelines/topic_cards/`
- `generate_ai_sections.py` -> `pipelines/ai_sections/`
- `generate_key_points_and_recommendations.py` -> `pipelines/key_points/`
- `enrich_key_point_details.py` -> `pipelines/key_point_details/`

For `key_point_details`, the large rule chain is split into ordered matcher modules (`rules_part1.py` ... `rules_part4.py`) to preserve behavior while avoiding oversized files.

## Shared Utilities

Cross-pipeline utility logic is centralized in `pipelines/shared/`:

- `text.py`: compact/trimming/normalization helpers.
- `json_tools.py`: JSON blob extraction from LLM output.
- `llm.py`: gemini-cli invocation wrapper.
- `iterables.py`: chunking helpers.

This removes duplicated implementations across `ai_sections`, `key_points`, and `topic_cards`.

## Quality Gates

- `scripts/check_file_lengths.py`: enforces max 500 lines for code files.
- `Makefile`: unified commands for syntax checks, policy checks, and tests.
- `.github/workflows/ci.yml`: CI runs `make validate` on push/PR.
