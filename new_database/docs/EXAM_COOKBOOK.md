# EXAM_COOKBOOK — how to write *this exact kind* of Python exam

> [!info] Final-release note
> This cookbook was built during the taxonomy pass and remained valid after the stress-test/finalization round.

> [!summary] Audience
> Imagine you are a teaching assistant who has been told:
> “Please make a final exam for Intro to Python. It should feel familiar, a little evil, but still defensible when students complain.”
>
> This document explains how to do that.

## 0. The one-sentence recipe

Build a **24-question multiple-choice exam** that is **cumulative**, leans a little toward **post-midterm** material, and repeatedly asks students to do one of four things:

1. pick the only code option that actually works  
2. predict what short code prints / returns  
3. notice why a tempting option fails  
4. recognize a recurring skeleton disguised with different nouns  

## 1. Baseline anatomy

### 1.1 Length and balance

Across the deduped exam families, the average split is:

- about **13.8 post-midterm** questions
- about **10.2 pre-midterm** questions

So the exam is not “old material plus a pandas appendix,” and it is also not “pandas/OOP/datetime only.”
It is a real cumulative paper.

### 1.2 Safe topic quotas

A very safe family-level blueprint is:

| Topic | Typical count | Safe recipe for a fresh 24-question paper | What the questions usually look like |
|:--|--:|:--|:--|
| Core Python | 4–7 | **5** | truthiness, built-ins, indexing, slicing, loops, `zip`, `enumerate` |
| Dictionaries & comprehensions | 3–6 | **4** | counting, aggregation, dict iteration, list/dict/set comprehensions |
| Functions & scope | 2–4 | **3–4** | `return`, defaults, keyword args, `*args`, `**kwargs`, local/global |
| Strings | almost always 3 | **3** | `split` / `join` / `replace`, formatting, parsing |
| Pandas | 2–5 | **3–4** | selection shape, `loc` / `iloc`, masks, transforms |
| Datetime | 2–3 | **2–3** | `strptime`, `strftime`, `timedelta`, overlap |
| OOP | 2–3 | **2–3** | `__init__`, `self`, attributes, method logic |

That recipe already lands you close to the historical papers.

### 1.3 Safe question-form quotas

If you want the exam to “feel right,” use this mix:

| Question form | Historical average (deduped families) | Safe recipe |
|:--|--:|:--|
| Choose the code that works | 10.4 | **10 or 11** |
| Predict the output | 6.0 | **5 to 7** |
| Match equivalent expressions / outputs | 2.4 | **2 or 3** |
| Choose the code that fails | 1.6 | **1 or 2** |
| Explain why a mismatch/error happens | 1.6 | **1 or 2** |
| Wildcards (`odd one out`, bad line, fill-in, etc.) | low | **0 to 2 total** |

## 2. The exam-makers’ operating philosophy

> [!tip] Core principle
> The exam is not mainly testing whether students can write long programs from scratch.
> It is testing whether they can **read short code precisely**.

That means your questions should usually be:

- short enough to fit on paper comfortably
- precise enough that one option is defensibly correct
- tricky enough that shallow familiarity is not enough

The best questions are often built from **two small rules**, not one giant rule.

### Good layering

A good item often combines:

- method semantics + mutation vs return
- parameter binding + default values
- `loc` / `iloc` + custom index labels
- string parsing + slicing
- `strptime` directives + date arithmetic
- `self` + where state is stored
- dict iteration + key/value confusion

### Bad layering

Avoid items that need five simultaneous leaps.
If students need to decode twenty lines of code before they even reach the trick, the paper stops feeling like the historical exams.

## 3. The recurring skeletons you should reuse

### 3.1 “Which line works?”

This is the signature form.

To write one:

1. pick one tiny task
2. write one correct option
3. write three distractors that each violate a **different** rule

Examples of task types:

- make a dictionary with the right keys and values
- select the even rows
- format a phone number
- construct an object with defaults
- call a function using keyword arguments
- parse a date string
- add a calculated pandas column

The distractors should be “almost right”:

- wrong argument order
- wrong bracket type
- wrong object used to call the method
- wrong return-value assumption
- wrong choice between label-based and position-based indexing

### 3.2 “What does this print?”

Use this when you want students to simulate execution.

Keep the code short and make the key cognitive move one of these:

- track a variable through a loop
- understand `return None`
- understand local scope
- follow a list/dict comprehension
- interpret `zip` / `enumerate`
- see whether an object changed in place
- understand how a method formats or parses

### 3.3 “Which options are correct: both / neither / all?”

Use sparingly, but use them.
They reward disciplined evaluation and punish students who commit to the first plausible option too early.

The trick is not to invent new Python here.
The trick is simply to take two normal mini-claims and wrap them in a meta-option frame.

### 3.4 “Which could have created this output?”

These questions are especially good for pandas and comprehensions.

Show the student:

- a final DataFrame / Series
- a printed dictionary
- a sorted/aggregated structure

Then ask which line **could** or **could not** have produced it.

This forces them to reason backward from:

- shape
- labels
- ordering
- type
- column names
- value transformations

## 4. Topic-by-topic construction guide

