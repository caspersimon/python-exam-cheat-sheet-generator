# study_data.json — README for downstream agents

## Purpose

This file (`study_data.json`) contains all structured study material extracted from the course
"Introduction to Python" (Weeks 1–3), compiled for midterm exam cheat-sheet preparation.
It is the single source of truth for a downstream agent tasked with analysing trends,
identifying high-yield topics, and generating cheat sheet content.

---

## Source files

| File | Type | What was extracted |
|---|---|---|
| `Lecture Week 1.md` | Lecture slides | Concepts, code snippets, in-lecture Q&As |
| `Lecture Week 2.md` | Lecture slides | Concepts, code snippets, in-lecture Q&As |
| `Lecture Week 3.md` | Lecture slides | Concepts, code snippets, in-lecture Q&As |
| `Notebook Week 1.ipynb` | Jupyter notebook | All non-empty cells with outputs, topic-tagged |
| `Notebook Week 2.ipynb` | Jupyter notebook | All non-empty cells with outputs, topic-tagged |
| `Notebook Week 3.ipynb` | Jupyter notebook | All non-empty cells with outputs, topic-tagged |
| `trial midterm.pdf` | Trial midterm 24/25 (PDF, published 15/04/2025) | 24 questions, options, answers (derived by analysis — no key in PDF) |
| `2023.pdf` | Trial midterm 22/23 (PDF, scanned) | 16 questions, options, answers (read from filled radio buttons in scan) |
| `2024.pdf` | Trial midterm 23/24 (PDF) | 24 questions, options, answers (read from boxed letters in PDF) |
| `Midterm Extra Practice.txt` | Practice questions (text) | 12 questions, options, answers (derived by analysis — no key in file) |

---

## Top-level JSON structure

```
{
  "meta":                         { course info, source files }
  "lectures":                     [ 3 lecture objects, one per week ]
  "notebooks":                    [ 340 cell objects across weeks 1–3 ]
  "exams":                        [ 4 exam objects, 76 questions total ]
  "key_exam_patterns_and_traps":  [ 21 documented trap/trick patterns ]
  "topic_analysis":               { frequency counts, most-tested topics, gaps }
}
```

---

## Section: `lectures`

Array of 3 objects (one per week). Each object has:

```json
{
  "week": 1,
  "topics": ["...", "..."],         // high-level topic list for the week
  "concepts": [                     // detailed concept entries
    {
      "topic": "Mutable vs immutable types",
      "explanation": "...",
      "week": 1,
      "code_examples": [            // present on most concepts
        {
          "description": "...",
          "code": "..."             // runnable Python, with inline comments
        }
      ]
    }
  ],
  "lecture_questions": [            // Q&As that appeared as slides in the lecture
    {
      "question": "...",
      "options": { "a": "...", "b": "..." },   // present on MC questions
      "correct": "a",
      "explanation": "...",
      "week": 1,
      "topic": "..."
    }
  ]
}
```

**Weeks and their major themes:**

