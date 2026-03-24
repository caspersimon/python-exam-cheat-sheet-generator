# Review Packet (round1)

## What Needs Your Review

- This packet condenses the round-1 synthesis into review themes instead of 151 isolated suggestions.
- The goal is to decide which snippet edits/additions are worth implementing before the second evaluation round.
- Completed evaluations: `168`
- Answerability split: `certain=88`, `partial=40`, `insufficient=40`

## Recommended Review Order

1. **Strings, Indexing, and Text Methods** (`priority=high`, `questions=52`, `suggestions=70`, `direction=add_this`)
2. **Loops, Iteration, and Comprehensions** (`priority=high`, `questions=14`, `suggestions=19`, `direction=add_this`)
3. **Functions, Returns, and Scope** (`priority=high`, `questions=11`, `suggestions=31`, `direction=add_this`)
4. **Dictionaries, Tuples, and Sets** (`priority=medium`, `questions=2`, `suggestions=6`, `direction=add_this`)
5. **OOP, self, and Attributes** (`priority=medium`, `questions=1`, `suggestions=7`, `direction=add_this`)
6. **Operators and Boolean Logic** (`priority=medium`, `questions=0`, `suggestions=7`, `direction=add_this`)
7. **Pandas Core Operations** (`priority=medium`, `questions=0`, `suggestions=7`, `direction=add_this`)
8. **Miscellaneous Exam-Specific Gaps** (`priority=selective`, `questions=0`, `suggestions=3`, `direction=add_this`)
9. **Datetime and Timedelta** (`priority=selective`, `questions=0`, `suggestions=1`, `direction=add_this`)

## Priority Themes

### Strings, Indexing, and Text Methods

- Priority: `high`
- Affected questions: `52` (`partial=19`, `insufficient=33`)
- Related synthesized suggestions: `70`
- Suggested direction mix: `{'add_this': 70}`
- Representative gaps:
  - The snippets lack a clear explanation of the difference between label-based (.loc) and integer-position-based (.iloc) indexing, specifically regarding the inclusivity of the stop index.
  - The snippets provide zero explanation for Pandas-specific method syntax required to evaluate the options.
  - The snippets lack a clear example of dictionary comprehension syntax and the specific use of slicing [:-1] to remove a trailing character in a list context.