## 4.1 Core Python

This is the quiet backbone of the exam.

You almost always want some mix of:

- truthiness / equality
- built-in return types
- indexing / negative indexing
- slicing
- loops
- `zip`
- `enumerate`

### Reliable traps

| Trap family | How to deploy it |
|:--|:--|
| `True == 1` style equality | Put booleans, ints, floats, and strings in the same options |
| slice stop exclusivity | Make one distractor off by exactly one element |
| negative indices | Hide the correct answer behind `-1`, `-2`, etc. |
| `range` stop exclusivity | Use a loop where the student must notice the last value is omitted |
| `enumerate` output shape | Swap `(index, value)` into `(value, index)` in one distractor |
| `zip` pairing | Make one option behave as if `zip` matched by meaning rather than position |
| `max` on lists | Tempt students into numeric-sum thinking when Python uses lexicographic comparison |

### Minimum recipe

Include at least:

- one indexing/slicing question
- one loop template / output question
- one `zip` or `enumerate` question
- one truthiness / built-in return question

## 4.2 Functions & scope

This section is about the tiny ways function calls go wrong.

### Reliable traps

| Trap family | Deployment |
|:--|:--|
| implicit `None` | Put `print(f(...))` after a function without an explicit `return` |
| local vs global | Define a variable inside the function, then access it outside |
| assignment makes local | Reuse a global-looking name inside a function body |
| keyword binding | Write one call that is valid but looks “out of order” |
| defaults | Include one optional argument and one distractor that treats it as required |
| `*args` / `**kwargs` | Offer options that misunderstand the collected object type |

### Minimum recipe

Include:

- one scope question
- one defaults / keyword-argument question
- one `*args` / `**kwargs` or lambda/higher-order question

## 4.3 Strings

String questions are compact, which makes them perfect MCQ material.

### Reliable traps

| Trap family | Deployment |
|:--|:--|
| immutability | Call a string method without reassigning |
| `join` ownership | Write `parts.join("-")` in a distractor instead of `"-".join(parts)` |
| `replace` signature | Swap old/new/count order |
| `find` vs `index` | Hide the missing-item behavior difference |
| formatting | Use wrong placeholder names or wrong expression placement |
| parsing | Make the student isolate the host/domain/extension in the right order |

### Minimum recipe

Include:

- one `split` / `join` / `replace` question
- one formatting question
- one parsing/editing question

## 4.4 Dictionaries & comprehensions

This family is a favorite because it creates excellent “looks right at a glance” distractors.

### Reliable traps

| Trap family | Deployment |
|:--|:--|
| dict iteration yields keys | Loop over `d` and tempt students to think they got key-value pairs |
| key/value swap in dict comp | Flip `{key: value}` into `{value: key}` in a distractor |
| counting pattern | Overwrite instead of increment |
| comprehension `if` placement | Confuse filter-only `if` with inline `x if cond else y` |
| set/list/dict confusion | Offer a comprehension with the wrong bracket type |

### Minimum recipe

Include:

- one build/count/aggregate dictionary question
- one list or dict comprehension question
- one dict iteration/equality or “next-link” style mapping question

## 4.5 OOP

These questions are compact and tend to punish fuzzy mental models of `self`.

### Reliable traps

| Trap family | Deployment |
|:--|:--|
| missing `self` | Remove it from the method signature |
| passing `self` twice | Call `obj.method(obj, x)` in a distractor |
| attribute stored as local | Set `name = ...` instead of `self.name = ...` |
| illegal `return` in `__init__` | Return a normal value from the constructor |
| state not stored on instance | Use a value later without saving it on `self` |

### Minimum recipe

Include:

- one `__init__` / defaults / attributes question
- one method/state/output question

## 4.6 Datetime

Datetime questions are loved because the rules are precise and the distractors are clean.

### Reliable traps

| Trap family | Deployment |
|:--|:--|
| `strptime` vs `strftime` | Ask a parse question and include formatting code as a distractor |
| directive order | Swap day and month directives |
| raw string vs datetime object | Try to add a `timedelta` to a string in a distractor |
| overlap logic | Write one option that checks non-overlap incorrectly |
| constructor order | Mix up year/month/day order when building a datetime |

### Minimum recipe

Include:

- one parse/format question
- one date arithmetic or overlap question

## 4.7 Pandas

This is where post-midterm flavor really shows.

### Reliable traps

| Trap family | Deployment |
|:--|:--|
| `loc` vs `iloc` | Use a custom index so labels are not positions |
| Series vs DataFrame | Use single vs double brackets |
| boolean mask parentheses | Remove the parentheses in one option |
| `map` vs `apply` | Use `map` where row-wise logic is needed |
| vectorized vs element-wise | Write a distractor that overcomplicates a simple vectorized operation |
| `sort_index` vs `sort_values` | Ask for row order by data, then include label-sort distractors |

### Minimum recipe

Include:

- one selection question
- one transform/new-column question
- optionally one construction/sorting question if you want the paper to lean more post-midterm

## 5. The trap library: how to be mean efficiently

> [!warning] The best distractor is one that is wrong for a *single crisp reason*.

Use this principle:

