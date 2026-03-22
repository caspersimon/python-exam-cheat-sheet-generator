# Python Exam Cheat Sheet Builder

Build a clean, personalized Python exam cheat sheet from the course topics that actually matter.

This app is made for students. You open a topic, tick the exact key points and examples you want, and the app turns your selections into a compact two-page A4 sheet you can print or export.

Right now the app includes:

- `27` curated Python topics
- content from weeks `1-6`
- `18` topics linked to practice-exam hits
- built-in preview, edit, undo, print, PNG, and PDF export tools

## What You Can Do

- browse topics by week in the sidebar
- filter for exam-linked material
- choose exact key points, examples, and snippets instead of taking whole topics
- preview your sheet on two A4 pages before exporting
- drag, resize, lock, edit, or delete cards in the preview
- keep your progress in the browser so you can come back later

## How It Works

1. Open the app and click `Get Started`.
2. Use the left sidebar to jump to a week and topic.
3. Tick the key points, details, code examples, and snippets you want to keep.
4. Open `Preview & Export` to see your cheat sheet.
5. Rearrange or edit cards until everything fits the way you want.
6. Export as `PDF`, `PNG`, or use `Print`.

## Screenshots

### First Open

The app starts with a short intro so you know the flow straight away.

![First-run intro](docs/assets/readme/student-splash.png)

### Picking What To Keep

You do not have to accept an entire topic. Select only the exact facts and examples you want on your sheet.

![Topic explorer and item selection](docs/assets/readme/student-explorer.png)

### Previewing The Final Sheet

Once you have picked enough material, the app builds a printable two-page layout that you can tweak before exporting.

![Preview and export workspace](docs/assets/readme/student-preview.png)

## Quick Tips

- Start with exam-linked topics first if you are short on time.
- Keep only what you would genuinely want to read during revision or right before the exam.
- Use the preview early instead of waiting until the end.
- If a card is in the right place, lock it so you do not move it by accident.

## Run It Locally

This is a static website, so you do not need a backend or a big setup.

```bash
python3 -m http.server 8000
```

Then open [http://localhost:8000](http://localhost:8000).

## Course Materials

Official course files are still kept at their canonical paths under `materials/`, but there is now also a cleaner week-ordered view under [materials/by_week](materials/by_week) for easier browsing.

## Support This Project

This project was made by just one student, and the AI coding tools used to build and improve it cost real money.

If this helped you and you want to buy me a coffee to say thank you, please do:

[Buy me a coffee](https://buymeacoffee.com/caspersimon)
