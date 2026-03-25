# CHANGELOG

## Review package -> final package

### Structural changes
- Removed snippet: `both-neither-all-meta-options`
- Added preset tables and preset exports
- Added question stress-test table and report
- Added actual `content/` markdown files for every piece
- Added frontend-oriented snippet grouping fields: `ui_section_slug`, `ui_section_title`, `ui_section_sort_order`, `ui_card_order`

### Feedback-driven content changes
- Rewrote method-heavy snippets to use realistic call syntax with `()`
- Added explicit outputs to high-value reference tables where that materially improved clarity
- Split the scope / `NameError` example into its own piece
- Reworked membership examples to use concrete containers and variables
- Shortened the chunking example
- Expanded the `zip()` / `enumerate()` example with clearer context
- Polished later unreviewed snippets in the same style

### Stress-test-triggered snippet edits
| Question ID                                         | Exam                           |   Q# | Primary snippet                        | Action                         | Change notes                                                                                                                                          |
|:----------------------------------------------------|:-------------------------------|-----:|:---------------------------------------|:-------------------------------|:------------------------------------------------------------------------------------------------------------------------------------------------------|
| final-exam-study-guide-trial-python-basics-2023-q24 | 2023 Trial Final Study Guide   |   24 | Object state and collection attributes | yes I edited one snippet       | Added a numbered-report-dictionary piece to the OOP collection-attributes snippet so the `enumerate(..., start=1)` garage-report pattern is explicit. |
| sample-final-plus-answers-q02                       | 2025 Sample Final Plus Answers |    2 | Object state and collection attributes | yes I edited multiple snippets | Added an average-rating OOP piece and added `round(x, n)` to the built-ins snippet so the rounded output 3.7 is directly supported.                   |
| sample-final-plus-answers-q03                       | 2025 Sample Final Plus Answers |    3 | f-strings and .format()                | yes I edited one snippet       | Expanded the f-strings snippet with a list-of-dicts print pattern and `:.1f` formatting so the correct loop/access pattern is explicit.               |

### Final counts
- Topics: **8**
- Subtopics: **20**
- Snippets: **45**
- Pieces: **137**
- Trap slugs: **75**
- Questions stress-tested: **168**
