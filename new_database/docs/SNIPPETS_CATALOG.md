# Snippets catalog

> [!summary] What this is
> Human-readable final copy of the snippet bank.
> Each snippet is shown with its metadata and all of its pieces.

## Topic index

- **Exam survival** (`survival`) — 2 snippets
- **Core Python** (`core-python`) — 8 snippets
- **Functions & scope** (`functions-and-scope`) — 6 snippets
- **Strings** (`strings`) — 6 snippets
- **Dictionaries & comprehensions** (`dicts-and-comprehensions`) — 6 snippets
- **OOP** (`oop`) — 4 snippets
- **Datetime** (`datetime`) — 5 snippets
- **Pandas** (`pandas`) — 8 snippets

# Exam survival

> [!info] Topic note
> Cross-topic elimination tactics and the most repeated trick families.
> Snippets in this topic: **2**

## Answering strategy

> [!tip] Subtopic note
> Fast elimination and wording-decoder pieces.
> Snippets in this subtopic: **1**

### Start here

#### MCQ elimination checklist

> [!abstract] Snippet metadata
> - Slug: `mcq-elimination-checklist`
> - Phase: `mixed`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `8` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/4`
> - Estimated space: `1552` chars selected / `2023` chars total
> - Keywords: `does not work`, `elimination`, `mcq`, `strategy`, `traps`, `works`
> - Trap slugs: `loc_vs_iloc`, `local_scope_nameerror`, `method_returns_none`, `string_immutable_reassign`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q03`, `final-exam-solutions-for-python-programming-62oop21-q07`, `final-exam-study-guide-trial-python-basics-2023-q19`, `introduction-to-python-trial-final-exam-solutions-py22-q14`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q18`, `sample-final-plus-answers-q04`, `sample-final-plus-answers-q06`, `sample-final-plus-answers-q15`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> The bank repeatedly rewards fast shape-checking: type, mutation, labels vs positions, parse vs format, and whether code actually returns/prints what the stem asks.

**Summary.** A cross-topic decision tree for eliminating bad options before you fully solve the question.

##### Piece 1 — 10-second elimination flow

_kind:_ `checklist` · _role:_ `core` · _default selected:_ `yes`

1. **What object type is this?** String, list, dict, Series, DataFrame, datetime, object?
2. **Mutates or returns a new value?** `"book-book".replace("book", "novel", 1)` returns a **new string**; `items.append(x)` mutates the list and returns `None`.
3. **Labels or positions?** Pandas: `df.loc[2, 'B']` uses labels; `df.iloc[1, 1]` uses integer positions.
4. **Value shape?** `df['B']` -> Series, `df[['B']]` -> DataFrame.
5. **Method or free function?** `"Amsterdam".count('a')`, not `count("Amsterdam", 'a')`.
6. **Did they reassign?** If not, immutable objects such as strings stay unchanged.
7. **Scope okay?** A name created inside a function cannot be used outside it.
8. **Parse or format?** `datetime.strptime("03-02-2013", "%d-%m-%Y")` reads a string; `dt.strftime("%d-%m-%Y")` writes a string.
9. **Stop exclusive?** `x[1:4]` uses indices `1,2,3`; the stop index is excluded.
10. **Could the answer simply be an error?** Many distractors fail before any deeper logic matters.

##### Piece 2 — Question wording decoder

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Wording in stem | What you should do |
|---|---|
| “works / achieves what you want” | keep only syntactically valid options that exactly match required output/type |
| “does **not** work / could **not** have created” | look for one fatal mismatch; do not overthink the others |
| “same output” / “different datatype” | compare shape first, not just values |
| “What prints?” / “What returns?” | mentally execute; watch `None`, rounding, integer vs float |
| “Why error?” | find first invalid assumption: scope, wrong method call, bad indexing, wrong object type |

##### Piece 3 — Tiny exam-style sanity checks

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
s = "020-525"
s.replace("-", "")        # returns '020525'
s                         # still '020-525' unless reassigned

df["B"]                   # Series
df[["B"]]                 # DataFrame

for key, value in d:      # error: iterating a dict yields keys, not (key, value) pairs
    ...
```

##### Piece 4 — Scope sanity check

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
def build_total(x, y):
    total = x + y
    return total

build_total(2, 3)   # 5
total               # NameError: total only exists inside build_total
```

---

## Cross-topic traps

> [!tip] Subtopic note
> Trap families that recur across multiple topic areas.
> Snippets in this subtopic: **1**

### Start here

#### Mutation vs return value

> [!abstract] Snippet metadata
> - Slug: `mutation-vs-return`
> - Phase: `mixed`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `6` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `905` chars selected / `1233` chars total
> - Keywords: `append`, `immutable`, `mutation`, `replace`, `returns none`, `shuffle`, `sort`
> - Trap slugs: `method_returns_none`, `shuffle_sort_in_place`, `string_immutable_reassign`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q04`, `final-exam-solutions-for-python-programming-62oop21-q19`, `final-exam-study-guide-trial-python-basics-2023-q17`, `introduction-to-python-trial-final-exam-solutions-py22-q17`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q21`, `sample-final-plus-answers-q04`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> A large share of wrong options fail because the code forgets that strings are immutable, that `append`/`sort`/`shuffle` mutate in place, or that some expressions return `None`.

**Summary.** A single place to remember which operations change an object, which return a new value, and which return `None`.

##### Piece 1 — Mutate / return / object after call

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Expression | Returns | Original object changed? | Exam trap |
|---|---|---:|---|
| `s.replace(old, new)` | new string | No | reassign or lose change |
| `s.split(sep)` | list | No | returns list, not string |
| `sep.join(parts)` | string | No | `join` is called on separator |
| `lst.append(x)` | `None` | Yes | `return lst.append(x)` returns `None` |
| `lst.sort()` | `None` | Yes | use `sorted(lst)` when you need a value |
| `random.shuffle(lst)` | `None` | Yes | shuffles list in place |
| `df.sort_values(...)` | new DataFrame | No | reassign if you want sorted result stored |

##### Piece 2 — Minimal reminders

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
# strings: immutable
s = "book-book"
s.replace("book", "novel", 1)
print(s)                     # 'book-book'

# lists: append mutates, returns None
y = []
result = y.append(3)
print(y, result)            # [3] None

# shuffle: in place
words = "hello there you".split()
random.shuffle(words)       # words changed
```

##### Piece 3 — Fast trap signals

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

- If the method is attached to a **string**, assume it returns a **new string**.
- If the method name sounds like “change order / add item” on a **list**, assume it mutates and often returns `None`.
- If the stem wants a **printed final value**, check whether the code stored the returned object or silently discarded it.

---

# Core Python

> [!info] Topic note
> Types, truthiness, indexing, slicing, loops, and small built-ins.
> Snippets in this topic: **8**

## Types & conditions

> [!tip] Subtopic note
> Truthiness, equality, membership, and built-ins.
> Snippets in this subtopic: **3**

### Start here

#### Types, None, bool, equality

> [!abstract] Snippet metadata
> - Slug: `types-none-bool-equality`
> - Phase: `pre-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `15` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `637` chars selected / `816` chars total
> - Keywords: `None`, `bool`, `comparison`, `equality`, `truthiness`, `type`
> - Trap slugs: `bool_sum_counts_true`, `comparison_chain`, `float_int_string_equality`, `implicit_return_none`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q10`, `final-exam-solutions-for-python-programming-62oop21-q13`, `final-exam-solutions-for-python-programming-62oop21-q18`, `final-exam-study-guide-trial-python-basics-2023-q03`, `introduction-to-python-trial-final-exam-solutions-py22-q01`, `introduction-to-python-trial-final-exam-solutions-py22-q03`, `introduction-to-python-trial-final-exam-solutions-py22-q24`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q01`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q03`, `resit-solutions-for-introduction-to-python-35761538-q01`, `resit-solutions-for-introduction-to-python-35761538-q03`, `sample-final-plus-answers-q13`, `sample-final-plus-answers-q17`, `trial-final-exam-solutions-introduction-to-python-3077951-q13`, `trial-final-exam-solutions-introduction-to-python-3077951-q17`
> - Presets: `balanced-default`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> Basic-looking MCQs often hide one decisive fact: `'3' != 3`, `3 == 3.0`, empty containers are falsey, and reaching the end of a function returns `None`.

**Summary.** Core Python value semantics: types, `None`, truth values, and equality between strings, ints, floats, and booleans.

##### Piece 1 — Equality / truthiness mini-table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Expression | Result | Why |
|---|---:|---|
| `'3' == 3` | `False` | string vs int |
| `3 == 3.0` | `True` | numeric equality |
| `'3' == 3.0` | `False` | string vs float |
| `[]`, `{}`, `''` in `if` | falsey | empty container/string |
| non-empty list/dict/string | truthy | contains something |
| `True == 1` | `True` | booleans are numeric subclasses |
| `False == 0` | `True` | same idea |

##### Piece 2 — Chains and booleans

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

- `a == b == c` means `(a == b) and (b == c)`.
- `sum([cond1, cond2, ...])` counts how many conditions are `True`.
- If a function hits the end without `return`, it returns `None`.
- `type(x)` gives the class object, e.g. `int`, `str`, `dict`.

##### Piece 3 — Micro examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
x, y, z = '3', 3, 3.0
print(x == y)        # False
print(y == z)        # True
print(x == y == z)   # False

print(bool([]))      # False
print(bool([1]))     # True
```

---

#### Built-ins and what they return

> [!abstract] Snippet metadata
> - Slug: `builtins-return-values`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `very-common` across `4` families / `11` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/4`
> - Estimated space: `804` chars selected / `1071` chars total
> - Keywords: `count`, `index`, `len`, `max`, `ord`, `sorted`, `sum`, `type`
> - Trap slugs: `builtin_return_type`, `sort_vs_sorted`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q24`, `final-exam-study-guide-trial-python-basics-2023-q03`, `final-exam-study-guide-trial-python-basics-2023-q04`, `final-exam-study-guide-trial-python-basics-2023-q11`, `introduction-to-python-trial-final-exam-solutions-py22-q03`, `introduction-to-python-trial-final-exam-solutions-py22-q06`, `introduction-to-python-trial-final-exam-solutions-py22-q11`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q05`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q11`, `resit-solutions-for-introduction-to-python-35761538-q05`, `resit-solutions-for-introduction-to-python-35761538-q11`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`

> [!summary] Why it matters
> A surprising number of MCQs are really about remembering one built-in exactly: `len`, `sorted`, `sum`, `max`, `ord`, `type`, `count`, `index`.

**Summary.** High-yield built-ins that recur in output questions: what they take, what they return, and their usual type.

##### Piece 1 — Built-ins at a glance

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Call | Output | Return type / note |
|---|---|---|
| `len([1,2,3])` | `3` | `int` |
| `sorted([3,1,2])` | `[1,2,3]` | new list |
| `sum([4,5])` | `9` | number |
| `max([4,5])` | `5` | largest element |
| `round(11/3, 1)` | `3.7` | rounded number |
| `ord('a')` | `97` | Unicode code point |
| `type({})` | `<class 'dict'>` | class object, not `'dict'` |
| `'abc'.index('b')` | `1` | position or `ValueError` |
| `'Amsterdam'.count('a')` | `1` | occurrence count |

