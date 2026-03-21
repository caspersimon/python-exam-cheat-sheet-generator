# study_db.json — Data Reference

## Canonical Database

The canonical source dataset is:

- `data/study_db.json`

This file is the single source of truth used by the generation pipeline.

## Raw Source Materials

Course/source files are organized under `materials/`:

- `materials/lectures/`
- `materials/notebooks/`
- `materials/exams/`

`data/study_db.json` keeps references to these files in:

- `meta.sources`
- `weeks[*].sources`
- `assessments.exams[*].source`

## Top-Level Schema

```json
{
  "meta": {
    "schema_version": "3.0",
    "course": "...",
    "description": "...",
    "weeks_covered": [1, 2, 3],
    "sources": ["materials/..."],
    "last_updated": "2026-02-27T...Z"
  },
  "weeks": [
    {
      "week": 1,
      "title": "Week 1",
      "topics": [
        {
          "id": "w1-python-basics",
          "title": "Python Basics",
          "order": 1,
          "lecture_refs": [{"source": "materials/lectures/Lecture Week 1.md"}],
          "subtopics": [
            {
              "id": "w1-python-basics-execution-model",
              "title": "Execution Model, Logical Lines, and Comments",
              "order": 1,
              "knowledge_snippets": ["..."],
              "code_snippets": ["..."],
              "question_snippets": ["..."]
            }
          ]
        }
      ],
      "sources": ["materials/..."],
      "curation_meta": {
        "generator": "gemini-cli",
        "model": "gemini-2.5-pro"
      }
    }
  ],
  "assessments": {
    "exams": ["..."]
  },
  "knowledge": {
    "key_exam_patterns_and_traps": ["..."],
    "topic_analysis": {
      "topic_frequency_across_all_exams": [["topic", 3]],
      "most_tested_topics": ["topic"],
      "topics_in_lectures_not_yet_in_exams": ["topic"],
      "exam_question_counts": {
        "midterm_2024": 24,
        "total": 76
      }
    }
  }
}
```

## Week Ingestion Contract

Use `data/templates/week_template.json` as the input schema for new week material.

Required fields:

- `week` (int)
- `title` (str)
- `topics` (list[object])
- `topics[*].subtopics` (list[object])
- `topics[*].subtopics[*].knowledge_snippets` (list[object])
- `topics[*].subtopics[*].code_snippets` (list[object])
- `topics[*].subtopics[*].question_snippets` (list[object])
- `sources` (list[str])

## AI-First Ingestion Workflow

```bash
python3 scripts/add_week_material.py --week-file data/templates/week_template.json
```

Safer pre-merge dry run:

```bash
python3 scripts/add_week_material.py \
  --week-file /path/to/week_payload.json \
  --dry-run \
  --report-file data/curation_reports/week_xx_curation_report_dry_run.json
```

What it does:

1. Validates week payload shape (`v3` directly, or older flat payloads that are auto-converted).
2. Verifies payload source paths exist (unless `--allow-missing-sources` is set).
3. Runs Gemini curation on legacy lecture/notebook payloads when requested.
4. Converts the week into the lecture-first `week -> topic -> subtopic -> snippet` schema.
5. Re-validates the converted payload before integration.
6. Integrates curated week into `data/study_db.json` (unless `--dry-run`).
7. Recomputes `knowledge.topic_analysis` (unless disabled).
8. Writes a manual-review report to `data/curation_reports/`, including lecture-first assignment metadata.

## One-Time Migration (Old Monolith -> study_db)

```bash
python3 scripts/migrate_study_database.py --input /path/to/old/study_data.json --output data/study_db.json
```

This is only needed when importing historical monolithic data.