- the correct answer should feel precise in hindsight
- each wrong answer should be explainable in one sentence

### High-yield trap families

1. **mutation vs return value**  
   Great for strings, lists, and pandas.

2. **object type mismatch**  
   Student thinks they still have a string; actually they now have a list.  
   Student thinks they have a DataFrame; actually they selected a Series.

3. **position vs label**  
   Perfect for slicing, indexing, pandas, and `zip`/`enumerate`.

4. **scope / lifetime**  
   The variable existed, but not *here*.

5. **constructor / instance-state mistakes**  
   Great OOP trap family because one missing `self.` breaks the whole idea.

6. **parse vs format confusion**  
   Datetime and string formatting both love this.

7. **key vs value confusion**  
   Extremely reusable in dictionaries and pandas mapping questions.

## 6. How to vary difficulty without changing the syllabus

### Make a question easier by:

- testing only one rule
- using obvious variable names
- avoiding meta-options
- printing the intermediate value

### Make a question harder by:

- combining two small rules
- choosing slightly misleading variable names
- asking for the one option that **does not** work
- wrapping two claims inside a “both / neither” frame
- showing output and asking students to work backward

### Make a question unfair by:

- relying on hidden assumptions not taught elsewhere
- making multiple options arguably correct
- stuffing too many lines of irrelevant code around the real trick

Do the first two. Avoid the third.

## 7. A full 24-question blueprint you can reuse

Here is a conservative but historically faithful build:

| Slot block | Count | Suggested content |
|:--|--:|:--|
| Opening warm-up | 3 | one core Python truthiness/indexing item, one string-method item, one dict/comprehension item |
| Early middle | 5 | functions/scope, loops, `zip`/`enumerate`, a second dict/comprehension, one OOP constructor trap |
| Middle | 6 | pandas selection, pandas transform, datetime parse/format, datetime arithmetic, output prediction, both/neither meta-item |
| Late middle | 5 | core slicing/loop simulation, string formatting/parsing, function binding, OOP state question, dict iteration |
| Closing | 5 | one harder pandas/datetime item, one reverse-logic item, one choose-the-bad-line item, and two high-confidence standard skeletons |

That blueprint keeps the paper feeling varied without feeling random.

## 8. Checklist for writing each individual item

Before you keep a question, ask:

- Is one option clearly correct?
- Is each wrong option wrong for a specific reason?
- Does the question test a rule that actually recurs in the course?
- Is the code short enough that the trick is the **Python**, not the reading load?
- Can I explain the intended trap in one sentence?

If the answer to the last question is “not really,” the item is probably muddy rather than clever.

## 9. How to annoy students without causing a rebellion

> [!quote] Officially
> The exam should test understanding.

> [!quote] Unofficially
> The exam should also reward students who learned the exact failure modes that keep showing up.

The sweet spot is:

- familiar skeleton
- unfamiliar surface story
- one precise trap
- one precise correct answer

That is the house style.

## Appendix A — family-level topic counts

| Exam family                              |   Core Python |   Datetime |   Dictionaries & comprehensions |   Functions & scope |   OOP |   Pandas |   Strings |
|:-----------------------------------------|--------------:|-----------:|--------------------------------:|--------------------:|------:|---------:|----------:|
| 2022 final                               |             4 |          2 |                               5 |                   4 |     2 |        4 |         3 |
| 2023 resit family                        |             3 |          2 |                               4 |                   4 |     3 |        5 |         3 |
| 2023 trial                               |             6 |          3 |                               3 |                   3 |     3 |        3 |         3 |
| 2024 trial                               |             7 |          3 |                               3 |                   2 |     3 |        3 |         3 |
| 2025 sample-family / later-course family |             4 |          3 |                               6 |                   4 |     2 |        2 |         3 |

## Appendix B — family-level question-form counts

| Exam family                              |   Choose the code that fails |   Choose the code that works |   Match equivalent expressions / outputs |   Explain why a mismatch/error happens |   Fill a template / blank |   Identify the bad line |   Find the odd one out |   Predict the output |   Reverse-engineer a transform |   Select the true statement |
|:-----------------------------------------|-----------------------------:|-----------------------------:|-----------------------------------------:|---------------------------------------:|--------------------------:|------------------------:|-----------------------:|---------------------:|-------------------------------:|----------------------------:|
| 2022 final                               |                            3 |                           10 |                                        1 |                                      2 |                         0 |                       0 |                      1 |                    5 |                              1 |                           1 |
| 2023 resit family                        |                            2 |                           10 |                                        4 |                                      2 |                         0 |                       0 |                      0 |                    6 |                              0 |                           0 |
| 2023 trial                               |                            0 |                           11 |                                        4 |                                      1 |                         1 |                       1 |                      1 |                    5 |                              0 |                           0 |
| 2024 trial                               |                            0 |                            9 |                                        3 |                                      2 |                         1 |                       1 |                      1 |                    7 |                              0 |                           0 |
| 2025 sample-family / later-course family |                            3 |                           12 |                                        0 |                                      1 |                         0 |                       0 |                      1 |                    7 |                              0 |                           0 |

## Appendix C — recurring trap shortlist

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