##### Piece 2 — Exam-style comparisons

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
x = [0,1,2,3,4,5,6,7,8,9]
len(x)                    # 10
sorted(x, reverse=True)[0]# 9
x.index(9)                # 9
sum(x[4:6])               # 9
```

##### Piece 3 — Common confusion

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

- `sorted(x)` returns a value; `x.sort()` mutates the list and returns `None`.
- `type(3)` is a class object: `type(3) == int` is `True`, but `type(3) == 'int'` is `False`.
- `round(x, n)` returns a rounded number; it does not mutate anything.
- Use method-call shapes that actually run: `'Amsterdam'.count('a')`, `'Amsterdam'.index('d')`.

##### Piece 4 — type() micro-example

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
type(3)              # <class 'int'>
type(3) == int       # True
type(3) == 'int'     # False
```

---

### Add next

#### Membership and condition logic

> [!abstract] Snippet metadata
> - Slug: `membership-and-condition-logic`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `common` across `3` families / `5` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/4`
> - Estimated space: `632` chars selected / `1131` chars total
> - Keywords: `and`, `conditions`, `in`, `membership`, `not in`, `or`
> - Trap slugs: `condition_precedence_brackets`, `membership_checks_keys`
> - Question refs: `final-exam-study-guide-trial-python-basics-2023-q01`, `introduction-to-python-trial-final-exam-solutions-py22-q01`, `introduction-to-python-trial-final-exam-solutions-py22-q10`, `sample-final-plus-answers-q17`, `trial-final-exam-solutions-introduction-to-python-3077951-q17`
> - Presets: `balanced-default`, `trap-hunter`

> [!summary] Why it matters
> Several questions are solved by recognizing that membership is checked against the right object, and that condition precedence can make a nearly-correct answer wrong.

**Summary.** How `in`, `not in`, `and`, `or`, and `not` are used in the bank’s condition questions.

##### Piece 1 — Membership semantics

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Container | `x in container` checks |
|---|---|
| list / tuple | elements |
| set | elements |
| string | substring / character |
| dict | **keys**, not values |

##### Piece 2 — Condition patterns worth memorizing

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

- If the question is only checking whether one value belongs to a known collection, look for a direct membership test such as `item in allowed_values`.
- Odd/even questions usually reduce to `x % 2 == 0` (even) or `x % 2 != 0` (odd).
- When a condition mixes `and` and `or`, mentally evaluate the smaller comparisons first; many wrong options change the grouping.
- For dictionaries, `x in d` checks **keys**; use `x in d.values()` only when the stem asks about values.

##### Piece 3 — Tiny examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
x = 7
x % 2 != 0          # True  -> odd

grades = {"Alice": 8, "Bob": 7}
"Alice" in grades           # True  (key check)
8 in grades                 # False (still checking keys)
8 in grades.values()        # True  (value check)
```

##### Piece 4 — Membership with real context

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
allowed_countries = {"Belgium", "France", "Germany"}
destination = "France"

destination in allowed_countries     # True
destination in {"Spain", "Italy"}    # False
```
This is the pattern behind many “is this value allowed / included?” answers.

---

## Lists, slicing & loops

> [!tip] Subtopic note
> Indexing, slicing, iteration templates, zip/enumerate.
> Snippets in this subtopic: **5**

### Start here

#### zip() and enumerate() core patterns

> [!abstract] Snippet metadata
> - Slug: `zip-enumerate-core`
> - Phase: `pre-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `14` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `418` chars selected / `807` chars total
> - Keywords: `enumerate`, `index value`, `pairing`, `zip`
> - Trap slugs: `enumerate_gives_index_value`, `zip_pairs_positionally`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q16`, `final-exam-solutions-for-python-programming-62oop21-q23`, `final-exam-study-guide-trial-python-basics-2023-q05`, `final-exam-study-guide-trial-python-basics-2023-q08`, `introduction-to-python-trial-final-exam-solutions-py22-q04`, `introduction-to-python-trial-final-exam-solutions-py22-q05`, `introduction-to-python-trial-final-exam-solutions-py22-q08`, `introduction-to-python-trial-final-exam-solutions-py22-q10`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q11`, `resit-solutions-for-introduction-to-python-35761538-q11`, `sample-final-plus-answers-q03`, `sample-final-plus-answers-q20`, `trial-final-exam-solutions-introduction-to-python-3077951-q03`, `trial-final-exam-solutions-introduction-to-python-3077951-q20`
> - Presets: `balanced-default`, `ultra-dense-core`

> [!summary] Why it matters
> These two functions recur in list, dict, and output questions. Students often mix up index/value order or forget that `enumerate(..., start=1)` shifts numbering.

**Summary.** The exact shapes of `zip()` and `enumerate()` and how they are used to build dictionaries and paired outputs.

##### Piece 1 — What they produce

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Expression | Items produced |
|---|---|
| `zip(a, b)` | `(a0, b0), (a1, b1), ...` |
| `enumerate(x)` | `(0, x0), (1, x1), ...` |
| `enumerate(x, 1)` | `(1, x0), (2, x1), ...` |

##### Piece 2 — Useful templates

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
# dict from two lists
d = {name: age for name, age in zip(names, ages)}

# count from 1
for i, value in enumerate(items, start=1):
    print(i, value)

# next-link dict
d = {left: right for left, right in zip(l1[:-1], l1[1:])}
```

##### Piece 3 — Exam-style micro examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
[item[0] * item[1] for item in zip(list1, list2)]
# ['a', 'bb', 'ccc']
```

```python
player1 = [1, 0, 2]
player2 = [0, 1, 1]
player3 = [2, 2, 0]
match_goals = {}

for i, (g1, g2, g3) in enumerate(zip(player1, player2, player3), start=1):
    match_goals[i] = (g1, g2, g3)

# match_goals == {1: (1, 0, 2), 2: (0, 1, 2), 3: (2, 1, 0)}
```

---

#### Slicing patterns

> [!abstract] Snippet metadata
> - Slug: `slicing-patterns`
> - Phase: `pre-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `very-common` across `4` families / `9` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `406` chars selected / `699` chars total
> - Keywords: `chunking`, `every third`, `reverse`, `slice`, `start stop step`
> - Trap slugs: `negative_step_direction`, `slice_stop_exclusive`
> - Question refs: `final-exam-study-guide-trial-python-basics-2023-q09`, `final-exam-study-guide-trial-python-basics-2023-q11`, `introduction-to-python-trial-final-exam-solutions-py22-q09`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q05`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q12`, `resit-solutions-for-introduction-to-python-35761538-q05`, `resit-solutions-for-introduction-to-python-35761538-q12`, `sample-final-plus-answers-q18`, `trial-final-exam-solutions-introduction-to-python-3077951-q18`
> - Presets: `balanced-default`, `ultra-dense-core`

> [!summary] Why it matters
> Slice blanks and list-construction questions are common, and the distractors usually differ by one subtle issue: start, stop, step, or stop-exclusivity.

**Summary.** How to read and write slices, especially when the exam asks for every nth element or reverse-order patterns.

##### Piece 1 — Slice syntax table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Form | Meaning |
|---|---|
| `x[a:b]` | start at `a`, stop **before** `b` |
| `x[a:b:c]` | same, but jump by `c` each time |
| `x[::-1]` | reversed copy |
| `x[-1::-2]` | start at last item, move left by 2 |
| `x[1:len(x):3]` | indices `1, 4, 7, ...` |

##### Piece 2 — Typical exam patterns

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
mylist = [10, 15, 20, 25, 30, 35, 40, 45]
mylist[1:len(mylist):3]      # [15, 30, 45]

numbers = [1,2,3,4,5,6,7,8,9,10]
numbers[-1::-2]              # [10, 8, 6, 4, 2]
numbers[::-1][::2]           # [10, 8, 6, 4, 2]
numbers[::-2][::-1]          # [2, 4, 6, 8, 10]  # not the same
```

##### Piece 3 — Chunking pattern

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
x = ['a','b','c','d','e','f','g','h','i']
chunks = [x[i:i+3] for i in range(0, len(x), 3)]
# [['a','b','c'], ['d','e','f'], ['g','h','i']]
```

---

#### List selection and aggregation

> [!abstract] Snippet metadata
> - Slug: `list-selection-and-aggregation`
> - Phase: `pre-midterm`
> - Default priority: `3`
> - Difficulty: `mixed`
> - Recurrence: `very-common` across `4` families / `6` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `354` chars selected / `510` chars total
> - Keywords: `equal to index`, `filter`, `max`, `sublist`, `sum`
> - Trap slugs: `append_index_vs_value`, `lexicographic_vs_sum`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q23`, `final-exam-solutions-for-python-programming-62oop21-q24`, `final-exam-study-guide-trial-python-basics-2023-q08`, `introduction-to-python-trial-final-exam-solutions-py22-q08`, `sample-final-plus-answers-q18`, `trial-final-exam-solutions-introduction-to-python-3077951-q18`
> - Presets: _none_

> [!summary] Why it matters
> The bank includes questions where the real task is not syntax but choosing the right selection criterion: equal to index, largest sum, or another derived property.

**Summary.** Patterns for filtering lists, keeping elements that meet an index-based rule, or selecting one sub-list by a derived statistic.

##### Piece 1 — Keep elements equal to their index

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
# x has unique integers
y = [value for i, value in enumerate(x) if i == value]
```

Equivalent loop:
```python
y = []
for i, value in enumerate(x):
    if i == value:
        y.append(value)
```

##### Piece 2 — Pick the sub-list with the highest sum

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
sums = [sum(sub) for sub in x]
y = x[sums.index(max(sums))]
```

Do **not** use `max(x)` unless the question wants lexicographic list order.

##### Piece 3 — Max-sum trap

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `no`

`max([[8,20,300],[40,5,6]])` compares lists lexicographically, not by the sum of their elements.  
If the criterion is **sum**, compute the sums explicitly.

---

### Add next

#### Loop templates

> [!abstract] Snippet metadata
> - Slug: `loop-templates`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `common` across `3` families / `5` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/3`
> - Estimated space: `333` chars selected / `462` chars total
> - Keywords: `for`, `inclusive`, `previous`, `range`, `while`
> - Trap slugs: `range_stop_exclusive`, `while_condition_off_by_one`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q14`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q04`, `resit-solutions-for-introduction-to-python-35761538-q04`, `sample-final-plus-answers-q14`, `trial-final-exam-solutions-introduction-to-python-3077951-q14`
> - Presets: `balanced-default`

> [!summary] Why it matters
> The loop questions are rarely deep; they reward knowing a few exact templates and noticing inclusive vs exclusive bounds.

**Summary.** Minimal patterns for range-based loops, while-loops, and loops with a carry variable such as `previous`.

##### Piece 1 — Core templates

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
# inclusive 1..10
for i in range(1, 11):
    ...

# inclusive 0..20 with while
i = 0
while i <= 20:
    ...
    i += 1
```

