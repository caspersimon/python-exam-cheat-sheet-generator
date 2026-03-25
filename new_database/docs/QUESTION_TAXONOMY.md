# Question taxonomy and exam-pattern analysis

> [!info] Final-release note
> The taxonomy remained stable through the final stress-test pass. Only some snippet mappings and coverage details were refined.

> [!summary] Purpose
> This document is the structured output of the first-pass close inspection.
> It answers:
> - what topics the exams actually test
> - how the questions are usually phrased
> - which patterns recur often enough to deserve dedicated snippet coverage

## 1. Dataset scope

- **7 supplied exams**
- **168 total questions**
- **5 deduped exam families** used for recurrence analysis

The family grouping matters because some papers are near-duplicate variants.

## 2. Broad topic map

The manual coding settled on these main topics:

1. **Exam survival** — elimination strategy and cross-topic trap patterns  
2. **Core Python** — truthiness, indexing, slicing, loops, `zip`, `enumerate`, built-ins  
3. **Functions & scope** — return behavior, defaults, keyword binding, `*args`, `**kwargs`, scope, imports, lambda  
4. **Strings** — method semantics, formatting, parsing  
5. **Dictionaries & comprehensions** — build/count/aggregate, dict iteration, dict/list/set comprehensions  
6. **OOP** — `__init__`, `self`, attributes, state, methods, comparison/reporting  
7. **Datetime** — parsing/formatting, arithmetic, overlap logic, date sequences  
8. **Pandas** — selection, boolean masks, vectorized transforms, construction, sorting

## 3. Topic counts

### Deduped exam-family view

| Exam family                              |   Core Python |   Datetime |   Dictionaries & comprehensions |   Functions & scope |   OOP |   Pandas |   Strings |
|:-----------------------------------------|--------------:|-----------:|--------------------------------:|--------------------:|------:|---------:|----------:|
| 2022 final                               |             4 |          2 |                               5 |                   4 |     2 |        4 |         3 |
| 2023 resit family                        |             3 |          2 |                               4 |                   4 |     3 |        5 |         3 |
| 2023 trial                               |             6 |          3 |                               3 |                   3 |     3 |        3 |         3 |
| 2024 trial                               |             7 |          3 |                               3 |                   2 |     3 |        3 |         3 |
| 2025 sample-family / later-course family |             4 |          3 |                               6 |                   4 |     2 |        2 |         3 |

### Full-bank view

| Topic                         |   Questions |
|:------------------------------|------------:|
| Dictionaries & comprehensions |          31 |
| Core Python                   |          31 |
| Functions & scope             |          25 |
| Pandas                        |          24 |
| Strings                       |          21 |
| OOP                           |          18 |
| Datetime                      |          18 |

> [!note] Reading the table
> The deduped family view is the better “what do exam-makers like?” view.
> The full-bank view is still useful for implementation because it reflects how often students are likely to see the pattern while browsing past material.

## 4. Course-phase balance

The final is best modeled as **cumulative with a post-midterm tilt**.

### Deduped family phase counts

| Exam family                              |   Post-midterm |   Pre-midterm |
|:-----------------------------------------|---------------:|--------------:|
| 2022 final                               |             13 |            11 |
| 2023 resit family                        |             15 |             9 |
| 2023 trial                               |             14 |            10 |
| 2024 trial                               |             14 |            10 |
| 2025 sample-family / later-course family |             13 |            11 |

Practical consequence for cheat-sheet generation:

- do **not** build a cheat sheet that only knows pandas/OOP/datetime
- but do give slightly more weight to post-midterm snippets in any default preset

## 5. Question-form taxonomy

### Deduped family counts

| Question form                          |   Questions |
|:---------------------------------------|------------:|
| Choose the code that works             |          52 |
| Predict the output                     |          30 |
| Match equivalent expressions / outputs |          12 |
| Choose the code that fails             |           8 |
| Explain why a mismatch/error happens   |           8 |
| Find the odd one out                   |           4 |
| Fill a template / blank                |           2 |
| Identify the bad line                  |           2 |
| Reverse-engineer a transform           |           1 |
| Select the true statement              |           1 |

