# Python Midterm Cheat Sheet Builder

This project is a **Tinder-style web app** for building a personalized, two-page (double-sided A4) Python midterm cheat sheet.

The app lets students swipe through topic cards, select only the snippets they want, and export a compact print-ready sheet.

## Important file rename

The previous dataset-focused README has been preserved as:

- `DATASET_INFO.md`

If you need deep details about the original extracted dataset (`study_data.json`), read that file first.

## Current status (as of 2026-02-25)

Implemented and working:

- Minimal swipe UI with hidden drawers/panels (clean main interface)
- Swipe decisions via drag, buttons, and left/right arrow keys
- Card metadata: lecture week(s), exam hit frequency, exam-source breakdown
- Sections visible by default (no nested collapse interactions)
- Low-value one-line notebook/lecture snippets filtered out
- AI sections at top of each card:
  - AI Summary
  - AI Common Questions
  - Key Points to Remember
  - AI Examples
- Source split sections:
  - Recommended for Cheat Sheet
  - Additional Snippets
- Per-item checkboxes with live `x/y selected` counters
- Gear settings on card for:
  - section visibility toggles
  - default source selection mode (`manual` or `auto-select recommended`)
- Default behavior now selects **nothing** unless user enables auto-select recommended
- Preview mode with 2 A4 pages, drag-to-reorder cards, auto grid density + manual row/column overrides
- Export options: Print, PNG, PDF
- Exam question rendering fixes:
  - preserves multiline formatting
  - splits prompt vs code into `<p>` and `<pre>`
  - keeps options readable and code-like options in `<pre>`

## Quick start

Run the app locally as a static site:

```bash
cd "/Users/juliuseikmans/Desktop/Studies/2025-2026/intro to python/claude database"
python3 -m http.server 8000
# open http://localhost:8000
```

No npm install is required for runtime. Frontend libraries are loaded via CDN in `index.html`.

## Project structure

- `index.html`
  - app shell, swipe/preview views, drawer containers, control IDs
- `styles.css`
  - modern visual theme and flattened section styling
- `app.js`
  - all state, rendering, interaction handlers, preview/export logic
- `study_data.json`
  - base extracted course/exam dataset
- `topic_cards.json`
  - app-ready cards consumed by UI
- `build_topic_cards.py`
  - transforms `study_data.json` -> `topic_cards.json` skeleton + placeholders
- `generate_ai_sections.py`
  - fills AI Summary / AI Common Questions / AI Examples using Gemini
- `generate_key_points_and_recommendations.py`
  - fills Key Points + Recommended IDs using Gemini
- `DATASET_INFO.md`
  - detailed dataset documentation from the previous README

## Data flow

1. Build base topic cards:

```bash
python3 build_topic_cards.py
```

2. Generate AI summary/common questions/examples:

```bash
python3 generate_ai_sections.py
```

3. Generate key points + recommended snippet IDs:

```bash
python3 generate_key_points_and_recommendations.py
```

All scripts read/write `topic_cards.json` in place.

## `topic_cards.json` schema (what the UI expects)

Top-level:

- `meta`
- `cards[]`

Per card:

- `id`
- `topic`
- `canonical_topic`
- `weeks[]`
- `exam_stats`
  - `total_hits`
  - `by_exam`
  - `coverage_count`
- `related_topics[]`
- `trap_patterns[]`
- `sections`
  - `lecture_snippets[]`
  - `exam_questions[]`
  - `notebook_snippets[]`
  - `ai_summary`
  - `ai_common_questions`
  - `ai_examples[]`
  - `key_points_to_remember[]`
  - `recommended_ids[]`

### UI section mapping

In `app.js`, card selections are stored in draft state with keys:

- `aiExamples`
- `keyPoints`
- `recommended`
- `additional`

If you add/remove sections in data, update:

- `ensureDraft(...)`
- `sectionToSelectionKey(...)`
- card render functions
- preview render functions

## UX constraints from user requests (preserve these)

These were explicit user preferences and should remain unless asked otherwise:

- Keep main UI minimal (hide controls behind drawers/buttons)
- Avoid nested scroll regions and stacked box-inside-box visuals
- Show content sections directly; use section headers, not heavy containers
- Keep the old top chip/toggle strip hidden behind card settings (gear)
- Keep `x/y selected` counters accurate in real time
- Do not auto-select snippets by default
- Provide setting to auto-select Recommended snippets
- Keep exam/code formatting readable (multiline + code blocks)
- Filter out low-value one-line snippets without useful code/content

## Important implementation details

### Source split logic

`app.js` constructs combined source items from exam/lecture/notebook snippets, then splits into:

- `recommended`: from `sections.recommended_ids` (with runtime fallback if missing)
- `additional`: everything else

### Key points placement

Rendered directly below AI Common Questions and above AI Examples.

### Formatting safeguards

Question rendering functions (`renderQuestionContent`, `splitPromptAndCode`, `isCodeBlockLikely`) are critical for not flattening code into one line.

## Known caveats

- `topic_cards.json` currently has 87 cards.
- Most cards have `recommended_ids`; runtime fallback handles cards where it is missing/empty.
- Gemini-generated text is useful but not perfect; quality varies by topic.

## Validation checklist after edits

Run these before handing off:

```bash
node --check app.js
python3 -m py_compile build_topic_cards.py generate_ai_sections.py generate_key_points_and_recommendations.py
```

Then manually smoke-test in browser:

1. Swipe mode loads and shows card sections in correct order.
2. Gear opens settings; default selection mode changes behavior for new cards.
3. `x/y selected` counts update when toggling checkboxes.
4. Exam questions show multiline code in `<pre>` (not flattened).
5. Preview shows accepted cards with selected sections.
6. Auto-grid/manual rows+columns both work.
7. Print/PNG/PDF actions trigger without JS errors.

## If you are the next model continuing work

Recommended first steps:

1. Read this README.
2. Read `DATASET_INFO.md` if you need dataset provenance details.
3. Inspect `app.js` render/state functions before changing schema.
4. Use targeted changes (avoid broad refactors unless requested).
5. Re-run the validation checklist.