##### Piece 2 — Carry the previous value

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
previous = 0
for i in range(1, 11):
    print(i + previous)
    previous = i
```
Prints:
```python
1, 3, 5, ..., 19
```

##### Piece 3 — Trap checklist

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

- `range(0, 20)` stops at `19`, not `20`.
- A `while` loop often needs the increment **inside** the loop.
- If the stem says “only the even numbers”, reject code that also prints `None` or odd numbers.

---

#### Nested indexing and negative indices

> [!abstract] Snippet metadata
> - Slug: `nested-indexing-and-negative-indices`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `occasional` across `2` families / `3` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/3`
> - Estimated space: `328` chars selected / `514` chars total
> - Keywords: `indexing`, `negative index`, `nested lists`, `tuples`
> - Trap slugs: `negative_indices`, `nested_index_order`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q13`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q01`, `resit-solutions-for-introduction-to-python-35761538-q01`
> - Presets: `balanced-default`

> [!summary] Why it matters
> Several “easy” questions are solved by correctly evaluating expressions like `x[0][1]`, `x[-3][0]`, or by knowing exactly what `-1` and `-2` mean.

**Summary.** Read nested sequences quickly and avoid off-by-one errors with negative indices.

##### Piece 1 — Index rules

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Pattern | Meaning |
|---|---|
| `x[0]` | first element |
| `x[-1]` | last element |
| `x[-2]` | second-last element |
| `x[i][j]` | first get outer element `i`, then inner element `j` |

##### Piece 2 — Exam-style example

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
x = [(1, 2), (3, 4), (5, 6), (7, 8)]

x[0][1]    # 2
x[-3][0]   # 3
x[-1][1]   # 8
x[-4][1]   # 2
```
Then:
```python
(x[0][1] * x[-3][0]) == (x[-1][1] - x[-4][1])   # True
```

##### Piece 3 — Fast check

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

Read from left to right: outer index first, inner index second.  
For negative indices, count from the end: `-1` last, `-2` second-last, etc.

---

# Functions & scope

> [!info] Topic note
> Returns, parameters, scope, imports, and higher-order call patterns.
> Snippets in this topic: **6**

## Returns & scope

> [!tip] Subtopic note
> Implicit None, local/global rules, and variable lifetime.
> Snippets in this subtopic: **2**

### Start here

#### Local vs global scope

> [!abstract] Snippet metadata
> - Slug: `local-vs-global-scope`
> - Phase: `pre-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `533` chars selected / `744` chars total
> - Keywords: `NameError`, `UnboundLocalError`, `global`, `local`, `scope`, `shadowing`
> - Trap slugs: `assignment_makes_local`, `local_scope_nameerror`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q15`, `final-exam-study-guide-trial-python-basics-2023-q02`, `introduction-to-python-trial-final-exam-solutions-py22-q02`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q02`, `resit-solutions-for-introduction-to-python-35761538-q02`, `sample-final-plus-answers-q15`, `trial-final-exam-solutions-introduction-to-python-3077951-q15`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> Scope questions recur in almost every exam family: a local variable is used outside its function, or assignment inside a function makes Python treat the name as local.

**Summary.** How names live inside and outside functions, plus the classic shadowing and NameError traps.

##### Piece 1 — Scope rules

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Situation | Result |
|---|---|
| Name created inside function | local to that function |
| Name created outside function | global/module-level |
| Read global inside function, no assignment | allowed |
| Assign to a name inside function | Python treats that name as local unless `global` is used |
| Use local name outside function | `NameError` |

##### Piece 2 — Classic traps

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
def power(num, factor):
    result = num ** factor
    return result

print(result)   # NameError: result was local to power
```

```python
a = 10
def f():
    a = a + 1   # local-shadowing problem
```

##### Piece 3 — Fast elimination hint

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

If the answer choices talk about invalid operators or bad formatting, but the code also references a variable **outside its scope**, the scope issue is usually the first fatal problem.

---

#### return, None, and function end

> [!abstract] Snippet metadata
> - Slug: `return-none-and-function-end`
> - Phase: `pre-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `common` across `3` families / `6` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `337` chars selected / `570` chars total
> - Keywords: `None`, `append`, `function end`, `return`
> - Trap slugs: `implicit_return_none`, `method_returns_none`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q21`, `final-exam-study-guide-trial-python-basics-2023-q10`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q02`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q03`, `resit-solutions-for-introduction-to-python-35761538-q02`, `resit-solutions-for-introduction-to-python-35761538-q03`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> Questions on missing `return` and accidental `None` are everywhere, especially in function-definition items.

**Summary.** Remember what `return` does, what happens without `return`, and why `return some_mutating_method(...)` is often wrong.

##### Piece 1 — Three rules

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

- `return value` immediately ends the function and sends `value` back.
- If no `return` runs, Python returns `None`.
- Many mutating methods return `None`, so `return lst.append(x)` is usually wrong.

##### Piece 2 — Exam-style examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
def main(x=0):
    if x > 0:
        return True
    if x < 0:
        return False

print(main())   # None
```

```python
def main(x):
    y = []
    ...
    return [y.append(i)]   # [None], because append returns None
```

##### Piece 3 — What to check in options

_kind:_ `checklist` · _role:_ `trap` · _default selected:_ `yes`

1. Does every path return?
2. Does the function maybe fall off the end?
3. Is the returned expression itself a method that returns `None`?

---

## Parameters & flexible args

> [!tip] Subtopic note
> Defaults, keyword binding, *args, **kwargs.
> Snippets in this subtopic: **2**

### Start here

#### *args and **kwargs

> [!abstract] Snippet metadata
> - Slug: `args-and-kwargs`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `signature` across `5` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `533` chars selected / `772` chars total
> - Keywords: `args`, `dict`, `flexible arguments`, `kwargs`, `tuple`
> - Trap slugs: `args_tuple_shape`, `kwargs_values_not_keys`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q20`, `final-exam-study-guide-trial-python-basics-2023-q12`, `introduction-to-python-trial-final-exam-solutions-py22-q12`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q06`, `resit-solutions-for-introduction-to-python-35761538-q06`, `sample-final-plus-answers-q23`, `trial-final-exam-solutions-introduction-to-python-3077951-q23`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> Flexible-argument questions recur: sum keyword values, compute multiple outputs from any number of integers, or iterate over keyword names in insertion order.

**Summary.** The shapes of `*args` and `**kwargs`, and the common tasks the exams build around them.

##### Piece 1 — *args / **kwargs cheat table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Parameter form | Inside function it is |
|---|---|
| `def f(*args):` | tuple of positional extras |
| `def f(**kwargs):` | dict of keyword extras |
| `kwargs.keys()` | keyword names |
| `kwargs.values()` | passed values |
| `kwargs.items()` | `(key, value)` pairs |

##### Piece 2 — Two exam templates

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def main(*args):
    return {
        'sum': sum(args),
        'pro': math.prod(args),
        'pow': [i**2 for i in args]
    }
```

```python
def main(**kwargs):
    total = 0
    for value in kwargs.values():
        total += value
    return total
```

##### Piece 3 — Less obvious pattern

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
def glue(**kwargs):
    result = ''
    for key in kwargs.keys():
        result = key + result
    return result

glue(a='e', b='d')   # 'ba'
```
The values `'e'` and `'d'` do not matter there; only the **keyword names** matter.

---

#### Defaults and keyword arguments

> [!abstract] Snippet metadata
> - Slug: `defaults-keyword-arguments`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `very-common` across `4` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `378` chars selected / `572` chars total
> - Keywords: `default parameter`, `keyword argument`, `optional`, `parameter binding`
> - Trap slugs: `default_arg_optional`, `keyword_binding_by_name`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q20`, `final-exam-solutions-for-python-programming-62oop21-q21`, `final-exam-study-guide-trial-python-basics-2023-q10`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q04`, `resit-solutions-for-introduction-to-python-35761538-q04`, `sample-final-plus-answers-q01`, `trial-final-exam-solutions-introduction-to-python-3077951-q01`
> - Presets: `balanced-default`

> [!summary] Why it matters
> Questions often hide the whole answer in one tiny detail: a default makes the second argument optional, or a keyword call binds by name instead of position.

**Summary.** How default parameters work, when an argument becomes optional, and how keyword calls are matched.

##### Piece 1 — Binding rules

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Definition | Meaning |
|---|---|
| `def f(x, y=11): ...` | `x` required, `y` optional |
| `f(1)` | valid, uses default `y=11` |
| `f(y=2, x=1)` | valid if names match |
| positional args | matched by position |
| keyword args | matched by parameter name |

##### Piece 2 — Typical exam example

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
def main(x, y=11):
    table = []
    i = 1
    while i < y:
        table.append(f'{x} * {i} = {x*i}')
        i += 1
    return table

main(1)    # valid, because y has a default
```

##### Piece 3 — Elimination hint

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

If the stem calls `main(1)` and the function is `def main(x, y=11):`, reject every option that claims “missing argument”.

---

## Imports & lambda

> [!tip] Subtopic note
> Import names, aliases, lambda, and call shapes.
> Snippets in this subtopic: **2**

### Add next

#### Higher-order functions and lambda

> [!abstract] Snippet metadata
> - Slug: `higher-order-lambda`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `common` across `2` families / `5` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `1/3`
> - Estimated space: `295` chars selected / `673` chars total
> - Keywords: `function argument`, `higher-order`, `lambda`, `map`
> - Trap slugs: `lambda_call_shape`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q22`, `sample-final-plus-answers-q16`, `sample-final-plus-answers-q23`, `trial-final-exam-solutions-introduction-to-python-3077951-q16`, `trial-final-exam-solutions-introduction-to-python-3077951-q23`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> Lambda questions are usually short but high-yield: once you know the call shape, they become free points.

**Summary.** Lambda syntax, list-of-lambdas, and functions that receive another function plus values.

##### Piece 1 — Core forms

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Pattern | Meaning |
|---|---|
| `lambda x: x + 5` | anonymous function with one parameter |
| `lambda a, b: a * b` | anonymous function with two parameters |
| `list(map(lambda x: x*2, x))` | apply function to each element, then force list |
| `f(func, *args)` | pass a function, then values |

##### Piece 2 — Exam-style examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
funcs = [lambda a, b: a + b, lambda a, b: a * b]
funcs[0](1, 2) ** funcs[1](1, 2)   # 3 ** 2 = 9
```

```python
def calculation(func, *args):
    return sum(func(el) for el in args)

