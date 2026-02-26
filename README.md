# Python Exam Cheat Sheet Generator

> **[🚀 Open the app](https://caspersimon.github.io/python-exam-cheat-sheet-generator/)** — no installation needed, runs in your browser.

A free web tool that helps you build a personalised, printable cheat sheet for your Python exam — in just a few minutes.

---

## What is this?

Preparing for a Python exam and want a compact reference sheet you can actually bring into the exam?

This tool shows you all the important Python topics (taken from real lecture notes, notebooks, and past exam questions) one at a time. You swipe through them like a card deck, keeping what you want and skipping what you already know. At the end you get a neat 2-page A4 cheat sheet you can print or export as a PDF.

**No sign-up. No install. Works in any modern browser.**

---

## How to use it

1. **Open the app** — [caspersimon.github.io/python-exam-cheat-sheet-generator](https://caspersimon.github.io/python-exam-cheat-sheet-generator/)
2. **Swipe through topic cards** — click "Add (→)" to keep a topic or "No Thanks (←)" to skip it.
3. **Customise each card** — for every kept topic, tick the key points and code examples you actually want on your sheet. You can also expand optional detail blocks (tables, mini-examples, explanations) and include only what's useful.
4. **Preview your sheet** — click "Preview & Export" to see a live 2-page A4 layout. Drag and resize cards to arrange them exactly how you like.
5. **Export** — hit Print, PNG, or PDF to save your finished cheat sheet.

Your progress is saved automatically in your browser, so you can close the tab and come back later without losing anything.

---

## Features at a glance

| Feature | Details |
|---|---|
| Topic cards | 28 topics drawn from lectures, notebooks, and past exam questions |
| Default exam deck | 21 topics that appeared in practice exams |
| Filters | Filter by week, minimum exam appearances, or search by keyword |
| Key points | 198 curated key points with optional expandable detail blocks |
| Export formats | Print, PNG, PDF |
| Data persistence | Saved in your browser's local storage — no account needed |

---

## Running it locally (optional)

You don't need to install anything to use the app — just open the link above.

If you want to run it on your own machine:

```bash
# 1. Clone this repository
git clone https://github.com/caspersimon/python-exam-cheat-sheet-generator.git
cd python-exam-cheat-sheet-generator

# 2. Start a local web server
python3 -m http.server 8000

# 3. Open http://localhost:8000 in your browser
```

---

## Something looks wrong?

Content mistakes, broken features, layout bugs — all welcome in the [Issues tab](https://github.com/caspersimon/python-exam-cheat-sheet-generator/issues).

When reporting, please include:

- What you expected to happen and what actually happened
- The topic or key-point name (if it's a content issue)
- Your browser and operating system
- A screenshot if possible

**Common fixes:**
- *Lost my progress* — check if you were in private/incognito mode, or if browser storage was cleared.
- *Export looks odd* — try refreshing the preview and re-positioning the cards before exporting.
- *Card count looks wrong* — check the active filters (search box, week filter, minimum hits).

---

## Repo overview (for contributors)

| File | Purpose |
|---|---|
| `index.html` | App structure |
| `styles.css` | All styling |
| `app.js` | App logic, state management, persistence |
| `topic_cards.json` | The topic data consumed by the UI |
| `AGENTS.md` | Technical handoff for coding agents / contributors |
| `TOPIC_MERGING_GUIDELINES.md` | Curation guidelines for maintainers |

---

If this saved you time, consider [buying me a coffee ☕](https://buymeacoffee.com/caspersimon).
