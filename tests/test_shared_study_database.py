from __future__ import annotations

import unittest

from pipelines.shared.study_database import flatten_study_db_for_pipeline


class SharedStudyDatabaseTests(unittest.TestCase):
    def test_flatten_v3_preserves_week_local_notebook_cell_indexes(self) -> None:
        db = {
            "meta": {"schema_version": "3.0"},
            "weeks": [
                {
                    "week": 4,
                    "topics": [
                        {
                            "id": "topic-1",
                            "title": "Objects",
                            "subtopics": [
                                {
                                    "id": "subtopic-1",
                                    "title": "Classes",
                                    "knowledge_snippets": [],
                                    "question_snippets": [],
                                    "code_snippets": [
                                        {
                                            "source_type": "notebook",
                                            "content": "print('week4')",
                                            "outputs": [],
                                            "source_refs": [{"original_id": "notebook-cell-8"}],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
                {
                    "week": 5,
                    "topics": [
                        {
                            "id": "topic-2",
                            "title": "Files",
                            "subtopics": [
                                {
                                    "id": "subtopic-2",
                                    "title": "Reading",
                                    "knowledge_snippets": [],
                                    "question_snippets": [],
                                    "code_snippets": [
                                        {
                                            "source_type": "notebook",
                                            "content": "print('week5')",
                                            "outputs": [],
                                            "source_refs": [{"original_id": "notebook-cell-2"}],
                                        }
                                    ],
                                }
                            ],
                        }
                    ],
                },
            ],
            "assessments": {"exams": []},
            "knowledge": {},
        }

        materialized = flatten_study_db_for_pipeline(db)

        self.assertEqual([8, 2], [item["cell_index"] for item in materialized["notebooks"]])


if __name__ == "__main__":
    unittest.main()