calculation(lambda x: x + 5, 1, 2, 3, 4)  # 30
```

##### Piece 3 — Trap hint

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `no`

If the exam prints a `map(...)` object directly, remember that raw `map` is not a list; wrap it in `list(...)` when a list is expected.

---

### Edge cases / niche

#### Imports and aliases

> [!abstract] Snippet metadata
> - Slug: `imports-and-aliases`
> - Phase: `pre-midterm`
> - Default priority: `3`
> - Difficulty: `beginner`
> - Recurrence: `rare` across `1` families / `2` questions
> - UI section: `edge-cases` — Edge cases / niche
> - Default-selected pieces: `2/2`
> - Estimated space: `372` chars selected / `372` chars total
> - Keywords: `alias`, `import`, `math`, `pi`
> - Trap slugs: `import_alias_name_mismatch`
> - Question refs: `sample-final-plus-answers-q24`, `trial-final-exam-solutions-introduction-to-python-3077951-q24`
> - Presets: _none_

> [!summary] Why it matters
> Import questions are easy to lose for a silly reason: you imported under one name but used another.

**Summary.** Exact name rules for `import`, `from ... import ...`, and aliases.

##### Piece 1 — Import patterns

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Code | How to use it later |
|---|---|
| `import math` | `math.pi` |
| `from math import pi` | `pi` |
| `import math as constants` | `constants.pi` |
| `from math import pi as constant` | `constant` |

##### Piece 2 — Immediate exam rule

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

If you alias a module, you **must** use the alias:
```python
import math as constants
print(constants.pi * r**2)   # correct
print(math.pi * r**2)        # wrong here
```

---

# Strings

> [!info] Topic note
> String methods, formatting, and parsing mini-problems.
> Snippets in this topic: **6**

## Methods

> [!tip] Subtopic note
> split/join/replace/find/count/case methods.
> Snippets in this subtopic: **3**

### Start here

#### split(), join(), replace()

> [!abstract] Snippet metadata
> - Slug: `split-join-replace`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `12` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `480` chars selected / `744` chars total
> - Keywords: `join`, `replace`, `split`, `strings`
> - Trap slugs: `join_called_on_separator`, `string_immutable_reassign`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q03`, `final-exam-solutions-for-python-programming-62oop21-q04`, `final-exam-solutions-for-python-programming-62oop21-q09`, `final-exam-solutions-for-python-programming-62oop21-q19`, `final-exam-study-guide-trial-python-basics-2023-q17`, `final-exam-study-guide-trial-python-basics-2023-q18`, `introduction-to-python-trial-final-exam-solutions-py22-q17`, `introduction-to-python-trial-final-exam-solutions-py22-q18`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q14`, `resit-solutions-for-introduction-to-python-35761538-q14`, `sample-final-plus-answers-q04`, `trial-final-exam-solutions-introduction-to-python-3077951-q04`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> These methods power URL/email/phone parsing, sentence shuffling, capitalization fixes, and many distractors.

**Summary.** The three most exam-relevant string methods: split into parts, join parts back, and replace text.

##### Piece 1 — Method table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Call | Output | Note |
|---|---|---|
| `'a-b-c'.split('-')` | `['a','b','c']` | returns list of pieces |
| `'-'.join(['a','b'])` | `'a-b'` | separator calls `.join(...)` |
| `'book-book'.replace('book', 'novel', 1)` | `'novel-book'` | third argument limits replacements |

Docs-style optional-argument reminder: `text.replace(old, new[, count])`.

##### Piece 2 — Exam-style patterns

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
"020-525-14-00".replace("-", "")      # '0205251400'
"020-525-14-00".split("-")            # ['020', '525', '14', '00']
"".join("020-525-14-00".split("-"))   # '0205251400'
```

```python
words = sentence.split()
random.shuffle(words)
" ".join(words)
```

##### Piece 3 — Join trap

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

`join` is called on the **separator string**, not on the list:
```python
'-'.join(words)    # correct
words.join('-')    # wrong
```

---

### Add next

#### find(), index(), count()

> [!abstract] Snippet metadata
> - Slug: `find-index-count`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `common` across `3` families / `5` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/3`
> - Estimated space: `424` chars selected / `692` chars total
> - Keywords: `count`, `find`, `index`, `search`
> - Trap slugs: `count_is_method`, `find_minus_one_index_valueerror`
> - Question refs: `introduction-to-python-trial-final-exam-solutions-py22-q11`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q13`, `resit-solutions-for-introduction-to-python-35761538-q13`, `sample-final-plus-answers-q22`, `trial-final-exam-solutions-introduction-to-python-3077951-q22`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`

> [!summary] Why it matters
> The bank uses these methods directly and also hides them inside “replace only the second occurrence” questions.

**Summary.** Search-like string methods: where something starts, how many times it occurs, and when you get `-1` versus an error.

##### Piece 1 — Comparison table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Call shape | If found | If not found |
|---|---|---|
| `'banana'.find('na')` | start index such as `2` | `-1` |
| `'banana'.index('na')` | start index such as `2` | `ValueError` |
| `'banana'.count('na')` | count such as `2` | `0` |

##### Piece 2 — Second occurrence pattern

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
index = sentence.find('book')
index = sentence.find('book', index + 1)
new_sentence = sentence[:index] + 'novel' + sentence[index + 4:]
```
This targets the **second** `book` only.

##### Piece 3 — Method call reminder

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
x = 'Amsterdam'
x.count('a')      # 1
x.find('d')       # 5
count(x, 'a')     # wrong in normal Python
```
Docs-style optional-argument reminder:
- `text.find(value[, start[, end]])`
- `text.index(value[, start[, end]])`
- `text.count(value[, start[, end]])`

---

#### Case methods and capitalization

> [!abstract] Snippet metadata
> - Slug: `case-and-capitalization`
> - Phase: `post-midterm`
> - Default priority: `3`
> - Difficulty: `beginner`
> - Recurrence: `common` across `3` families / `5` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/2`
> - Estimated space: `520` chars selected / `520` chars total
> - Keywords: `capitalize`, `islower`, `isupper`, `lower`, `upper`
> - Trap slugs: `case_method_pipeline`
> - Question refs: `introduction-to-python-trial-final-exam-solutions-py22-q18`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q10`, `resit-solutions-for-introduction-to-python-35761538-q10`, `sample-final-plus-answers-q12`, `trial-final-exam-solutions-introduction-to-python-3077951-q12`
> - Presets: `post-midterm-tilted`

> [!summary] Why it matters
> Case conversion appears in list comprehensions, proper-noun cleanup, and string-validation distractors.

**Summary.** The case methods that appear most often: `lower`, `upper`, `islower`, `isupper`, and `capitalize`.

##### Piece 1 — Quick reference

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Call | Output example | Use |
|---|---|---|
| `'AbC'.lower()` | `'abc'` | all lower-case |
| `'AbC'.upper()` | `'ABC'` | all upper-case |
| `'abc'.islower()` | `True` | boolean test |
| `'ABC'.isupper()` | `True` | boolean test |
| `'aMSTERDAM'.capitalize()` | `'Amsterdam'` | first char upper, rest lower |

##### Piece 2 — Swap-case comprehension

_kind:_ `example` · _role:_ `core` · _default selected:_ `yes`

```python
[letter.upper() if letter.islower() else letter.lower() for letter in list_1]
```

Proper-noun cleanup pattern:
```python
for word in names:
    sentence = sentence.replace(word, word.capitalize())
```

---

## Formatting

> [!tip] Subtopic note
> f-strings, .format(), and targeted edits.
> Snippets in this subtopic: **2**

### Start here

#### f-strings and .format()

> [!abstract] Snippet metadata
> - Slug: `fstrings-and-format`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `very-common` across `4` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/4`
> - Estimated space: `444` chars selected / `1040` chars total
> - Keywords: `f-string`, `format`, `placeholder`, `printing`
> - Trap slugs: `format_placeholder_mismatch`, `misspelled_variable_name`
> - Question refs: `final-exam-study-guide-trial-python-basics-2023-q13`, `final-exam-study-guide-trial-python-basics-2023-q23`, `introduction-to-python-trial-final-exam-solutions-py22-q13`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q14`, `resit-solutions-for-introduction-to-python-35761538-q14`, `sample-final-plus-answers-q03`, `trial-final-exam-solutions-introduction-to-python-3077951-q03`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> Formatting questions are usually won by reading placeholders carefully and spotting spelling/placeholder mismatches.

**Summary.** String formatting patterns that actually show up in the bank: f-strings, positional `.format`, and named placeholders.

##### Piece 1 — Formatting patterns

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Style | Example |
|---|---|
| f-string | `f"{name} receives ${salary}"` |
| positional `.format` | `"The {0} is priced at ${1}.".format(item, price)` |
| named `.format` | `"My name is {name}".format(name=name)` |

##### Piece 2 — Exam-like reminders

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

- Positional placeholders `{0}`, `{1}` depend on argument order.
- Named placeholders `{name}` need keyword-style arguments.
- A perfectly formatted string still fails if you print the wrong variable name (`message` vs `mesage`).

##### Piece 3 — Tiny examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
item = "laptop"; price = 1299.99
"The {0} is priced at ${1}.".format(item, price)
```

```python
for student in students:
    print(f"{student['Name']} has received a grade of {student['Grade']:.1f}.")
```
Use `:.1f` when the stem explicitly asks for one decimal place.

##### Piece 4 — List-of-dicts print pattern

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
students = [{"Name": "Adam", "Grade": 7.5}, {"Name": "Bernard", "Grade": 8.0}]

for student in students:
    print(f"{student['Name']} has received a grade of {student['Grade']:.1f}.")
```
If `students` is a **list**, do not call `.items()` on it. Iterate through the list first, then index each dictionary.

---

#### Targeted string edits

> [!abstract] Snippet metadata
> - Slug: `targeted-string-edit-patterns`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `very-common` across `4` families / `6` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `415` chars selected / `623` chars total
> - Keywords: `anagram`, `replace count`, `second occurrence`, `swap`
> - Trap slugs: `replace_count_order`, `string_immutable_reassign`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q04`, `final-exam-solutions-for-python-programming-62oop21-q19`, `final-exam-study-guide-trial-python-basics-2023-q18`, `introduction-to-python-trial-final-exam-solutions-py22-q18`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q13`, `resit-solutions-for-introduction-to-python-35761538-q13`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`

> [!summary] Why it matters
> These questions reward knowing the exact order of operations, especially because strings are immutable and `replace(..., count)` works left-to-right.

**Summary.** Small but common string-edit tasks: swap two marked letters, replace only one occurrence, or normalize text before comparison.

##### Piece 1 — Single-occurrence replace rule

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

`text.replace(old, new, 1)` changes only the **first** match from left to right.

To target the second occurrence, the usual exam-safe pattern is:
- find the first one
- search again starting at `index + 1`
- rebuild the string around that second index

##### Piece 2 — Swap `x` and `y` when each appears once

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
s1 = "x and y"
s1 = s1.replace('y', 'x', 1).replace('x', 'y', 1)
# 'y and x'
```
This works because after `y -> x`, the **first** `x` from the left is still the original `x`, which then becomes `y`.

##### Piece 3 — Normalize before comparing strings

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def is_anagram(word_1, word_2):
    w1 = word_1.replace(" ", "").lower()
    w2 = word_2.replace(" ", "").lower()
    return sorted(w1) == sorted(w2)
```