- Representative suggestions:
  - Key Point: Boolean String Methods. Methods like .islower(), .isupper(), and .isdigit() return True only if the string contains at least one character and all characters meet the criteria. Importantly, .islower() returns False for spaces, punctuation, and numbers as they are not lowercase letters.
  - Create a common question snippet: 'How do zip() and floor division (//) work?'. Content: `zip(list1, list2)` pairs elements by index: (list1[0], list2[0]), (list1[1], list2[1]). `//` is floor division, which divides and rounds down to the whole number (e.g., 5 // 2 = 2).
  - Expand the search text/explanation to explicitly define why option A ([::-2][::-1]) results in [2, 4, 6, 8, 10] (it reverses the reversed slice).

### Loops, Iteration, and Comprehensions

- Priority: `high`
- Affected questions: `14` (`partial=10`, `insufficient=4`)
- Related synthesized suggestions: `19`
- Suggested direction mix: `{'add_this': 19}`
- Representative gaps:
  - The main conceptual hurdle is the implicit conversion of Booleans to integers during a sum operation, and the behavior of an empty match (summing all False values).
  - The main missing piece is a clear explanation of how range(start, stop) behaves regarding the upper bound.
  - There is a complete lack of 'lambda' syntax explanation in the recommended snippets.
- Representative suggestions:
  - Create a 'Comprehension Syntax' summary card: 1. Dictionary: {key: value for item in iterable}, 2. List: [value for item in iterable], 3. Set: {value for item in iterable}.
  - List Comprehension: [expression for item in iterable] creates a new list by running the expression for every item. Example: [i*2 for i in range(3)] generates [0, 2, 4].
  - Create a snippet explaining the range() function: range(0, 10) produces numbers 0, 1, 2, 3, 4, 5, 6, 7, 8, 9. The number 10 is not included.

### Functions, Returns, and Scope

- Priority: `high`
- Affected questions: `11` (`partial=9`, `insufficient=2`)
- Related synthesized suggestions: `31`
- Suggested direction mix: `{'add_this': 27, 'consider_instead': 4}`
- Representative gaps:
  - Existing snippets provide the 'what' (rules) and the 'where' (class), but miss the 'why' regarding the logical structure of comparison functions.
  - Existing snippets cover the 'how' for the correct options but don't explicitly warn against the common mistake of passing a Series into .map().
  - The primary gap is the 'implicit return' behavior. A student can deduce x=0 and see that neither 'if x > 0' nor 'if x < 0' will run, but they won't know what happens when a function 'runs out' of code.
- Representative suggestions:
  - Title: 'Comparing Objects with Multiple Criteria'. Snippet: 'When comparing two objects (A, B) based on multiple rules, remember that ! (A > B) does not imply (B > A). Example: def compare(self, other): if self.val > other.val and self.count >= other.count: return self; if other.val > self.val and other.count >= self.count: return other; return None'
  - Create a snippet titled 'Conditional Expressions vs Statements' showing: 'return "Yes" if check else "No"' is equivalent to 'if check: return "Yes" else: return "No"'.
  - Add a compare method: def is_better(self, other): return self.average() > other.average()

### Dictionaries, Tuples, and Sets

- Priority: `medium`
- Affected questions: `2` (`partial=1`, `insufficient=1`)
- Related synthesized suggestions: `6`
- Suggested direction mix: `{'add_this': 6}`
- Representative gaps:
  - Missing the specific rule that Python dictionaries compare equal if they have the same key-value pairs, regardless of order.
  - The primary gaps are the mathematical syntax for parity checking and exponentiation, as well as the explicit distinction between integer accumulation and list appending.
- Representative suggestions:
  - Create a 'Sequence Properties' card showing that len([]) == 0, len({}) == 0, and len('') == 0, and explaining that a == b == c is only True if all three are identical.
  - Add a snippet explaining 'Sorted Dictionary Iteration': 'To process a dictionary in order of its keys, use `for key in sorted(my_dict.keys()):`. This ensures you visit keys from smallest to largest, which is useful for calculating running totals.'
  - Create a snippet showing: 'for key in sorted(prices.keys()): ...' and another showing 'sub_total = sum([val for key, val in d.items() if key < 10])'.

### OOP, self, and Attributes

- Priority: `medium`
- Affected questions: `1` (`partial=1`, `insufficient=0`)
- Related synthesized suggestions: `7`
- Suggested direction mix: `{'consider_instead': 3, 'add_this': 4}`
- Representative gaps:
  - No snippet explicitly demonstrates the difference between a method reference and a method call (e.g., self.rating vs self.rating()), nor does any snippet show one instance calling a method on another instance (other.rating()).
- Representative suggestions:
  - Update the search_text to show a snippet of the code for the Vehicle class, specifically including a default value for the 'mode' attribute (e.g., mode='land').
  - Create a snippet explaining 'self' as a reference to the current instance, used to access attributes defined in __init__.
  - Title: Instance Attributes and 'self'. Content: 'To make an attribute available on an object (like my_car.name), you must assign it to self inside the __init__ method (e.g., self.name = vehicle_name). Without self, the variable only exists temporarily during creation.'

### Operators and Boolean Logic

- Priority: `medium`
- Affected questions: `0` (`partial=0`, `insufficient=0`)
- Related synthesized suggestions: `7`
- Suggested direction mix: `{'consider_instead': 3, 'add_this': 4}`
- Representative suggestions:
  - Ensure the 'search_text' includes the full code for options a and b and clarifies why both work, matching the provided question explanation.
  - Create a snippet showing: 'my_list = [True, False]; len([]); my_list[0] # Returns True'.
  - Snippet: Comparison Operators. x >= y means 'x is greater than or equal to y'. x < y means 'x is less than y'. Example: 0 >= 0 is True.

### Pandas Core Operations

- Priority: `medium`
- Affected questions: `0` (`partial=0`, `insufficient=0`)
- Related synthesized suggestions: `7`
- Suggested direction mix: `{'add_this': 6, 'consider_instead': 1}`
- Representative suggestions:
  - Create a snippet titled 'Pandas Boolean Filtering' showing: df_filtered = df[df['Salary'] > 50000].
  - Ensure the example code includes a lambda with a condition, e.g., s.map(lambda x: 'High' if x > 10 else 'Low').
  - Create a snippet titled 'Lambda Basics' that explains: 'lambda x: x + 5' means 'take x and add 5 to it'.

### Miscellaneous Exam-Specific Gaps

- Priority: `selective`
- Affected questions: `0` (`partial=0`, `insufficient=0`)
- Related synthesized suggestions: `3`
- Suggested direction mix: `{'add_this': 3}`
- Representative suggestions:
  - Add a snippet demonstrating: count = sum([val == target for val in collection]). Show that this results in an integer, even if the count is zero.
  - Add a foundational snippet explaining that .loc[2:4] includes labels 2, 3, and 4, whereas .iloc[[3, 2, 1]] selects the 4th, 3rd, and 2nd rows respectively.
  - Update the search_text to include the full solution code for option C: word_lengths = {word: len(word) for word in words}.

### Datetime and Timedelta

- Priority: `selective`
- Affected questions: `0` (`partial=0`, `insufficient=0`)
- Related synthesized suggestions: `1`
- Suggested direction mix: `{'add_this': 1}`
- Representative suggestions:
  - Add a 'Topic Detail' or 'Cheat Sheet' item for Week 8 (Datetime) covering: 1. datetime(year, month, day, hour, minute) 2. timedelta(minutes=N) 3. Comparing datetimes using <, >, ==.

## Strong Existing Snippets

| Rank | Snippet | Best single | Top 3 | Minimal set |
|---|---|---:|---:|---:|
| 1 | `exam-intro_python_sample_final_24_25-8-w4-string-fundamentals`<br>Week 5 • Working With Values • recommended/source_exam | 10 | 20 | 18 |
| 2 | `exam-midterm_2023-14-w2-loops`<br>Week 2 • Loops • recommended/source_exam | 5 | 21 | 12 |
| 3 | `exam-intro_python_sample_final_24_25-6-w4-string-operations-and-methods`<br>Week 5 • Inspecting and Selecting Data • recommended/source_exam | 6 | 13 | 11 |
| 4 | `exam-Resit 22/23-7-w2-dictionaries-and-mappings`<br>Week 2 • Dictionaries and Mappings • recommended/source_exam | 4 | 21 | 10 |
| 5 | `exam-intro_python_sample_final_24_25-5-w4-string-fundamentals`<br>Week 5 • Pandas Core Structures • recommended/source_exam | 4 | 15 | 12 |
| 6 | `exam-Test Exam 07-06-22-2-w4-oop-fundamentals`<br>Week 4 • OOP Fundamentals • recommended/source_exam | 7 | 11 | 9 |
| 7 | `exam-Trial final exam Introduction to Python-1-w4-oop-fundamentals`<br>Week 4 • OOP Fundamentals • recommended/source_exam | 3 | 15 | 11 |
| 8 | `exam-extra_practice-9-w3-return-behavior`<br>Week 3 • Return Behavior • recommended/source_exam | 5 | 10 | 7 |
| 9 | `exam-intro_python_sample_final_24_25-10-w6-datetime`<br>Week 6 • Datetime • recommended/source_exam | 5 | 8 | 8 |
| 10 | `exam-intro_python_sample_final_24_25-3-w3-defining-and-calling-functions`<br>Week 3 • Defining and Calling Functions • recommended/source_exam | 5 | 6 | 8 |
| 11 | `exam-Test Exam 07-06-22-5-w5-pandas-core-structures`<br>Week 5 • Pandas Core Structures • recommended/source_exam | 2 | 11 | 7 |
| 12 | `exam-trial-final-exam-py22-5-w2-dictionaries-and-mappings`<br>Week 2 • Dictionaries and Mappings • recommended/source_exam | 1 | 13 | 7 |
| 13 | `aiq-5`<br>Week 5 • Inspecting and Selecting Data • aiQuestions/ai_common_question | 3 | 8 | 6 |
| 14 | `exam-midterm_2023-9-w3-arguments`<br>Week 3 • Arguments • recommended/source_exam | 4 | 8 | 4 |
| 15 | `exam-Trial final exam Introduction to Python-6-w5-inspecting-and-selecting-data`<br>Week 5 • Inspecting and Selecting Data • recommended/source_exam | 2 | 10 | 6 |

## Week Coverage Snapshot

| Week | Top 1 unique | Top 3 unique | Minimal-set unique | Minimal-set unused |
|---|---:|---:|---:|---:|
| 2 | 22 | 34 | 31 | 62 |
| 3 | 22 | 34 | 26 | 38 |
| 1 | 8 | 18 | 15 | 57 |
| 6 | 8 | 13 | 14 | 50 |
| 4 | 7 | 13 | 11 | 37 |
| 5 | 8 | 9 | 9 | 47 |

## Suggested Human Workflow

1. Review the high-priority themes first and decide `add`, `edit existing`, or `skip`.
2. Use the representative suggestions as examples, not as a forced one-to-one implementation list.
3. Favor additions/edits that solve multiple question gaps rather than single-exam edge cases.
4. Only after that review should the implementation round begin.

