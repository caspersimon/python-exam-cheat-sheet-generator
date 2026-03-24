# study_db.json — Data Reference

## Canonical Database

The canonical source dataset is:

- `data/study_db.json`

This file is the single source of truth used by the generation pipeline.

Related generated audit artifact:

- `data/quality/source_coverage_report.json`

This report records coverage for homework exercises and assessment questions against the current `topic_cards.json` output.

## Exam Curation Data

`data/study_db.json` remains the canonical course-content database, but the vision-first exam-curation workflow keeps its review products separate from the main study DB.

Vision-only capture rule:

- exam pages are rendered to PNGs and reviewed by agents with vision
- exam question capture should not rely on `pdftotext`, OCR, or other deterministic text-layer extraction
- legacy imports in `data/import_payloads/post_midterm_assessments/` and `data/import_payloads/post_midterm_agent/` are treated as seed material, not final ground truth, until they are superseded by reviewed vision records

Derived exam artifacts live under `data/vision_exam_pipeline/` as separate JSON products:

- `page_manifest.json`
  - persistent manifest of target exams and rendered/reused page PNG paths
- `exam_question_bank.json`
  - canonical per-exam reviewed question bank with alias metadata, provenance, and blocked question slots
- `exam_question_bank_completeness.json`
  - completeness report that fails open questions into explicit blocked slots
- `selectable_items_snapshot.json`
  - stable snapshot of the current selectable snippet universe used for review rounds
- `evaluations/<round>.json`
  - per-question snippet evaluation records, answerability notes, and suggested changes
- `synthesis/<round>.json`
  - grouped edit/addition suggestions with pros, cons, and human-review status
- `analytics/<round>.json` and `analytics/<round>.md`
  - week-level snippet-usage distributions and ranking-prep summaries
- `review_packets/<round>.json` and `review_packets/<round>.md`
  - human-facing review packet that clusters round findings into decision-ready themes and top-snippet summaries
- `work_packets/extractions/*.json`
  - per-exam vision-review capture packets
- `work_packets/evaluations/<round>/*.json`
  - per-exam question-to-snippet review packets

The current render-and-review packet used by the audit workflow is still the fastest way to bootstrap those artifacts:

- `tmp/exam_coverage_audit/manifest.json`
- `tmp/exam_coverage_audit/selectable_items.json`
- `tmp/exam_coverage_audit/pages/<exam-id>/page-XX.png`

See [RM-009 Vision-First Exam Curation Pipeline](../specs/RM-009-vision-first-exam-curation-pipeline.md) for the workflow contract.

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

## topic_cards.json Dense Curation Notes

The materialized `topic_cards.json` now supports denser exam-focused structures in addition to raw source buckets:

- `sections.ai_common_questions.items`
  - structured common-question blocks with `summary`, `detail`, optional `extra`, optional `code`, and optional `table`
- `sections.ai_examples[*].output`
  - optional explicit output/result text rendered beneath code examples when the example depends on a concrete result
- `sections.key_points_to_remember[*].details`
  - optional `example`, `table`, `commands`, and `explanation` details for high-density reference content

The intended build strategy is:

1. mine lecture/questions/exams/notebooks/homework for exam-relevant patterns,
2. compress them into denser representations when that preserves exam usefulness,
3. keep raw source snippets only when they still add standalone value.

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