---

## Parsing

> [!tip] Subtopic note
> URL, email, and phone parsing patterns.
> Snippets in this subtopic: **1**

### Start here

#### URL, email, and phone parsing

> [!abstract] Snippet metadata
> - Slug: `url-email-phone-parsing`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `common` across `3` families / `5` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `412` chars selected / `630` chars total
> - Keywords: `email`, `parse`, `phone`, `split`, `url`
> - Trap slugs: `parse_host_before_extension`, `string_immutable_reassign`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q03`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q15`, `resit-solutions-for-introduction-to-python-35761538-q15`, `sample-final-plus-answers-q04`, `trial-final-exam-solutions-introduction-to-python-3077951-q04`
> - Presets: `balanced-default`, `post-midterm-tilted`, `ultra-dense-core`

> [!summary] Why it matters
> The exam likes “extract piece X from string Y” questions. They are easiest when you think in short pipelines.

**Summary.** Reusable parsing pipelines for URLs, email addresses, and phone numbers.

##### Piece 1 — Three common pipelines

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Task | Safe pipeline |
|---|---|
| URL TLD | `url.split('//')[1].split('/')[0].split('.')[-1]` |
| email local/domain | `local, domain = email.split('@')` |
| phone digits only | `''.join(number.split('-'))` or filter digits |

##### Piece 2 — Why some URL options fail

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

If you split on `'.'` too early, you may grab the page extension (`html`) instead of the domain extension (`nl`).  
Usually isolate the **host** first, then take the last host segment.

##### Piece 3 — Exam-style examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
url = "https://www.uva.nl/en/education/bachelors.html"
url.split("//")[1].split("/")[0].split(".")[-1]   # 'nl'

email = "student@uva.nl"
email.split("@")[0]   # 'student'
email.split("@")[1]   # 'uva.nl'
```

---

# Dictionaries & comprehensions

> [!info] Topic note
> Building mappings, comprehension syntax, sets, and dict iteration.
> Snippets in this topic: **6**

## Dictionary patterns

> [!tip] Subtopic note
> Counting, aggregation, iteration, equality, running links.
> Snippets in this subtopic: **3**

### Start here

#### Build, count, and aggregate dictionaries

> [!abstract] Snippet metadata
> - Slug: `dict-build-count-aggregate`
> - Phase: `pre-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `very-common` across `4` families / `11` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `404` chars selected / `736` chars total
> - Keywords: `aggregate`, `count`, `dict`, `values`, `zip`
> - Trap slugs: `dict_counting_pattern`, `keys_vs_values`
> - Question refs: `final-exam-study-guide-trial-python-basics-2023-q05`, `final-exam-study-guide-trial-python-basics-2023-q06`, `final-exam-study-guide-trial-python-basics-2023-q12`, `introduction-to-python-trial-final-exam-solutions-py22-q05`, `introduction-to-python-trial-final-exam-solutions-py22-q06`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q08`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q09`, `resit-solutions-for-introduction-to-python-35761538-q08`, `resit-solutions-for-introduction-to-python-35761538-q09`, `sample-final-plus-answers-q19`, `trial-final-exam-solutions-introduction-to-python-3077951-q19`
> - Presets: `balanced-default`, `ultra-dense-core`

> [!summary] Why it matters
> Dictionary construction and counting are a core pre-midterm pattern that still shows up in finals and resits.

**Summary.** How to build dictionaries from lists, count frequencies, and aggregate values from a dictionary.

##### Piece 1 — Core templates

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
# build from two lists
d = {name: age for name, age in zip(names, ages)}

# count frequencies
counts = {}
for grade in grades:
    if grade not in counts:
        counts[grade] = 0
    counts[grade] += 1
```

##### Piece 2 — Aggregate over dictionary values

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
average_score = sum(math_scores.values()) / len(math_scores)
for student in math_scores:
    if math_scores[student] > average_score:
        print(student)
```

```python
max_rating = max(employee_ratings.values())
for employee, rating in employee_ratings.items():
    if rating == max_rating:
        print(employee)
```

##### Piece 3 — Fast reminder

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

- Direct iteration over a dict gives keys.
- `d.values()` gives the numeric values you usually want for `sum`, `max`, `mean`-type logic.
- If you need both key and value, use `d.items()`.

---

#### Dictionary iteration and equality

> [!abstract] Snippet metadata
> - Slug: `dict-iteration-equality`
> - Phase: `pre-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `very-common` across `4` families / `9` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `343` chars selected / `510` chars total
> - Keywords: `dict equality`, `items`, `keys`, `values`
> - Trap slugs: `dict_iterates_keys`, `dict_order_not_equality`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q17`, `final-exam-solutions-for-python-programming-62oop21-q18`, `final-exam-study-guide-trial-python-basics-2023-q06`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q09`, `resit-solutions-for-introduction-to-python-35761538-q09`, `sample-final-plus-answers-q20`, `sample-final-plus-answers-q21`, `trial-final-exam-solutions-introduction-to-python-3077951-q20`, `trial-final-exam-solutions-introduction-to-python-3077951-q21`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> This is one of the most repeated distractor families in the bank.

**Summary.** The dict facts that exam setters love: equality ignores order, direct iteration yields keys, and `.values()` / `.items()` matter.

##### Piece 1 — Two must-know facts

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Fact | Consequence |
|---|---|
| `for x in d:` iterates over keys | `for key, value in d:` fails unless you iterate over `d.items()` |
| `d1 == d2` compares key-value content | insertion order does **not** matter |

##### Piece 2 — Correct iteration shapes

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
for key in d.keys():
    ...

for value in d.values():
    ...

for key, value in d.items():
    ...
```

```python
{1: 5, 4: 6} == {4: 6, 1: 5}   # True
```

##### Piece 3 — Odd-one-out pattern

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

If three options sum or multiply dict values correctly and one uses `for key, value in d:`, that one is usually the bad option.

---

### Add next

#### Running totals and next-link dictionaries

> [!abstract] Snippet metadata
> - Slug: `dict-running-totals-and-next-links`
> - Phase: `pre-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `occasional` across `2` families / `3` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/3`
> - Estimated space: `415` chars selected / `628` chars total
> - Keywords: `cumulative`, `next item`, `running total`, `zip`
> - Trap slugs: `sorted_running_total_shape`, `zip_next_link`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q16`, `sample-final-plus-answers-q19`, `trial-final-exam-solutions-introduction-to-python-3077951-q19`
> - Presets: `balanced-default`

> [!summary] Why it matters
> These are a little more “algorithmic” than the average MCQ, so having the exact templates saves space and time.

**Summary.** Two recurring dict-construction tasks: cumulative totals and linking each item to the next item.

##### Piece 1 — Next-link dictionary

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def main(l1):
    return {left: right for left, right in zip(l1[:-1], l1[1:])}
```
Example:
```python
main([1, 3, 2, 4])   # {1: 3, 3: 2, 2: 4}
```

##### Piece 2 — Running-total dictionary

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def main(d):
    result = {}
    for output_key in d:
        result[output_key] = sum(v for k, v in d.items() if k <= output_key)
    return result
```
This preserves the original keys while computing “sum of values whose keys are <= current key”.

##### Piece 3 — Alternative sorted-key approach

_kind:_ `rules` · _role:_ `clarifier` · _default selected:_ `no`

A sorted-key running total also works **if** the required output is just the cumulative value per key:
```python
running_total = 0
for key in sorted(d):
    running_total += d[key]
    out[key] = running_total
```

---

## Comprehensions

> [!tip] Subtopic note
> List/dict/set comprehension construction and syntax placement.
> Snippets in this subtopic: **3**

### Start here

#### Dictionary comprehension patterns

> [!abstract] Snippet metadata
> - Slug: `dict-comprehension-patterns`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `10` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `398` chars selected / `589` chars total
> - Keywords: `dict comprehension`, `len`, `ord`, `zip`
> - Trap slugs: `bool_sum_counts_true`, `dict_comp_key_value_order`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q09`, `final-exam-solutions-for-python-programming-62oop21-q10`, `final-exam-study-guide-trial-python-basics-2023-q04`, `introduction-to-python-trial-final-exam-solutions-py22-q04`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q07`, `resit-solutions-for-introduction-to-python-35761538-q07`, `sample-final-plus-answers-q08`, `sample-final-plus-answers-q11`, `trial-final-exam-solutions-introduction-to-python-3077951-q08`, `trial-final-exam-solutions-introduction-to-python-3077951-q11`
> - Presets: `balanced-default`, `ultra-dense-core`

> [!summary] Why it matters
> This is one of the most repeated patterns across the exams.

**Summary.** Short templates for building dictionaries with comprehensions, plus the few transformations that recur in the bank.

##### Piece 1 — Core shape

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
{key_expr: value_expr for item in source}
```
Examples:
```python
{item: len(item) for item in list_1}
{vowel: ord(vowel) for vowel in 'aeiou'}
{num: roman for num, roman in zip(range(1, 6), ['I','II','III','IV','V'])}
```

##### Piece 2 — Counting with booleans

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
grade_curve = {
    grade: sum(v == grade for v in grades.values())
    for grade in dutch_grades
}
```
Because `True` acts like `1` and `False` like `0`, `sum(...)` counts matches.

##### Piece 3 — High-frequency mistake

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

Check the direction:
- wanted `{word: len(word)}` -> do **not** accidentally write `{len(word): word}`
- wanted `{num: roman}` -> do **not** flip it to `{roman: num}`

---

#### List comprehension patterns

> [!abstract] Snippet metadata
> - Slug: `list-comprehension-patterns`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `316` chars selected / `501` chars total
> - Keywords: `filter`, `if else`, `list comprehension`
> - Trap slugs: `comprehension_if_else_position`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q23`, `final-exam-study-guide-trial-python-basics-2023-q07`, `introduction-to-python-trial-final-exam-solutions-py22-q07`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q10`, `resit-solutions-for-introduction-to-python-35761538-q10`, `sample-final-plus-answers-q12`, `trial-final-exam-solutions-introduction-to-python-3077951-q12`
> - Presets: `balanced-default`, `ultra-dense-core`

> [!summary] Why it matters
> These appear repeatedly and are easy to compress into one mental template.

**Summary.** The two list-comprehension forms you actually need: filter-only and map-with-conditional-expression.

##### Piece 1 — Syntax patterns

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Goal | Pattern |
|---|---|
| keep some items | `[x for x in xs if keep(x)]` |
| transform all items | `[f(x) for x in xs]` |
| transform with `if/else` | `[a if cond(x) else b for x in xs]` |

##### Piece 2 — Examples from the bank

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
[x * 2 if x % 2 == 0 else x for x in numbers]

[x for x in numbers if x % 2 == 0 and x > 2]

[letter.upper() if letter.islower() else letter.lower()
 for letter in list_1]
```

##### Piece 3 — Placement trap

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

- Filter-only `if` goes **after** the `for`.
- `if ... else ...` for choosing between two values goes **before** the `for`.