| Week | Key topics |
|---|---|
| 1 | Objects, types, names, mutability, indexing, slicing, range, imports |
| 2 | Augmented ops, dicts, lists, sets, conditions, loops, walrus, truthy/falsy, type conversion |
| 3 | Functions (all aspects): scope, *args/**kwargs, defaults, lambdas, map/filter/reduce, sorted |

---

## Section: `notebooks`

Flat array of 340 cell objects. Each object:

```json
{
  "cell_index": 42,          // original index in the .ipynb file
  "week": 1,                 // which week's notebook (1, 2, or 3)
  "cell_type": "code",       // "code" or "markdown"
  "topic": "slicing",        // manually assigned topic label (see list below)
  "is_advanced_optional": false,  // true = cells starting with # (beyond-exam content)
  "source": "...",           // full cell source text
  "outputs": ["..."]         // list of captured stdout/result strings (may be empty)
}
```

### Important flag: `is_advanced_optional`

Cells with `"is_advanced_optional": true` are marked with a leading `#` in the notebook,
meaning the lecturer explicitly flagged them as beyond the exam scope (e.g., integer
interning, bytecode inspection, IPython tricks). **Filter these out** for cheat-sheet
generation unless you specifically want advanced content.

### Topic labels used in notebooks

The `topic` field uses these values (can be used to group/filter cells):

**Week 1:** `intro`, `comments`, `objects`, `assignment`, `identity_id`, `types`,
`type_conversion`, `names`, `arithmetic_operators`, `comparison_operators`,
`mutable_immutable`, `len_function`, `indexing`, `slicing`, `line_joining`,
`strings`, `strings_fstrings`, `strings_quotes`, `strings_escape`, `imports`,
`advanced_optional`

**Week 2:** `augmented_operators`, `dictionaries`, `lists`, `conditions`,
`conditions_precedence`, `conditional_expression`, `for_loops`, `looping_dicts`,
`enumerate`, `zip`, `while_loops`, `walrus_operator`, `type_conversion`,
`truthy_falsy`, `fun_example`, `advanced_optional`

**Week 3:** `function_definition`, `function_calls`, `return_statement`,
`multiple_returns`, `pass`, `scope`, `positional_args`, `args_star`,
`mutable_args`, `function_factories`, `keyword_args`, `mixed_args`,
`default_args`, `mutable_defaults`, `lambda`, `map_function`, `filter_function`,
`reduce_function`, `sorted_key`, `max_key`, `sorted_builtins`, `for_vs_while`,
`nested_loops`, `hw_question3`, `hw_question5`, `hw_question9`

---

## Section: `exams`

Array of 4 exam objects:

```json
{
  "source": "2024.pdf",
  "exam_label": "midterm_2024",
  "year": "2023-2024",
  "note": "...",              // how the answer key was determined
  "questions": [
    {
      "number": 3,
      "topic": "mutable / immutable",
      "week": 1,
      "question": "...",      // full question text, including any code
      "code_context": "...",  // present on some questions with longer code blocks
      "options": {
        "A": "...",
        "B": "...",
        "C": "...",
        "D": "..."
      },
      "correct": "B",         // the correct answer letter
      "explanation": "..."    // step-by-step reasoning for the correct answer
    }
  ]
}
```

### Exam labels and answer key provenance

| `exam_label` | Source | Year | Questions | How answers determined |
|---|---|---|---|---|
| `trial_midterm` | `trial midterm.pdf` | 2024–2025 | 24 | Derived by code analysis (no key in PDF) |
| `midterm_2023` | `2023.pdf` | 2022–2023 | 16 | Read from filled radio buttons in scanned PDF |
| `midterm_2024` | `2024.pdf` | 2023–2024 | 24 | Read from boxed letter in PDF |
| `extra_practice` | `Midterm Extra Practice.txt` | unknown | 12 | Derived by code analysis (no key in file) |

> ⚠️ All three PDF exams are **trial midterms** — none are official real exams. The filenames
> (`2023.pdf`, `2024.pdf`) refer to the academic year of the trial midterm, not a real exam year.

### Question fields reference

| Field | Always present | Notes |
|---|---|---|
| `number` | ✓ | Question number within exam |
| `topic` | ✓ | Fine-grained topic label |
| `week` | ✓ | Which lecture week the topic belongs to |
| `question` | ✓ | Full question text |
| `code_context` | some | Present when question includes longer code that needed separate capture |
| `options` | ✓ | Dict with keys A/B/C/D (or a/b/c/d for extra_practice) |
| `correct` | ✓ | The correct answer letter |
| `correct_override` | some | Use this instead of `correct` where noted |
| `explanation` | ✓ | Full reasoning trace |
| `note` | some | Additional clarification |

> ⚠️ A handful of questions in `trial_midterm` have a `"correct_override"` field.
> Where present, **use `correct_override` as the authoritative answer** — it supersedes `correct`.
> This was added during verification to fix a reasoning error in the initial pass.

---

## Section: `key_exam_patterns_and_traps`

Array of 21 objects, each documenting a specific trap or trick that appears in exams:

```json
{
  "pattern": "Slicing creates a NEW object",
  "trap": "l2=l1 vs l2=l1[:] — l2=l1 shares the SAME object...",
  "weeks": [1],
  "appears_in_exams": ["trial_midterm", "midterm_2023", "midterm_2024", "extra_practice"]
}
```

The `appears_in_exams` list tells you which exams have tested this trap —
useful for identifying the highest-priority traps to put on a cheat sheet.

---

## Section: `topic_analysis`

```json
{
  "topic_frequency_across_all_exams": [ ["slicing", 5], ["scope / global", 4], ... ],
  "most_tested_topics": ["slicing", "scope / global", ...],
  "topics_in_lectures_not_yet_in_exams": ["line_joining", "walrus operator in depth", ...]
}
```

Use `topic_frequency_across_all_exams` to rank topics by exam importance.
Use `topics_in_lectures_not_yet_in_exams` to identify topics that could appear
on a future exam but haven't yet — these are lower priority but worth a brief note.

---

## Suggested queries for a downstream agent

### "What topics appear most often across all exams?"
→ Read `topic_analysis.topic_frequency_across_all_exams`, sorted descending.

### "Show me all exam questions about slicing"
→ Filter `exams[*].questions` where `topic` contains `"slicing"`.

### "What are the most dangerous traps to memorise?"
→ Read `key_exam_patterns_and_traps`, sort by length of `appears_in_exams` list descending.

### "Give me all code examples for scope/closures from the notebooks"
→ Filter `notebooks` where `topic` in `["scope", "function_factories"]` and `cell_type == "code"` and `is_advanced_optional == false`.

### "What code examples does the lecture give for mutable defaults?"
→ Filter `lectures[week=3].concepts` where `topic == "Default arguments"`, then read `code_examples`.

### "What were the exact wrong answers offered for Q3 of the 2024 exam?"
→ Read `exams` where `exam_label == "midterm_2024"`, question `number == 3`, field `options`.

### "Which topics appear in lectures but have never been tested?"
→ Read `topic_analysis.topics_in_lectures_not_yet_in_exams`.

---

## Notes and caveats

- **The exam format is multiple-choice** (4 options). Options are sometimes "Both work",
  "Neither works", "All of the above", "An error" — these appear frequently and are
  worth including on a cheat sheet.

- **Week coverage on the exam:** All 3 weeks are tested. The trial midterm (24/25) and
  the 2024 trial midterm each have 24 questions; the 2023 trial midterm has 16. All three
  cover the widest range of Week 3 function topics.

- **The 2023 PDF (`2023.pdf`) is a scanned document** — some question text was reconstructed
  from visual inspection. Treat those answers as high-confidence but not perfect.

- **Notebook cells tagged `is_advanced_optional: true`** are beyond exam scope per the
  lecturer's own marking. Safe to ignore for cheat-sheet purposes.

- **The `hw_question3`, `hw_question5`, `hw_question9` notebook topics** correspond to
  the worked homework solutions shown at the end of the Week 3 lecture — these are
  explicitly flagged as exam material by the lecturer.