### Full-bank counts

| Question form                          |   Questions |
|:---------------------------------------|------------:|
| Choose the code that works             |          74 |
| Predict the output                     |          43 |
| Match equivalent expressions / outputs |          16 |
| Choose the code that fails             |          13 |
| Explain why a mismatch/error happens   |          11 |
| Find the odd one out                   |           5 |
| Fill a template / blank                |           2 |
| Identify the bad line                  |           2 |
| Reverse-engineer a transform           |           1 |
| Select the true statement              |           1 |

## 6. What these forms really mean

> [!tip] Translation layer
> The wording changes, but the underlying tasks are surprisingly stable.

| Question form | What the student is really doing |
|:--|:--|
| Choose the code that works | Spot the one option with the right syntax + right object type + right return behavior |
| Predict the output | Simulate execution without running the code |
| Choose the code that fails | Notice the one hidden trap that breaks the option |
| Match equivalent expressions / outputs | Compare semantics instead of surface syntax |
| Explain why a mismatch/error happens | Recognize the underlying rule that the distractor violated |
| Odd one out | Use elimination across a small concept family |
| Identify the bad line | Localize a single syntax or object-type mistake |
| Reverse-engineer a transform | Work backward from shown output/data structure |

## 7. Most recurring snippets

These are the patterns that show up across the largest number of exam families.

| Snippet                                    | Slug                                |   Exam families |   Questions |   Priority | Topic                         |
|:-------------------------------------------|:------------------------------------|----------------:|------------:|-----------:|:------------------------------|
| Types, None, bool, equality                | types-none-bool-equality            |               5 |          15 |          5 | Core Python                   |
| zip() and enumerate() core patterns        | zip-enumerate-core                  |               5 |          14 |          5 | Core Python                   |
| split(), join(), replace()                 | split-join-replace                  |               5 |          12 |          5 | Strings                       |
| strptime() and strftime()                  | datetime-strptime-strftime          |               5 |          12 |          5 | Datetime                      |
| Dictionary comprehension patterns          | dict-comprehension-patterns         |               5 |          10 |          5 | Dictionaries & comprehensions |
| __init__, self, defaults, attributes       | oop-init-self-defaults              |               5 |          10 |          5 | OOP                           |
| MCQ elimination checklist                  | mcq-elimination-checklist           |               5 |           8 |          5 | Exam survival                 |
| List comprehension patterns                | list-comprehension-patterns         |               5 |           7 |          5 | Dictionaries & comprehensions |
| Local vs global scope                      | local-vs-global-scope               |               5 |           7 |          5 | Functions & scope             |
| Series vs DataFrame                        | pandas-series-vs-dataframe          |               5 |           7 |          5 | Pandas                        |
| timedelta and day counts                   | datetime-timedelta-day-counts       |               5 |           7 |          5 | Datetime                      |
| *args and **kwargs                         | args-and-kwargs                     |               5 |           7 |          4 | Functions & scope             |
| Both / neither / all-of-the-above patterns | both-neither-all-meta-options       |               5 |           7 |          4 | Exam survival                 |
| Compare/report method patterns             | oop-compare-and-report-patterns     |               5 |           7 |          4 | OOP                           |
| Object state and collection attributes     | oop-state-and-collection-attributes |               5 |           7 |          4 | OOP                           |

Interpretation:

- the top of the table is the best candidate pool for a future **default preset**
- these are also the snippets that deserve the strongest visual priority in the frontend

## 8. Most recurring trap families