---

### Edge cases / niche

#### Set vs list vs dict

> [!abstract] Snippet metadata
> - Slug: `set-vs-list-vs-dict`
> - Phase: `post-midterm`
> - Default priority: `3`
> - Difficulty: `beginner`
> - Recurrence: `rare` across `1` families / `2` questions
> - UI section: `edge-cases` — Edge cases / niche
> - Default-selected pieces: `1/2`
> - Estimated space: `255` chars selected / `414` chars total
> - Keywords: `duplicates`, `membership`, `set`, `sorting`
> - Trap slugs: `membership_checks_keys`, `set_removes_duplicates`
> - Question refs: `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q05`, `resit-solutions-for-introduction-to-python-35761538-q05`
> - Presets: _none_

> [!summary] Why it matters
> A few deceptively simple options rely on knowing that sets remove duplicates and that dict membership checks keys, not values.

**Summary.** When to use a set, and how set behavior differs from lists and dicts in the kinds of MCQs this course uses.

##### Piece 1 — One-line facts

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Object | Duplicates kept? | Ordered?* | Typical use |
|---|---:|---:|---|
| list | Yes | Yes | sequence |
| set | No | no reliable order | dedup / fast membership |
| dict | keys unique | insertion order preserved, but equality ignores order | mapping |

##### Piece 2 — Exam pattern

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
x = [1,1,2,2,3,3,4,4,5,5]
sorted(set(x), reverse=True)   # [5,4,3,2,1]
x[::-2]                        # [5,4,3,2,1]
```
Different route, same output.

---

# OOP

> [!info] Topic note
> Constructors, state, methods, and object comparison/reporting patterns.
> Snippets in this topic: **4**

## Constructors & state

> [!tip] Subtopic note
> What goes in __init__, where state lives, collection attributes.
> Snippets in this subtopic: **2**

### Start here

#### __init__, self, defaults, attributes

> [!abstract] Snippet metadata
> - Slug: `oop-init-self-defaults`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `beginner`
> - Recurrence: `signature` across `5` families / `10` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `3/3`
> - Estimated space: `680` chars selected / `680` chars total
> - Keywords: `__init__`, `default attribute`, `instance attribute`, `self`
> - Trap slugs: `attribute_not_on_self`, `default_arg_optional`, `missing_self`, `return_in_init`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q01`, `final-exam-study-guide-trial-python-basics-2023-q16`, `final-exam-study-guide-trial-python-basics-2023-q22`, `introduction-to-python-trial-final-exam-solutions-py22-q16`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q16`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q19`, `resit-solutions-for-introduction-to-python-35761538-q16`, `resit-solutions-for-introduction-to-python-35761538-q19`, `sample-final-plus-answers-q01`, `trial-final-exam-solutions-introduction-to-python-3077951-q01`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> The most repeated OOP pattern in the bank is a class definition where one option forgets `self`, forgets a default, or forgets to save attributes on the instance.

**Summary.** Constructor essentials: `__init__`, `self`, default attributes, and what must be assigned onto the instance.

##### Piece 1 — Constructor checklist

_kind:_ `checklist` · _role:_ `core` · _default selected:_ `yes`

1. First parameter of instance methods is `self`.
2. Required arguments have no default; optional ones do.
3. Save data on the instance: `self.name = name`.
4. `__init__` should initialize state, not `return` values.

##### Piece 2 — Canonical template

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
class Vehicle:
    def __init__(self, name, mode="land"):
        self.name = name
        self.mode = mode
```
This makes `Vehicle("Mazda").mode` become `'land'`.

##### Piece 3 — Common wrong answers

_kind:_ `table` · _role:_ `trap` · _default selected:_ `yes`

| Wrong pattern | Why it fails |
|---|---|
| `def __init__(name, mode):` | missing `self` |
| `return name, mode` inside `__init__` | constructor should not return tuple |
| `name = vehicle_name` | local name only; attribute never stored |
| missing default | call without second arg fails |

---

#### Object state and collection attributes

> [!abstract] Snippet metadata
> - Slug: `oop-state-and-collection-attributes`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `signature` across `5` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/5`
> - Estimated space: `503` chars selected / `1281` chars total
> - Keywords: `append`, `garage`, `list attribute`, `reviews`, `state`
> - Trap slugs: `mutable_default_list`, `state_stored_on_instance`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q02`, `final-exam-study-guide-trial-python-basics-2023-q24`, `introduction-to-python-trial-final-exam-solutions-py22-q16`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q20`, `resit-solutions-for-introduction-to-python-35761538-q20`, `sample-final-plus-answers-q02`, `trial-final-exam-solutions-introduction-to-python-3077951-q02`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> Many class questions are about an internal list attribute that grows over time, or capacity/state logic that depends on it.

**Summary.** How objects store changing state, especially lists such as reviews or stored child objects like cars in a garage.

##### Piece 1 — Safe patterns for collection attributes

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.review_scores = []
```

```python
class Garage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cars = []
```

##### Piece 2 — Add / capacity logic

_kind:_ `example` · _role:_ `core` · _default selected:_ `yes`

```python
def add_car(self, car):
    if len(self.cars) < self.capacity:
        self.cars.append(car)
    else:
        return "Capacity reached."
```

```python
def add_review(self, score):
    self.review_scores.append(score)
```

##### Piece 3 — Mutable-default warning

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `no`

Avoid `cars=[]` or `review_scores=[]` as a default parameter in `__init__` unless you really want that same list reused across objects.  
Safer general pattern:
```python
def __init__(self, reviews=None):
    self.reviews = [] if reviews is None else list(reviews)
```

##### Piece 4 — Average-rating pattern

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
def add_review(self, score):
    self.review_scores.append(score)

def show_rating(self):
    if self.review_scores:
        return round(sum(self.review_scores) / len(self.review_scores), 1)
```
This is the recurring “store scores, then return the rounded average” pattern.

##### Piece 5 — Numbered report dictionary

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
def check_garage(self):
    return {
        i: car.get_description()
        for i, car in enumerate(self.cars, start=1)
    }
```
Use `enumerate(..., start=1)` when the output dictionary must start its keys at `1`.

---

## Methods & comparison

> [!tip] Subtopic note
> self, method calls, comparison/reporting patterns.
> Snippets in this subtopic: **2**

### Start here

#### Compare/report method patterns

> [!abstract] Snippet metadata
> - Slug: `oop-compare-and-report-patterns`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `signature` across `5` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `3/3`
> - Estimated space: `863` chars selected / `863` chars total
> - Keywords: `average score`, `compare objects`, `overview`, `report string`
> - Trap slugs: `compare_both_directions`, `method_call_in_fstring`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q02`, `final-exam-study-guide-trial-python-basics-2023-q23`, `introduction-to-python-trial-final-exam-solutions-py22-q23`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q20`, `resit-solutions-for-introduction-to-python-35761538-q20`, `sample-final-plus-answers-q02`, `trial-final-exam-solutions-introduction-to-python-3077951-q02`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> These are common ‘long OOP’ questions. Once you see the pattern, they become template filling rather than full problem solving.

**Summary.** How the bank writes comparison/report methods: use helper methods, compare object state carefully, then return a title/string/report.

##### Piece 1 — Comparison template

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def compare(self, other):
    for first, second in [(self, other), (other, self)]:
        better_value = first.metric() > second.metric()
        enough_context = first.count() >= second.count()
        if better_value and enough_context:
            return first.title
    return None   # or 'Either', depending on stem
```

##### Piece 2 — Report / overview template

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def payment_overview(self):
    return (
        f'{self.name} receives ${self.salary} monthly, '
        f'${self.holiday_bonus()} in May and '
        f'${self.year_end_bonus()} in December.'
    )
```
Call helper **methods** if the class defines them.

##### Piece 3 — Common traps

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

- Do not return the “other” object too early; first check whether it really beats `self`.
- If the class already has helper methods (`average_score`, `rating`, `holiday_bonus`), use them.
- If the tie rule says `None` or `'Either'`, return exactly that text/value.

---

### Add next

#### Method calls and self

> [!abstract] Snippet metadata
> - Slug: `oop-method-calls-and-self`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `beginner`
> - Recurrence: `common` across `3` families / `4` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/3`
> - Estimated space: `333` chars selected / `570` chars total
> - Keywords: `instance method`, `method call`, `self`
> - Trap slugs: `missing_self`, `self_passed_twice`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q01`, `introduction-to-python-trial-final-exam-solutions-py22-q24`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q19`, `resit-solutions-for-introduction-to-python-35761538-q19`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`

> [!summary] Why it matters
> A classic exam trap is an otherwise-correct method call that passes the object twice.

**Summary.** Define methods with `self`, call them on the object, and do not pass `self` again manually.

##### Piece 1 — Definition vs call

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| In class definition | At call site |
|---|---|
| `def set_date(self, date): ...` | `obj.set_date("29-02-2022")` |
| `def compare(self, other): ...` | `book1.compare(book2)` |

##### Piece 2 — Most common trap

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
my_flight = Flight("KLM", "Amsterdam", "Paris")
my_flight.set_date(my_flight, "29-02-2022")   # wrong
```
Why? Python already passes `my_flight` as `self` automatically.  
Correct:
```python
my_flight.set_date("29-02-2022")
```

##### Piece 3 — Attribute access rule

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

Inside methods, use `self.attr` and `self.method(...)`.  
Bare names like `reviews`, `legs`, or `sound` are usually wrong unless they were defined as locals.

---

# Datetime

> [!info] Topic note
> Parsing, formatting, date arithmetic, overlap logic, and date sequences.
> Snippets in this topic: **5**

## Parsing & formatting

> [!tip] Subtopic note
> strptime/strftime and building datetime objects.
> Snippets in this subtopic: **2**

### Start here

#### strptime() and strftime()

> [!abstract] Snippet metadata
> - Slug: `datetime-strptime-strftime`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `signature` across `5` families / `12` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `372` chars selected / `628` chars total
> - Keywords: `datetime`, `format directives`, `strftime`, `strptime`
> - Trap slugs: `date_directive_order`, `strptime_vs_strftime`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q11`, `final-exam-study-guide-trial-python-basics-2023-q15`, `final-exam-study-guide-trial-python-basics-2023-q21`, `introduction-to-python-trial-final-exam-solutions-py22-q15`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q17`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q21`, `resit-solutions-for-introduction-to-python-35761538-q17`, `resit-solutions-for-introduction-to-python-35761538-q21`, `sample-final-plus-answers-q07`, `sample-final-plus-answers-q09`, `trial-final-exam-solutions-introduction-to-python-3077951-q07`, `trial-final-exam-solutions-introduction-to-python-3077951-q09`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> Datetime questions often look harder than they are; most boil down to one directive string and knowing whether you are parsing or formatting.

**Summary.** The parse/format split, plus the directive patterns that recur throughout the exams.

##### Piece 1 — Parse vs format

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Task | Method | Example |
|---|---|---|
| string -> datetime | `datetime.strptime(s, fmt)` | `datetime.strptime("05.12.2023", "%m.%d.%Y")` |
| datetime -> string | `dt.strftime(fmt)` | `dt.strftime("%d-%m-%Y")` |

##### Piece 2 — Directive mini-table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Directive | Meaning |
|---|---|
| `%d` | day |
| `%m` | month |
| `%Y` | four-digit year |
| `%y` | two-digit year |
| `%H` | hour (24h) |
| `%M` | minute |

##### Piece 3 — Exam-style examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
date = datetime.strptime("04.05.2020", "%m.%d.%Y")
(date + timedelta(days=-10)).strftime("%d-%m-%Y")
# '26-03-2020'
```

