# Python Exam Cheat Sheet Generator

Create a personalized, print-ready Python exam cheat sheet by swiping through topic cards, selecting only what you want, and exporting to A4 pages.

## What This App Does

- Presents Python topics as swipeable cards.
- Lets students keep/reject topics quickly (drag, buttons, arrow keys).
- Shows focused content blocks per topic:
  - Summary
  - Common Questions
  - Key Points for Reference
  - Code Examples
  - Recommended for Cheat Sheet
  - Additional Snippets
- Lets users choose exactly which items to include.
- Builds a fixed-size 2-page A4 preview with free-position, resizable cards.
- Exports via Print, PNG, or PDF.

## Current Snapshot (2026-02-25)

- `topic_cards.json` currently contains **28 total cards**.
- With default filter `only exam topics`, swipe mode currently shows **21 cards**.
- Duplicate visible topic labels were collapsed in a broad merge pass.

## Known Data-Curation Flaw (Important Handoff)

The broad duplicate-topic merge pass was **not** fully manual for every topic.

What this means:

- `Dictionaries` was manually curated in detail.
- Additional manual curation was completed for these bundles:
  - `For Loops` + `Range()`
  - condition cards (`Conditions`, `truthy_falsy`, `Boolean operators`, `comparison_operators`)
  - `*args` variants (`*args`, `*args / **kwargs`, undefined-positional `*args`)
  - default/mutable default cards (`Default arguments`, `mutable args`, `mutable_default`)
  - `Dictionaries` + `dict / average`
- Many other merged topic cards were combined via a quality-scored merge process (source union + dedupe + best-content selection), not line-by-line manual editing.

Risk:

- Some merged cards may still mix loosely related subtopics or contain uneven phrasing/detail quality.

Next-agent handoff:

- Use [`TOPIC_MERGING_GUIDELINES.md`](./TOPIC_MERGING_GUIDELINES.md) to do strict manual topic curation and semantic merge cleanup.
- Treat current `topic_cards.json` as a good baseline, but not final gold-standard curation.

## New UX Features

- First-open splash screen with a large `Get Started` button.
- Header link to [Buy Me a Coffee](https://buymeacoffee.com/caspersimon).
- `Reset intro` action in card settings (gear menu) to show splash again.
- Cleaner UI with fewer separator lines and higher section-header hierarchy.
- AI/source info popovers on `?` and sparkle icons.
- Cheat sheet cards now focus on essentials (no summary/common-questions/week-hit metadata in exported cards).

## Progress Persistence (Important)

Progress now survives hard refreshes via `localStorage`.

Persisted state includes:

- decisions (accepted/rejected)
- accepted card order
- card draft selections/toggles
- filters (search, min hits, week filters)
- layout settings (font, grid, spacing)
- source auto-select preference
- preview card geometry (position, size, z-order)

Storage keys:

- `python_midterm_app_state_v1`
- `python_midterm_splash_seen_v1`

## Folder / Repo Rename

You can safely rename the project folder to:

- `python-exam-cheat-sheet-generator`

No code path depends on the local folder name. This is a static app with relative asset paths.

## Quick Start (Local)

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

No npm install is needed for runtime.

## Project Structure

- `index.html`
  - app shell, splash overlay, swipe/preview views, drawer containers
- `styles.css`
  - visual design, section hierarchy, splash/overlay styles
- `app.js`
  - app state, rendering, interactions, persistence, preview/export logic
- `topic_cards.json`
  - card data consumed by the UI
- `study_data.json`
  - source dataset
- `build_topic_cards.py`
  - builds base card skeleton from source data (now includes better token normalization for dictionary/dictionaries)
- `generate_ai_sections.py`
  - generates summary/common-questions/code-examples content
- `generate_key_points_and_recommendations.py`
  - generates key points + recommended IDs
- `enrich_key_point_details.py`
  - adds optional key-point detail blocks
- `TOPIC_MERGING_GUIDELINES.md`
  - detailed manual workflow for semantic merge/curation handoff
- `.github/workflows/pages.yml`
  - GitHub Actions workflow for automatic GitHub Pages deploy
- `DATASET_INFO.md`
  - deeper dataset provenance/docs

## Data Pipeline

Run scripts in order when regenerating content:

```bash
python3 build_topic_cards.py
python3 generate_ai_sections.py
python3 generate_key_points_and_recommendations.py
python3 enrich_key_point_details.py
```

All scripts update `topic_cards.json` in place.

Important:

- Re-running the generation pipeline can reintroduce topic overlaps or quality drift.
- After regeneration, always run the manual merge/curation workflow in [`TOPIC_MERGING_GUIDELINES.md`](./TOPIC_MERGING_GUIDELINES.md).

## Deployment

### Recommended: GitHub Pages (Free)

This repo already includes a workflow:

- `.github/workflows/pages.yml`

What to do:

1. Push to GitHub (`main` or `master`).
2. In repo settings, open `Pages`.
3. Set source to **GitHub Actions**.
4. The `Deploy To GitHub Pages` workflow will publish the site.

### Alternative: Vercel (Free Hobby tier)

Also works well for static sites.

1. Import the repo in Vercel.
2. Framework preset: `Other`.
3. Build command: leave empty.
4. Output directory: leave empty (root static files).

Important:

- Vercel Hobby is for personal, non-commercial use.
- If your usage is commercial, use Vercel Pro (or another commercial-friendly plan).

## Does GitHub Pages Allow Cookies / localStorage?

Yes for browser-side usage:

- `localStorage` works normally.
- JS-managed cookies (`document.cookie`) also work.

This app uses `localStorage` for persistence (no backend required).

Note:

- GitHub Pages is static hosting and not a backend runtime.
- GitHub Pages also has usage policy/limits (for example, it is not meant as a general free commercial/SaaS host).

## Validation Checklist

Before sharing:

```bash
node --check app.js
python3 -m py_compile build_topic_cards.py generate_ai_sections.py generate_key_points_and_recommendations.py enrich_key_point_details.py
```

Dataset integrity check:

```bash
python3 - <<'PY'
import json, re
from collections import Counter
with open("topic_cards.json") as f:
    cards = json.load(f)["cards"]
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
print("cards:", len(cards), "duplicate-normalized-topics:", len(dups))
PY
```

Then manual smoke test:

1. First open shows splash once.
2. `Get Started` dismisses splash.
3. Gear menu contains `Reset intro`, which reopens splash.
4. Refresh keeps progress/selections.
5. Swipe interactions and counts still work.
6. Preview drag + resize works, and card positions persist after refresh.
7. Topic counts in UI match `topic_cards.json`.
8. Print/PNG/PDF export runs without console errors.

## Notes For Contributors

- Keep UI changes in `app.js` + `styles.css` aligned.
- If changing card schema, update render + draft + preview mapping together.
- If you intentionally break persisted-state compatibility, bump storage key versions in `app.js`.
- If touching topic curation, update both `topic_cards.json` and the process notes in `TOPIC_MERGING_GUIDELINES.md`.