| Trap                        |   Exam families |   Questions | Why it recurs                                                                                             |
|:----------------------------|----------------:|------------:|:----------------------------------------------------------------------------------------------------------|
| Bool Sum Counts True        |               5 |          24 | Because booleans are integers in Python, summing booleans counts how many values are `True`.              |
| String Immutable Reassign   |               5 |          23 | String methods return a new string; the original string stays unchanged unless you reassign it.           |
| Implicit Return None        |               5 |          19 | A function without an explicit `return` returns `None`.                                                   |
| Method Returns None         |               5 |          19 | A mutating method changed the object in place, but the expression itself evaluates to `None`.             |
| Comparison Chain            |               5 |          15 | Chained comparisons like `a < b < c` are not the same as comparing booleans or tuples.                    |
| Default Arg Optional        |               5 |          15 | A parameter with a default is optional when calling the function.                                         |
| Float Int String Equality   |               5 |          15 | Python can treat some numeric types as equal (`True == 1`, `1 == 1.0`), but strings stay separate.        |
| Enumerate Gives Index Value |               5 |          14 | `enumerate(iterable)` yields `(index, value)` pairs, in that order.                                       |
| Local Scope Nameerror       |               5 |          14 | A local name is not visible outside the function where it was created.                                    |
| Zip Pairs Positionally      |               5 |          14 | `zip(a, b)` pairs items by position, not by value matching.                                               |
| Date Directive Order        |               5 |          12 | Datetime directives must match the input order exactly (`%d/%m/%Y` is not `%m/%d/%Y`).                    |
| Join Called On Separator    |               5 |          12 | `join` is called on the separator string, not on the list of pieces.                                      |
| Loc Vs Iloc                 |               5 |          12 | `loc` uses labels; `iloc` uses integer positions.                                                         |
| Strptime Vs Strftime        |               5 |          12 | `strptime` parses strings into datetime objects; `strftime` formats datetime objects into strings.        |
| Missing Self                |               5 |          11 | Instance methods need `self` as the first parameter in the method definition.                             |
| Timedelta Requires Datetime |               5 |          11 | Date arithmetic with `timedelta` works on date/datetime objects, not raw strings.                         |
| Attribute Not On Self       |               5 |          10 | Instance state should be stored on `self`, not as a bare local variable that disappears after `__init__`. |
| Dict Comp Key Value Order   |               5 |          10 | Dictionary comprehension syntax is `{key_expr: value_expr for ...}` in that order.                        |
| Return In Init              |               5 |          10 | `__init__` initializes the object and should not return a normal value.                                   |
| Args Tuple Shape            |               5 |           7 | `*args` collects extra positional arguments into a tuple.                                                 |

This is why the snippet bank is not organized as a generic “Python course summary”.
The recurring traps are much more specific than that.

## 9. Observed exam-writing habits

### Habit A — near-miss distractors

Wrong answers are rarely random nonsense.
They usually differ from the correct option by exactly one thing:

- wrong object type
- wrong method semantics
- wrong return value
- wrong argument order
- wrong index basis
- wrong expectation about mutation vs new object
- wrong expectation about `self`, scope, or pandas selection shape

### Habit B — short code, layered meaning

The code is usually short, but it compresses two or three rules together.
Example pattern:

- one rule about **what type a method returns**
- plus one rule about **whether the original object changed**
- plus one rule about **what finally gets printed**

### Habit C — same skeleton, new nouns

A question that looks new often is not new.
The exam-makers reuse skeletons like:

- count something into a dictionary
- build a dict/list comprehension with one tiny syntax trap
- parse/format a string or date
- compare a pair of objects
- select rows/columns from pandas with one indexing trap

## 10. Question-bank notes and caveats

> [!warning] Source-bank caveats
> These notes matter for analytics, but not much for snippet usefulness.

- one sample-final question is duplicated exactly (`q08` = `q11`)
- the resit pair should be treated as one family during recurrence analysis
- the sample-final and later-course trial are strongly related and should also be deduped for recurrence analysis

## 11. Bottom-line conclusions for snippet design

1. **Elimination support matters almost as much as content knowledge.**
2. **Trap metadata is not optional**; it is a core feature.
3. **Snippet bodies should mix formats**:
   - dense rule tables
   - tiny code examples
   - compact trap checklists
4. **The best default preset later should be weighted by recurrence**, not just by topic breadth.