```python
datetime.strptime("03-02-2013", "%d-%m-%Y").month   # 2
datetime.strptime("03/02/2013", "%m/%d/%Y").month   # 3
```

---

#### Build datetimes from parts

> [!abstract] Snippet metadata
> - Slug: `datetime-build-from-parts`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `very-common` across `4` families / `6` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `343` chars selected / `564` chars total
> - Keywords: `datetime constructor`, `day month year`, `hour minute`
> - Trap slugs: `datetime_arg_order`, `string_not_datetime`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q12`, `final-exam-study-guide-trial-python-basics-2023-q22`, `introduction-to-python-trial-final-exam-solutions-py22-q21`, `introduction-to-python-trial-final-exam-solutions-py22-q22`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q22`, `resit-solutions-for-introduction-to-python-35761538-q22`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> This shows up in both OOP and pandas questions where day/month/year or hour/minute arrive separately.

**Summary.** Build a full datetime from separate date parts, or from a date string plus a time string.

##### Piece 1 — Constructor order

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Build from parts | Pattern |
|---|---|
| date only | `datetime(year, month, day)` |
| date + time | `datetime(year, month, day, hour, minute)` |

##### Piece 2 — From date string and time string

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
self.date = datetime.strptime(date, '%d-%m-%Y')
hour, minute = start.split(':')
self.start = datetime(
    self.date.year, self.date.month, self.date.day,
    int(hour), int(minute)
)
```

##### Piece 3 — From DataFrame columns

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
df['Date'] = pd.Series([
    datetime(y, m, d).strftime('%d-%m-%Y')
    for d, m, y in zip(df['Day'], df['Month'], df['Year'])
])
```
Note the constructor order is `(year, month, day)`, not `(day, month, year)`.

---

## Arithmetic & overlap

> [!tip] Subtopic note
> timedelta, day counts, date windows, overlap logic.
> Snippets in this subtopic: **2**

### Start here

#### timedelta and day counts

> [!abstract] Snippet metadata
> - Slug: `datetime-timedelta-day-counts`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `signature` across `5` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `387` chars selected / `552` chars total
> - Keywords: `days`, `difference`, `timedelta`, `weeks`
> - Trap slugs: `inclusive_plus_one`, `timedelta_requires_datetime`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q11`, `final-exam-study-guide-trial-python-basics-2023-q15`, `introduction-to-python-trial-final-exam-solutions-py22-q15`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q17`, `resit-solutions-for-introduction-to-python-35761538-q17`, `sample-final-plus-answers-q10`, `trial-final-exam-solutions-introduction-to-python-3077951-q10`
> - Presets: `balanced-default`, `post-midterm-tilted`, `ultra-dense-core`

> [!summary] Why it matters
> This snippet covers day-of-year, day differences, one-week jumps, and inclusive counting questions.

**Summary.** Use `timedelta` for shifting datetimes and `.days` for whole-day differences.

##### Piece 1 — Core formulas

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Goal | Pattern |
|---|---|
| shift by N days | `dt + timedelta(days=N)` |
| shift by N weeks | `dt + timedelta(weeks=N)` |
| whole-day difference | `(dt2 - dt1).days` |
| day of year | `(dt - datetime(dt.year, 1, 1)).days + 1` |

##### Piece 2 — Inclusive count example

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
(datetime.strptime('2023/1/10', '%Y/%m/%d') - datetime(2023, 1, 1)).days + 1
# 10
```
Without `+ 1`, the difference from Jan 1 to Jan 10 is `9` whole days.

##### Piece 3 — Type trap

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

A `timedelta` can be added to a **datetime**, not to a formatted date string.  
Keep values as datetimes while computing; convert to strings only at the end.

---

### Add next

#### Overlap logic

> [!abstract] Snippet metadata
> - Slug: `datetime-overlap-logic`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `occasional` across `2` families / `2` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `3/3`
> - Estimated space: `508` chars selected / `508` chars total
> - Keywords: `interval`, `meeting`, `overlap`
> - Trap slugs: `overlap_is_not_nonoverlap`, `string_not_datetime`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q12`, `introduction-to-python-trial-final-exam-solutions-py22-q21`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`

> [!summary] Why it matters
> Meeting/lunch-overlap questions recur and are surprisingly template-like.

**Summary.** The overlap rule for meetings/events and the common string-vs-datetime mistakes around it.

##### Piece 1 — Overlap rule

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

Two intervals overlap iff:
```python
start1 < end2 and end1 > start2
```
Equivalent idea: overlap is the opposite of
```python
end1 <= start2 or start1 >= end2
```

##### Piece 2 — Lunch-meeting pattern

_kind:_ `example` · _role:_ `core` · _default selected:_ `yes`

```python
lunch_start = datetime(self.date.year, self.date.month, self.date.day, 12, 30)
lunch_end = lunch_start + timedelta(minutes=30)
return self.start < lunch_end and self.end > lunch_start
```

##### Piece 3 — Trap hints

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

- Compare **datetimes**, not raw strings like `"13:00"`.
- If the method asks for overlap, reject the option that returns the non-overlap condition.

---

## Sequence generation

> [!tip] Subtopic note
> Build repeated date sequences from ranges or dicts.
> Snippets in this subtopic: **1**

### Add next

#### Date sequences

> [!abstract] Snippet metadata
> - Slug: `datetime-sequence-generation`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `common` across `3` families / `4` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `3/3`
> - Estimated space: `718` chars selected / `718` chars total
> - Keywords: `sequence`, `strftime`, `weekly dates`, `weeks`
> - Trap slugs: `format_too_early`, `timedelta_requires_datetime`
> - Question refs: `final-exam-study-guide-trial-python-basics-2023-q21`, `introduction-to-python-trial-final-exam-solutions-py22-q22`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q21`, `resit-solutions-for-introduction-to-python-35761538-q21`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> The bank uses both list-based and DataFrame-based weekly-date generation tasks.

**Summary.** How to generate weekly date series, keep them computable, and only format them at the end.

##### Piece 1 — List of weekly dates

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def main(string):
    date = datetime.strptime(string, '%d-%m-%Y')
    out = [date]
    for _ in range(1, 10):
        out.append(out[-1] + timedelta(weeks=1))
    return [dt.strftime('%d-%m-%Y') for dt in out]
```
Example: `main('01-01-2023')[:3]` starts as `['01-01-2023', '08-01-2023', '15-01-2023']`.

##### Piece 2 — DataFrame weekly index

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
dates = [datetime(2023, 1, 1) + timedelta(weeks=i) for i in range(5)]
df = pd.DataFrame(
    {'Day': [d.day for d in dates],
     'Month': [d.month for d in dates],
     'Year': [d.year for d in dates]},
    index=[d.strftime('%d-%m-%y') for d in dates]
)
```

##### Piece 3 — Most common mistake

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

If you store strings too early, the next line `previous_date + timedelta(...)` fails because the previous item is no longer a datetime.

---

# Pandas

> [!info] Topic note
> Selection, transforms, boolean masks, construction, and sorting.
> Snippets in this topic: **8**

## Selection

> [!tip] Subtopic note
> Series/DataFrame, loc/iloc, masks, index alignment.
> Snippets in this subtopic: **3**

### Start here

#### Series vs DataFrame

> [!abstract] Snippet metadata
> - Slug: `pandas-series-vs-dataframe`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `signature` across `5` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `266` chars selected / `459` chars total
> - Keywords: `DataFrame`, `Series`, `shape`, `single column`
> - Trap slugs: `series_vs_dataframe_shape`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q07`, `final-exam-study-guide-trial-python-basics-2023-q14`, `introduction-to-python-trial-final-exam-solutions-py22-q14`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q18`, `resit-solutions-for-introduction-to-python-35761538-q18`, `sample-final-plus-answers-q05`, `trial-final-exam-solutions-introduction-to-python-3077951-q05`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> Several pandas questions are solved instantly once you know whether an option returns a Series or a DataFrame.

**Summary.** The shape difference between selecting one column as a Series and selecting one-column DataFrame slices.

##### Piece 1 — One-column selection shapes

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Code | Result shape |
|---|---|
| `df['B']` | Series |
| `df.loc[:, 'B']` | Series |
| `df[['B']]` | DataFrame |
| `df.loc[:, ['B']]` | DataFrame |

##### Piece 2 — Exam-style consequences

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

If the printed output shows:
```python
1    4
2    5
3    6
Name: B, dtype: int64
```
you want a **Series** selection, such as:
```python
df['B']
df.loc[:, 'B']
```
Not:
```python
df[['B']]
```

##### Piece 3 — Datatype-difference trap

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

When multiple lines “make the same selection”, check whether one of them changes the result from Series -> DataFrame.

---

#### loc vs iloc

> [!abstract] Snippet metadata
> - Slug: `pandas-loc-iloc`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `very-common` across `4` families / `8` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `207` chars selected / `454` chars total
> - Keywords: `iloc`, `labels`, `loc`, `positions`
> - Trap slugs: `custom_index_not_zero_based`, `loc_vs_iloc`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q07`, `introduction-to-python-trial-final-exam-solutions-py22-q14`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q18`, `resit-solutions-for-introduction-to-python-35761538-q18`, `sample-final-plus-answers-q05`, `sample-final-plus-answers-q06`, `trial-final-exam-solutions-introduction-to-python-3077951-q05`, `trial-final-exam-solutions-introduction-to-python-3077951-q06`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> The exams repeatedly mix DataFrames with row labels starting at 1 and positional indexing starting at 0.

**Summary.** Use `loc` for labels and `iloc` for integer positions. This single distinction solves many pandas MCQs.

##### Piece 1 — loc vs iloc

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Accessor | Rows/cols interpreted as |
|---|---|
| `loc` | labels |
| `iloc` | integer positions |

