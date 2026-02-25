# Python Exam Cheat Sheet Web App

This app helps students in the Intro to Python course build a focused, printable cheat sheet from real course/exam topics.

## Who This Is For

- Students preparing for the course exam/midterm
- Anyone who wants a compact, personalized review sheet from class materials

## What The App Does

- Shows topic cards you can keep or reject quickly
- Lets you choose which key points and code examples you want
- Builds a 2-page A4 cheat sheet preview
- Lets you drag/resize cards in the preview
- Exports your final sheet via Print, PNG, or PDF
- Saves your progress in your browser so refresh does not lose work

## How It Works

1. Open the app.
2. Swipe or click to keep/reject topics.
3. For kept topics, pick the points/examples you want on your sheet.
4. Open preview and arrange cards on the A4 pages.
5. Export as Print/PNG/PDF.

## Run It Locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

No npm install is required.

## Study Content Quality

- Topic cards are built from lectures, notebooks, and exam material.
- Exam-topic key points/examples are curated to keep important exam-relevant items.
- Content can still have occasional mistakes or overlap, so please report anything suspicious.

## If You Notice A Problem

Please submit an issue in this repository’s GitHub **Issues** tab.

Include:

- clear title
- what you expected vs what happened
- exact steps to reproduce
- topic/card name (if relevant)
- browser + OS
- screenshot or screen recording (if possible)
- for content issues: paste the exact key point/example and explain why it is wrong (ideally with course reference)

## Common Problems

- Lost progress: check whether browser storage was cleared/private mode used.
- Export layout odd: refresh preview and re-position cards before exporting.
- Counts look off: check active filters (search/min hits/week filters).

## Repo Files (Quick Reference)

- `index.html` - page structure
- `styles.css` - styling
- `app.js` - app logic and state
- `topic_cards.json` - topic data used by the UI