##### Piece 2 — Bank-style examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
# custom row labels are 1..6
df.loc[2::2, 'B']       # rows with labels 2,4,6
df.iloc[[1,3,5], 1]     # same positions if column B is at position 1
```

```python
df.loc[df.index % 2 == 0, ['B']]   # even labels, one-column DataFrame
```

##### Piece 3 — Fast warning

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

If the index shown in the printed DataFrame starts at `1`, then `loc[2]` means label `2`, not the third row.

---

#### Boolean masks and indexing

> [!abstract] Snippet metadata
> - Slug: `pandas-boolean-mask-and-indexing`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `common` across `3` families / `5` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `434` chars selected / `651` chars total
> - Keywords: `and`, `boolean mask`, `filter rows`, `or`
> - Trap slugs: `boolean_mask_parentheses`, `invalid_dataframe_tuple_index`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q07`, `final-exam-solutions-for-python-programming-62oop21-q08`, `final-exam-study-guide-trial-python-basics-2023-q19`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q23`, `resit-solutions-for-introduction-to-python-35761538-q23`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> This is one of the highest-frequency pandas skills in the bank.

**Summary.** Filter rows with boolean conditions and combine conditions safely.

##### Piece 1 — Correct mask syntax

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
df[(df['Age'] > 30) & (df['Gender'] == 'Male')]
df.loc[df['Height'] > 170, ['Player', 'Age']]
```
Correct exam options use `&` / `|` with **parentheses around each condition**.

##### Piece 2 — What is invalid

_kind:_ `table` · _role:_ `trap` · _default selected:_ `yes`

| Wrong code | Why |
|---|---|
| `df[df['Age'] > 30 & df['Gender'] == 'Male']` | missing parentheses |
| `df[1, 'Age']` | DataFrame does not use tuple indexing like that here |
| `df.loc(df['Age'] > 30)` | `loc` is an indexer, not a function call |

##### Piece 3 — Mask + keep all columns / some columns

_kind:_ `rules` · _role:_ `core` · _default selected:_ `no`

- `df[mask]` keeps rows where mask is `True`.
- `df.loc[mask, ['A','B']]` keeps rows by mask and only columns `A`,`B`.
- For “above average salary” questions, first compute the average, then compare each salary to it.

---

## Transforms

> [!tip] Subtopic note
> Vectorized columns, map/apply, string/date transforms.
> Snippets in this subtopic: **3**

### Start here

#### map() vs apply()

> [!abstract] Snippet metadata
> - Slug: `pandas-map-vs-apply`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `very-common` across `4` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `557` chars selected / `792` chars total
> - Keywords: `apply`, `axis=1`, `map`, `rowwise`
> - Trap slugs: `map_element_only_vs_apply_row`, `map_expression_not_function`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q05`, `final-exam-study-guide-trial-python-basics-2023-q19`, `final-exam-study-guide-trial-python-basics-2023-q20`, `introduction-to-python-trial-final-exam-solutions-py22-q19`, `introduction-to-python-trial-final-exam-solutions-py22-q20`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q24`, `resit-solutions-for-introduction-to-python-35761538-q24`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`, `ultra-dense-core`

> [!summary] Why it matters
> This is the main pandas trap family: elementwise vs rowwise reasoning.

**Summary.** When to use `Series.map(...)` and when to use `DataFrame.apply(..., axis=1)`.

##### Piece 1 — Decision table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Situation | Use |
|---|---|
| transform each element of one Series | `series.map(func)` |
| need multiple columns from same row | `df.apply(func, axis=1)` |
| no custom logic; simple arithmetic | direct vectorized ops |

##### Piece 2 — Correct examples

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
df['Bonus'] = df.apply(
    lambda row: row['Salary']*0.05 if row['Performance_review'] >= 4 else 0,
    axis=1
)
```

```python
df['Name_Length'] = df['Name'].map(len)
df['Name_Suffix'] = df['Name'].map(lambda x: x[-2:])
```

##### Piece 3 — Common wrong patterns

_kind:_ `table` · _role:_ `trap` · _default selected:_ `yes`

| Wrong pattern | Why |
|---|---|
| `series.map((series - series.mean())**2)` | `map` expects a function / mapping, not a finished Series expression |
| `df['Salary'].map(lambda x: ... if df['Performance_review'] >= 4 else 0)` | condition uses whole column, not current row |
| `df.apply(df['A'] - df['B'])` | `apply` is being misused |

---

#### Vectorized new columns

> [!abstract] Snippet metadata
> - Slug: `pandas-vectorized-new-columns`
> - Phase: `post-midterm`
> - Default priority: `5`
> - Difficulty: `mixed`
> - Recurrence: `common` across `3` families / `7` questions
> - UI section: `start-here` — Start here
> - Default-selected pieces: `2/3`
> - Estimated space: `310` chars selected / `432` chars total
> - Keywords: `column arithmetic`, `new column`, `vectorized`
> - Trap slugs: `broadcast_shape_mismatch`, `vectorized_ops_vs_map`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q05`, `final-exam-solutions-for-python-programming-62oop21-q06`, `final-exam-study-guide-trial-python-basics-2023-q20`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q23`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q24`, `resit-solutions-for-introduction-to-python-35761538-q23`, `resit-solutions-for-introduction-to-python-35761538-q24`
> - Presets: `balanced-default`, `post-midterm-tilted`, `ultra-dense-core`

> [!summary] Why it matters
> Many pandas questions are easiest because the answer is just `df['new'] = df['A'] - df['B']` or a similar vectorized expression.

**Summary.** Create new columns with vectorized column arithmetic instead of row-by-row Python loops where possible.

##### Piece 1 — Vectorized patterns

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
df['C'] = df['A'] - df['B']
df['Above_average'] = df['Salary'] > mean_salary
df['Salary_difference'] = df['Salary'] - mean_salary
```

##### Piece 2 — Scalar + Series is fine

_kind:_ `rules` · _role:_ `core` · _default selected:_ `yes`

These are valid elementwise operations:
```python
df['A'] + 5
df['Salary'] - mean_salary
(df['A'] - df['A'].mean())**2
```
A scalar broadcasts across the whole Series.

##### Piece 3 — Trap hint

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `no`

If you can already express the desired result as column arithmetic, prefer that over forcing `.map(...)` in a strange way.

---

### Add next

#### String/date columns

> [!abstract] Snippet metadata
> - Slug: `pandas-string-and-date-columns`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `occasional` across `2` families / `3` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/3`
> - Estimated space: `426` chars selected / `528` chars total
> - Keywords: `date column`, `map`, `pandas strings`, `replace`
> - Trap slugs: `column_transform_assignment`, `datetime_arg_order`
> - Question refs: `introduction-to-python-trial-final-exam-solutions-py22-q19`, `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q22`, `resit-solutions-for-introduction-to-python-35761538-q22`
> - Presets: `balanced-default`, `post-midterm-tilted`

> [!summary] Why it matters
> These questions look varied but collapse to a few short patterns.

**Summary.** Common column transforms on strings and dates: abbreviations, suffixes, replacements, and building date strings.

##### Piece 1 — Common column transforms

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
df['Sex_abbr'] = df['Gender'].map(lambda x: 'M' if x == 'Male' else 'F')
df['Name_Length'] = df['Name'].map(len)
df['Name_Suffix'] = df['Name'].map(lambda x: x[-2:])
df['Occupation'] = df['Occupation'].map(
    lambda x: 'Software Developer' if x == 'Engineer' else x
)
```

##### Piece 2 — Date column from Day/Month/Year

_kind:_ `example` · _role:_ `core` · _default selected:_ `yes`

```python
df['Date'] = pd.Series([
    datetime(y, m, d).strftime('%d-%m-%Y')
    for d, m, y in zip(df['Day'], df['Month'], df['Year'])
])
```

##### Piece 3 — Trap hint

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `no`

If you call `.map(...)` but never assign the result back to the column, the DataFrame stays unchanged.

---

## Construction & sorting

> [!tip] Subtopic note
> Creating DataFrames and sorting them correctly.
> Snippets in this subtopic: **2**

### Add next

#### sort_index() vs sort_values()

> [!abstract] Snippet metadata
> - Slug: `pandas-sort-index-vs-values`
> - Phase: `post-midterm`
> - Default priority: `4`
> - Difficulty: `mixed`
> - Recurrence: `common` across `3` families / `4` questions
> - UI section: `add-next` — Add next
> - Default-selected pieces: `2/3`
> - Estimated space: `301` chars selected / `561` chars total
> - Keywords: `ascending`, `sort_index`, `sort_values`
> - Trap slugs: `sort_index_vs_sort_values`
> - Question refs: `final-exam-solutions-for-python-programming-62oop21-q08`, `introduction-to-python-trial-final-exam-solutions-py22-q20`, `sample-final-plus-answers-q06`, `trial-final-exam-solutions-introduction-to-python-3077951-q06`
> - Presets: `balanced-default`, `post-midterm-tilted`, `trap-hunter`

> [!summary] Why it matters
> Several pandas reverse-engineering questions depend on this distinction.

**Summary.** Choose `sort_index` when ordering by labels and `sort_values` when ordering by column contents.

##### Piece 1 — Sorting table

_kind:_ `table` · _role:_ `core` · _default selected:_ `yes`

| Goal | Use |
|---|---|
| sort rows by row labels | `sort_index()` |
| sort columns by column labels | `sort_index(axis=1)` |
| sort rows by column contents | `sort_values('col')` |

##### Piece 2 — Common exam patterns

_kind:_ `example` · _role:_ `clarifier` · _default selected:_ `no`

```python
df1.loc[df1['Language'] != 'Dutch'].sort_values('Height', ascending=False)
```
sorts by the **values in column `Height`**.

```python
df1.sort_index(ascending=False).loc[:, ['A', 'C', 'D']]
```
sorts rows by index labels, then keeps selected columns.

##### Piece 3 — Trap hint

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

If the printed output changes row order because of a column’s numbers, `sort_index()` is almost never the right answer.

---

### Edge cases / niche

#### Build DataFrames from arguments

> [!abstract] Snippet metadata
> - Slug: `pandas-build-from-args`
> - Phase: `post-midterm`
> - Default priority: `3`
> - Difficulty: `mixed`
> - Recurrence: `rare` across `1` families / `2` questions
> - UI section: `edge-cases` — Edge cases / niche
> - Default-selected pieces: `2/2`
> - Estimated space: `482` chars selected / `482` chars total
> - Keywords: `*args`, `DataFrame constructor`, `lists as columns`
> - Trap slugs: `dataframe_column_lists_same_length`
> - Question refs: `resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q15`, `resit-solutions-for-introduction-to-python-35761538-q15`
> - Presets: `post-midterm-tilted`

> [!summary] Why it matters
> The email-address question is a pure template once you know the shape.

**Summary.** Build a DataFrame from flexible arguments by collecting one list per column and passing them into `pd.DataFrame(...)`.

##### Piece 1 — Template

_kind:_ `template` · _role:_ `core` · _default selected:_ `yes`

```python
def main(*args):
    local = []
    domain = []
    for email in args:
        local.append(email.split('@')[0])
        domain.append(email.split('@')[1])
    return pd.DataFrame({'local': local, 'domain': domain})
```

##### Piece 2 — Why some options fail

_kind:_ `rules` · _role:_ `trap` · _default selected:_ `yes`

- A single dict value like `data['local'] = email.split('@')[0]` inside the loop keeps overwriting the previous value.
- Column names and extracted values must line up exactly.
- Every column list passed to `pd.DataFrame(...)` must have the same length.

---
