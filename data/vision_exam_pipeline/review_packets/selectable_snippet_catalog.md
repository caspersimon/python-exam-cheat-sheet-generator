# Selectable Snippet Catalog

Human-readable export of the full selectable snippet snapshot used by the evaluation pipeline.

## Summary

- Selectable pieces: **801**
- Snippet families: **395**
- Weeks represented: **1, 2, 3, 4, 5, 6**

### Piece Counts By Bucket

- `keyPoints`: 241
- `aiExamples`: 201
- `recommended`: 189
- `aiQuestions`: 86
- `additional`: 84

### Piece Counts By Week

- Week 1: 153
- Week 2: 158
- Week 3: 143
- Week 4: 132
- Week 5: 127
- Week 6: 88

## Week 1

Snippet families in this group: **90**

### Built-ins Intro, Functions, and Modules

- Snippet ID: `subtopic:w1-functions-and-imports:w1-functions-and-imports-core`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `9`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: Import module under its original name import numpy numpy.random.randint(1, 10) # works import numpy as np np.random.randint(1, 10) # works numpy.random.randint(1, 10) # ERROR from numpy.random import randint randint(1,…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: Direct import plus alias binds both names clear_names() import extension as ex try: print(ex.YEAR) except Exception as e: print(e) try: print(extension.YEAR) except Exception as e: print(e) Keep track of which name is a…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: from-import binds only the imported name clear_names() import extension import extension as ex try: print(ex.YEAR) except Exception as e: print(e) try: print(extension.YEAR) except Exception as e: print(e) Keep track of…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: Aliased from-import uses the alias locally clear_names() from extension import create_absolute_year try: print(create_absolute_year(1)) except Exception as e: print(e) try: print(YEAR) except Exception as e: print(e) Ke…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: import module does not create bare globals clear_names() from extension import create_absolute_year as cay try: print(create_absolute_year(1)) except Exception as e: print(e) try: print(cay(1)) except Exception as e: pr…
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: Import module under its original name clear_names() try: print(YEAR) except Exception as e: print(Exception) try: print(extension.YEAR) except Exception as e: print(e) import extension try: print(YEAR) except Exception…
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: Income tax branches and return shape Suppose your country imposes the following tax brackets: Bracket Tax Taxable income rate Over Not over 1 10% $0 $11,000 2 12% $11,000 $45,000 3 22% $45,000 $95,000 4 32% $95,000 If y…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: `import x` keeps the module name, `import x as y` renames it, and `from x import z` brings `z` into scope directly.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Built-ins Intro, Functions, and Modules
  Preview: Use `print(...)` to display a value. A function groups reusable code and may also return a value to its caller.

### Functions and Imports

- Snippet ID: `item:cs-23b2cfd4d6`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `cs-23b2cfd4d6`
  Bucket: `additional` | Type: `source_notebook`
  Preview: imports clear_names() from extension import create_absolute_year as cay try: print(create_absolute_year(1)) except Exception as e: print(e) try: print(cay(1)) except Exception as e: print(e) name 'create_absolute_year'…

### Functions and Imports

- Snippet ID: `item:cs-4155022ebf`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `cs-4155022ebf`
  Bucket: `additional` | Type: `source_notebook`
  Preview: imports clear_names() from extension import create_absolute_year try: print(create_absolute_year(1)) except Exception as e: print(e) try: print(YEAR) except Exception as e: print(e) 2026 name 'YEAR' is not defined

### Functions and Imports

- Snippet ID: `item:cs-5b89a10dcd`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `cs-5b89a10dcd`
  Bucket: `additional` | Type: `source_notebook`
  Preview: imports clear_names() try: print(YEAR) except Exception as e: print(Exception) try: print(extension.YEAR) except Exception as e: print(e) import extension try: print(YEAR) except Exception as e: print(e) try: print(exte…

### Functions and Imports

- Snippet ID: `item:cs-6d0d650063`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `cs-6d0d650063`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: imports clear_names() import extension import extension as ex try: print(ex.YEAR) except Exception as e: print(e) try: print(extension.YEAR) except Exception as e: print(e) 2025 2025

### Functions and Imports

- Snippet ID: `item:cs-beb6591b24`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `cs-beb6591b24`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: imports clear_names() import extension as ex try: print(ex.YEAR) except Exception as e: print(e) try: print(extension.YEAR) except Exception as e: print(e) 2025 name 'extension' is not defined

### Functions and Imports

- Snippet ID: `item:cs-c25503e5db`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `cs-c25503e5db`
  Bucket: `additional` | Type: `source_notebook`
  Preview: imports %%writefile extension.py # In this cell we create a python file and write that to the hard disk (either of your computer or to the cloud depending where you run your code. # We will import this file to show how…

### Functions and Imports

- Snippet ID: `item:exam-Resit 22/23-5-w1-functions-and-imports`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `exam-Resit 22/23-5-w1-functions-and-imports`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have a list called x. Which of the following code segments will print the following list? [5, 4, 3, 2, 1] a b c d c Option A extracts unique elements with `set(x)`, resulting in `{1, 2, 3, 4, 5}`, then sorts…

### Functions and Imports

- Snippet ID: `item:exam-intro_python_sample_final_24_25-24-w2-conditions`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-24-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which script does NOT print the correct answer for the area of a circle? A B C D C If math is imported as constants, it must be referred to as 'constants.pi'. 'math.pi' will no longer be available unless 'math' was also…

### Functions and Imports

- Snippet ID: `item:exam-midterm_2023-12-w1-functions-and-imports`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `exam-midterm_2023-12-w1-functions-and-imports`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You want to write a program to calculate your income tax for 2023.

### Functions and Imports

- Snippet ID: `item:exam-midterm_2024-15-w1-functions-and-imports`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `exam-midterm_2024-15-w1-functions-and-imports`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: def main(lst, condition=lambda x: x): y = [] for x in lst: if condition(x): y.append(x) return y What will this function return, when called in the following way: main([1, 2, 3, 4, 5…

### Functions and Imports

- Snippet ID: `item:exam-midterm_2024-16-w1-functions-and-imports`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `exam-midterm_2024-16-w1-functions-and-imports`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called weather_alert that accepts a string argument, which is a color code of the weather alert system.

### Functions and Imports

- Snippet ID: `item:kp-1-d2`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `9`

- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Call | Use | Typical result int('123') | string to integer | 123 float('123') | string to float | 123.0 str(123.0) | number to string | '123.0' round(x, 2) | round for display/checking | 2 decimals
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dict membership checks KEYS, not values d = {1: 4, 2: 3} print(1 in d) # True (1 is a key) print(4 in d) # False (4 is a value, not a key)
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Wrong bracket errors print[1] # TypeError: 'function' object is not subscriptable l1 = [1,2,3] l1(1) # TypeError: 'list' object is not callable
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Mix defined and *args def adder(n1, n2, *args): result = n1 + n2 for number in args: result += number return result print(adder(1, 2, 3, 4, 5)) # 15
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Tool | Returns | Best for map(f, seq) | lazy transformed iterable | same-length transform filter(f, seq) | lazy filtered iterable | keep matching items sorted(seq, key=...) | new sorted list | comp…
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Form | What it means | Exam use '...'/"..." | basic literals | choose quote style \n / \t | newline / tab | predict printed output r'...' | raw string | slashes stay literal s[i:j:k] | string slici…
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Method | Returns | Trap s.find(x) | index or -1 | never raises s.index(x) | index | raises if missing s.replace(a, b) | new string | strings are immutable sep.join(seq) | new joined string | separa…
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Selector | What it uses | Result df.loc[row, col] | labels | endpoint-inclusive slicing df.iloc[row, col] | positions | Python-style exclusive slice df.head(n) | first rows | quick inspect df[df['A…
- `kp-1-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Operation | Main axis/key idea | When useful pd.concat([...], axis=0) | stack rows | same columns pd.concat([...], axis=1) | add columns | aligned index df.merge(...) | join on key(s) | relational…

### Functions and Imports

- Snippet ID: `item:ks-b6a39f66a2`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `ks-b6a39f66a2`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: intro ### Print is a function and tells Python to output the argument (that what is between the brackets after the function name) on your screen <ul><li>A function is a grouping of code that can perform a certain task a…

### Functions and Imports

- Snippet ID: `item:ks-f43422a4cf`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `ks-f43422a4cf`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Importing packages Multiple import styles. 'import X' makes X available. 'import X as Y' renames. 'from X import Z' brings Z directly into namespace. 'from X import Z as W' renames. Once you use 'as', the original name…

### Functions and Imports

- Snippet ID: `item:manual-implicit-none`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `manual-implicit-none`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What does a function return if it reaches the end without `return`? Python returns `None` if no `return` statement is executed. def f(): print('hi') print(f())

### Functions and Imports

- Snippet ID: `item:manual-import-names`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `manual-import-names`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do different import forms change the names you can use locally? `import math` gives `math.sqrt`, `import math as m` gives `m.sqrt`, and `from math import sqrt` gives `sqrt(...)` directly. import math import math as…

### Functions and Imports

- Snippet ID: `item:manual-print-vs-return`
- Topic: Functions and Imports
- Card ID: `w1-functions-and-imports`
- Piece count: `1`

- `manual-print-vs-return`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What is the difference between printing a value and returning a value from a function? `print(x)` shows a value on screen. `return x` sends a value back to the caller so it can be stored, reused, or printed later. def f…

### Objects and Names

- Snippet ID: `item:aiq-1`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `16`

- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Which of the following statements is correct? I: Two objects can have different values, while having the same type. II: Two objects can have the same value, while having different types. I is correct (e.g. a=1, b=2, bot…
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What is the result of (a//b)*b + a%b? Arithmetic operators
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Slicing / mutability Track which names point to the same object and which slice creates a copy before the mutation happens. Slicing / mutability
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Suppose you have a dictionary called characters, of which keys are strings and values are lists of strings. Check whether the method mutates the list in place and what the list looks like after each call. Exam • trial_m…
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Assume you already have a variable a, which is an integer between 1 and 4. Exam • midterm_2023 • Q15 mylist = [1, 3, 5, 7, 9] print(mylist[a] + mylist[-a])
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Condition flow and branch result Exam • midterm_2024 • Q1 Consider the following code snippet: a = True b = False c = True d = False if not (a or b) and (c or d): print("True") else: print("False") What will be printed…
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Mutable default argument Check whether the method mutates the list in place and what the list looks like after each call. Mutable default argument
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: You have four different blocks of code. Three of them return the same list, one of them returns something different. Apply the lambda/function to one element first, then extend that same transformation to the rest of th…
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Given s1 = 'abcd', which code fragment correctly updates s1 to 'Abcd'? Strings are immutable. s1.capitalize() returns a new string, so you must assign that result back to the name s1. String Methods
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do you include literal curly braces {} in an f-string? In f-strings, curly braces are escaped by doubling them ({{ and }}). F-strings
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: RuntimeError: dictionary changed size during iteration Adding or deleting dict entries while iterating over it causes RuntimeError
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What happens if you run print(df.iloc[5, 2]) on a DataFrame with only 3 rows? Unlike slicing, accessing a specific single position with .iloc that is out of bounds raises an IndexError. Selection with iloc
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Given s = pd.Series(['abc', 'xAef']), what is the result of s.str.upper().str.count('A').mean()? Upper becomes ['ABC', 'XAEF']. 'A' appears once in each, so counts are [1, 1]. The mean of [1, 1] is 1.0. Vectorized Opera…
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: During a .merge(how='left') operation, what is placed in a cell if no match is found in the right DataFrame? Pandas uses NaN (Not a Number) to represent missing data resulting from non-overlapping joins. Merging
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Why does Python interpret {x * 2 for x in l1} as a set comprehension and not a dictionary comprehension? Dictionary comprehensions require a 'key: value' syntax within the curly braces. Comprehensions
- `aiq-1`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What is the primary advantage of a generator over a list for large datasets? Generators do not store the entire sequence in memory, which is essential for very large or infinite datasets. Generators

### Objects and Names

- Snippet ID: `item:aiq-2`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `12`

- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Why does the following code work even though strings are immutable? Decide whether the code is rebinding a name or mutating a shared mutable object. Immutability/names
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Boolean operator precedence: not > and > or a==1 or a==2 and b==1 or b==2 is evaluated as a==1 or (a==2 and b==1) or b==2
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Slicing negative step Read the slice as `start:stop:step`; with a negative step Python walks right-to-left and still excludes the stop position. Slicing negative step
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Which update makes `library['books'] = 6` and adds `library['years']`? Check whether membership is testing keys, and trace any lookup or mutation on the dictionary. Exam • trial_midterm • Q8
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: List method effects and resulting list Check whether the method mutates the list in place and what the list looks like after each call. Exam • midterm_2023 • Q16 Consider the following code snippet: mylist = [1, 3, 2, 3…
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: def multiply(num1, num2): multiply() has no return statement, so it returns None. print(multiply(2,3)) prints None. But inside, global result is set to 6. print(result) prints 6. Output: None, 6. Exam • extra_practice •…
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Mutable arguments Mutating a passed list changes the caller's object; rebinding the parameter does not. Mutable arguments
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: You need to write a function called sort_list that accepts a list of integers. Check whether the method mutates the list in place and what the list looks like after each call. Exam • midterm_2023 • Q11 For example: If w…
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What does the slice s[::-2] do for the string s = 'abcdef'? The step -2 reverses the string and skips every second character, starting from the end ('f', then 'd', then 'b'). String Slicing
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: If df.A has 3 elements, which operation will raise a ValueError? When broadcasting a collection to a Series, the shapes must match. (3,) and (2,) cannot be broadcast together. Broadcasting Errors
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What is the result of {int(x) * 2 for x in '01212' if x in '02'}? Sets only store unique values. 0*2=0 and 2*2=4. Repeated values are ignored. Comprehensions
- `aiq-2`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: map/filter return iterables, not lists list(map(lambda x: x*2, l)) — must wrap in list(). Without it: <map object at 0x...>

### Objects and Names

- Snippet ID: `item:aiq-3`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `9`

- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Assume you already have a variable called x, which contains a list of integers. Expand `range(start, stop, step)` manually; `stop` is excluded and the next value is found by adding `step` each time. Exam • trial_midterm…
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] a: starts at -1 (10), step -2: [10,8,6,4,2]. Correct. b: [::-2] starts at last (10), step -2: [10,8,6,4,2]. Correct. c: [::-1] reverses to [10,9,8,7,6,5,4,3,2,1], then [::2] tak…
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What does `list(x.values()) + list(x.keys())` print? Check whether membership is testing keys, and trace any lookup or mutation on the dictionary. Exam • trial_midterm • Q10 Suppose you have the following dictionary: x…
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: list Exam • midterm_2024 • Q22 Consider the following code snippet: x = ["a", "b", "c", "4"] print(x[-3] + x[3]*3) Which of the following code snippet will print the same output?
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Assume sum_even_in_list(l1) filters non-integers and sums even integers. a: *args creates a tuple, sum_even_in_list accepts any iterable so passing a tuple works. b: list comprehension on tuple works fine. c: direct ite…
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Suppose you have the following function: Trace the returned value, not just what gets printed while the function runs. Exam • midterm_2023 • Q9 Suppose you have the following function: def add_numbers(num1, num2 = 10, n…
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Suppose you have the following functions, one to elevates a number to square and the second elevates to cube: Apply the lambda/function to one element first, then extend that same transformation to the rest of the Serie…
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: map/filter return iterables, not lists list(map(lambda x: x*2, l)) — must wrap in list(). Without it: <map object at 0x...>
- `aiq-3`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Slicing creates a NEW object l2=l1 vs l2=l1[:] — l2=l1 shares the SAME object, slicing creates independent copy

### Objects and Names

- Snippet ID: `item:aiq-4`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `6`

- `aiq-4`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Suppose you have the following function: Trace the returned value, not just what gets printed while the function runs. Exam • trial_midterm • Q3 Suppose you have the following function: def multiply(*args, factor=2): to…
- `aiq-4`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Unordered collections equality {1:1,2:2}=={2:2,1:1} is True; {1,2}=={2,1} is True; [1,2]==[2,1] is False
- `aiq-4`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Implicit return None Function without return statement, or where return is not reached, returns None. print(func()) will print None.
- `aiq-4`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: You need to write a function called print_info which takes two required arguments called name and age, and a flexible number of keyword Check whether the method mutates the list in place and what the list looks like aft…
- `aiq-4`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: 1 + True = 2 (bool is subclass of int) True==1, False==0 in numeric contexts. type(True)==int is False but isinstance(True,int) is True
- `aiq-4`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Mutable default argument def f(lst=[]): — the [] is created ONCE at def time and persists across calls. Fix: use None and create inside function

### Objects and Names

- Snippet ID: `item:aiq-5`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `7`

- `aiq-5`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Assume you have the following variables: Decide whether the code is rebinding a name or mutating a shared mutable object. Exam • trial_midterm • Q4 Assume you have the following variables: x = 3 y = 3.0 z = '3' What wil…
- `aiq-5`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: str.upper() / string methods don't modify in place s.upper() returns a new string; s is unchanged. Must do s = s.upper()
- `aiq-5`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Single-element tuple needs trailing comma (1) is int, not tuple. (1,) or 1, is a tuple
- `aiq-5`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: You have to write a function called summarize which take a list of integers as an argument. Return `{'amount': len(nums), 'smallest': min(nums), 'largest': max(nums), 'total': sum(nums)}`. Exam • midterm_2024 • Q13 The…
- `aiq-5`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: map/filter return iterables, not lists list(map(lambda x: x*2, l)) — must wrap in list(). Without it: <map object at 0x...>
- `aiq-5`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Slicing creates a NEW object l2=l1 vs l2=l1[:] — l2=l1 shares the SAME object, slicing creates independent copy
- `aiq-5`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: UnboundLocalError If a name appears on the left side of assignment ANYWHERE in a function, Python treats it as local THROUGHOUT the function body — even before the assignment line

### Objects and Names

- Snippet ID: `item:aiq-6`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `5`

- `aiq-6`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Slicing creates a NEW object l2=l1 vs l2=l1[:] — l2=l1 shares the SAME object, slicing creates independent copy
- `aiq-6`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: range() and slicing both exclusive at stop range(1,10,3)→[1,4,7] not including 10; l[2:7] goes up to but not including index 7
- `aiq-6`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: RuntimeError: dictionary changed size during iteration Adding or deleting dict entries while iterating over it causes RuntimeError
- `aiq-6`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Mutable default argument def f(lst=[]): — the [] is created ONCE at def time and persists across calls. Fix: use None and create inside function
- `aiq-6`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: range() and slicing both exclusive at stop range(1,10,3)→[1,4,7] not including 10; l[2:7] goes up to but not including index 7

### Objects and Names

- Snippet ID: `item:aiq-7`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `2`

- `aiq-7`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Mutable default argument def f(lst=[]): — the [] is created ONCE at def time and persists across calls. Fix: use None and create inside function
- `aiq-7`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Mutable parameter sharing When mutable object passed as argument, parameter and argument point to SAME object — mutations inside function affect original

### Objects and Names

- Snippet ID: `item:exam-Test Resit - Introduction to Python - 22/23-3-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-Test Resit - Introduction to Python - 22/23-3-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What will be printed by the following code segment? a b c d b The type of x is a list. The loop checks if the type of each element is equal to the type of x. The only element in x that is a list is the empty list `[]`.…

### Objects and Names

- Snippet ID: `item:exam-Trial final - Introduction to Python - 22/23-1-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-Trial final - Introduction to Python - 22/23-1-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you already have: (i) a list of strings called europe which contain the names of all European countries, and (ii) a string variable called destination. You want to write a program to advice Dutch residents on th…

### Objects and Names

- Snippet ID: `item:exam-Trial final exam Introduction to Python-3-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-Trial final exam Introduction to Python-3-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Imagine that you have a list called students, which is populated by a number of dictionaries. Each dictionary in the students list has two keys: "Name" and "Grade". The corresponding values are student names (as strings…

### Objects and Names

- Snippet ID: `item:exam-extra_practice-11-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-extra_practice-11-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: x = ['abc', [[]], (1, 2), {}, True, 3.0, 4] What is the output of the following code snippet? print(type(float(x[2][0] + x[2][1])) == type(x[-2])) a b c d d x[2] = (1,2). x[2][0]=1, x[2][1]=2. 1+2=3. float(3)=3.0. type(…

### Objects and Names

- Snippet ID: `item:exam-intro_python_sample_final_24_25-13-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-13-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What are the outputs of the following lines of code? print(x == y), print(y == z), print(x == z), print(x == y == z) A B C D A '3' == 3 is False. 3 == 3.0 is True. '3' == 3.0 is False. x == y == z evaluates as (x == y)…

### Objects and Names

- Snippet ID: `item:exam-midterm_2023-4-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-midterm_2023-4-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Assume you have the following variables: x = 'abc' y = 3 z = 2.0 What will be printed after these lines of code? print(x*y) print(x*z) print(y*z) A 'abcabcabc' The code will result in a TypeError because you can't multi…

### Objects and Names

- Snippet ID: `item:exam-midterm_2024-4-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-midterm_2024-4-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Consider the following code snippet: a = 1 b = 2.0 c = '3' d = 'hello' y = {} for i in [0,1]: if i==0: if type(a)==type(b): y[i] = True else: y[i] = False if i==1: if type(c)==type(d): y[i] = True else: y[i] = False pri…

### Objects and Names

- Snippet ID: `item:exam-midterm_2024-6-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-midterm_2024-6-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Consider the following code snippet: x = 10 y = '5' z = x + y ​What will be the value of 'z' and why? A The value of z will be 15 because the string '5' will be implicitly converted to an integer. B The value of z will…

### Objects and Names

- Snippet ID: `item:exam-trial-final-exam-py22-1-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial-final-exam-py22-1-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have a variable called x which contains an integer between 0 and 10 (both are inclusive). Which of the following programs will tell you whether x contains an odd or even number? a b c d d All three programs…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-1-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-1-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Assume you already have a variable called x, which contains a list of integers. Which of the following programs will print you a list of the squared values of the elements in x?

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-11-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-11-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Consider the following code snippet: x = 10 y = '5' z = x + y ​What will be the value of 'z' and why? A The code will result in a None because 'x' and 'y' have different types. B The code will result in an error because…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-12-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-12-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Which other program will produce the same output as the following code snippet?

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-14-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-14-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Consider the following code snippet: a = 1 b = 2.0 c = '3' d = 'hello' y = {} for i in [0,1]: if i==0: if type(a)==type(b): y[i] = True else: y[i] = False if i==1: if type(c)==type(d): y[i] = True else: y[i] = False pri…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-15-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-15-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following function count_characters, which takes two arguments: a list of strings which are names, and an optional keyword argument called character that has a default value of 'a'. def count_charac…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-16-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-16-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: What is the output of the program below?

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-18-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-18-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following function which take a list of numerical strings as an argument.

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-20-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-20-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: You have the following list: my_list = [1,2,3,4] Which one of the following lines of code lines does not print 4 as the output? A print(my_list[4]) B print(my_list[-1]) C print(max(my_list)) D print(len(my_list))

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-21-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-21-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Consider the following code snippet: x = ["a", "b", "c", "4"] print(x[-3] + x[3]*3) Which of the following code snippet will print the same output? A y = [1, 2, 3, 4] print('b'+ max(y)*3) B print('b' + str(len(x)*3)) C…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-22-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-22-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following a dictionary called students, which contains three sub-dictionaries: students = {"james": {"name": "James", "homework": [90.0, 97.0, 75.0, 92.0], "quizzes": [88.0, 40.0, 94.0], "tests": [7…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-24-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-24-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Consider the following code snippet: a = True b = False c = True d = False if not (a or b) and (c or d): print("True") else: print("False") What will be printed by the code? A The code will result in an error. B True C…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-3-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-3-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following function: def multiply(*args, factor=2): total = 1 for num in args: total *= num return total * factor Which of the following functions will return the same values as the function above, i…

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-4-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-4-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Assume you have the following variables: x = 3 y = 3.0 z = '3' What will be printed by the following code: print((x != z and x == int(z)) or (x != y and y != z)) A 3 B The code will result in an error. C False D True

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-7-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-7-w1-objects-and-names`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called dict_keys that checks whether a certain key is in available in a certain dictionary.

### Objects and Names

- Snippet ID: `item:exam-trial_midterm-9-w1-objects-and-names`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `exam-trial_midterm-9-w1-objects-and-names`
  Bucket: `additional` | Type: `source_exam`
  Preview: Consider the following code snippet: mylist = [1, 2, 5, 7, 9, 12] new_list1 = mylist[0:3] new_list2 = mylist[1:4] print(new_list1 + new_list2) What will be printed? A [1, 2, 5, 7, 2, 5, 7, 9] B [1, 2, 5, 2, 5, 7] C [2,…

### Objects and Names

- Snippet ID: `item:kp-2-d1`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `20`

- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: List is mutable — can change element in place l1 = [1, 2, 3] print(l1) # [1, 2, 3] l1[2] = 4 print(l1) # [1, 2, 4]
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Float precision issue print(1.1 + 2.2 == 3.3) # False
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: range examples print(list(range(6))) # [0, 1, 2, 3, 4, 5] print(list(range(3,6))) # [3, 4, 5] print(list(range(3,6,2))) # [3, 5]
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Looping over dict capitals = {'Andorra': 'Andorra la Vella', 'Belgium': 'Brussels'} for key in capitals.keys(): print(key) for val in capitals.values(): print(val) for key, value in capitals.items(): print(key, value) #…
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Set operations countries = set() # empty set (NOT {}) countries = {'Andorra', 'Belgium'} print({1,2,2} == {2,1}) # True (duplicates ignored) print(len({1,2,2})) # 2 countries.remove('Andorra') countries.add('Greece') co…
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Explicit conversions print(str(1) == '1') # True print(int('1') == 1) # True print(int('1a')) # ERROR print(float('1') == 1.0) # True print(float('1.0') == 1.0) # True print(tuple([1,2,3]) == (1,2,3)) # True print(tuple…
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Method on immutable — must capture return value s1 = 'UVA Amsterdam' s1 = s1.upper() # CORRECT — captures new string s1.upper() # WRONG — result is lost, s1 unchanged
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Implicit None return def adder(n1, n2): if type(n1) == type(n2) == int: total = n1 + n2 return total a = adder('1', 2) # Returns None (no return hit) print(a) # None
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Keyword arguments def calc(first, second, third, fourth, fifth, sixth): return first + 2*second + 3*third + 4*fourth + 5*fifth + 6*sixth print(calc(fifth=2, third=4, fourth=1, sixth=5, second=2, first=3)) # 63
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Lambda basics add_two = lambda x, y: x + y print(add_two(1, 2)) # 3 # Equivalent to: def add_two(x, y): return x + y
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Newlines and tabs print('Line 1\nLine 2\tTabbed') print("It\'s a string")
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Slicing examples s = '01234567' print(s[::4]) # '04' print(s[::-2]) # '7531'
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Debug shortcut val = 10 print(f'{val=}') # 'val=10'
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Using self to access attributes class Dog: def __init__(self, name): self.name = name def bark(self): return f'{self.name} says woof!'
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Raising an error def check_positive(n): if n < 0: raise ValueError('Number must be positive') return n
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Select rows/cols by name df.loc['First':'Third', ['Name', 'Weight']]
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Scalar broadcasting df['Height'] += 10 # Adds 10 to every cell in the column
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Left join on a key df1.merge(df2, on='Town', how='left')
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Double vowels in a string s2 = ''.join([x*2 if x.lower() in 'aeiou' else x for x in 'Python'])
- `kp-2-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Manual iteration it = iter([1, 2]); print(next(it)); print(next(it))

### Objects and Names

- Snippet ID: `item:kp-2-d2`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `7`

- `kp-2-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Tuple is immutable — assigning to index raises TypeError t1 = (1, 2, 3) t1[2] = 4 # TypeError: 'tuple' object does not support item assignment
- `kp-2-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: List/tuple comparison print([1, 2, 3] < [1, 2, 3, 0]) # True (shorter is less) print([2] < [1, 2, 3, 0]) # False (2 > 1 at index 0)
- `kp-2-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Iteration and ordering reminders Pattern | Iterates over | Trap for key in d | keys | same as for key in d.keys() for value in d.values() | values | no keys available unless you ask for them for key, value in d.items()…
- `kp-2-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Implicit conversion (Python allows with bool/numeric mix) print(1 + True) # 2 print(1.0 + False) # 1.0 print('1' * 2) # '11' print('1' * True) # '1' print('1' * False) # ''
- `kp-2-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Method on mutable — changes in place vs returns value l1 = [3, 1, 2] l1.sort() # changes l1 in place, returns None print(l1) # [1, 2, 3] print(l1.index(2)) # 1 (returns index, doesn't change l1)
- `kp-2-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: **kwargs def calc(**kwargs): return kwargs['first'] + 2*kwargs['second'] + 3*kwargs['third'] print(calc(third=4, second=2, first=3))
- `kp-2-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: map() with lambda l1 = [1, 2, 3, 4, 5, 6] print(list(map(lambda x: x * 2, l1))) # [2, 4, 6, 8, 10, 12] # Need list() to convert map object to list

### Objects and Names

- Snippet ID: `item:kp-3-d1`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `13`

- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Basic assignment name_1 = 300 print(name_1) # 300 print(type(name_1)) # <class 'int'> print(id(name_1)) # some unique integer
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Precedence trap a=1; b=3 print(a==1 or a==2 and b==1 or b==2) # True (WRONG: and binds tighter) print((a==1 or a==2) and (b==1 or b==2)) # False (CORRECT)
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: 1-element tuple gotcha t1 = (1) print(type(t1) == tuple) # False print(type(t1) == int) # True t1 = (1,) # correct 1-element tuple t1 = 1, # also correct x, y = y, x # swap using tuple unpacking
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Default value def multiplier(first, second=2): return first * second print(multiplier(3)) # 6 (uses default second=2) print(multiplier(3, 3)) # 9 print(multiplier(2, second=3)) # 6
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Compact lambda / map reference Pattern | Meaning lambda x: x * 2 | inline function for one value map(f, seq) | apply `f` to each element lazily list(map(f, seq)) | materialize the mapped results for display
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Joining a list into a string words = ['a', 'b', 'c'] print('-'.join(words)) # 'a-b-c' print(''.join(words)) # 'abc'
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Zero-padding an integer num = 7 print(f'{num:03d}') # '007'
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Shared class attribute class Counter: count = 0 def __init__(self): Counter.count += 1
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Specific exception handler s1 = 'abcdefghabcdefgh' needle = 'i' try: position = s1.index(needle) except ValueError: position = -1 print(position)
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Select by position df.iloc[0:2, 0:1] # Rows 0,1; Col 0
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Chained string operations s.str.upper().str.count('A')
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Grouped aggregation df.groupby('Nationality')['Height'].median()
- `kp-3-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dictionary with sub-dictionaries result = {x: {y: x + y for y in range(x, 4)} for x in range(1, 4)}

### Objects and Names

- Snippet ID: `item:kp-3-d2`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `2`

- `kp-3-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Two names bound to the same object (same id) name_3 = name_4 = name_5 = name_6 = 300 print(name_3 is name_4 is name_5 is name_6) # True
- `kp-3-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Mutable default BUG def main(addition, l1=[]): l1.append(addition) return l1 print(main(2)) # [2] print(main(3)) # [2, 3] ← BUG: l1 persists!

### Objects and Names

- Snippet ID: `item:kp-4-d1`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `7`

- `kp-4-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: All 8 types var_1 = 123 # int var_2 = 123.3 # float var_3 = '123' # str var_4 = True # bool var_5 = ('123', 123) # tuple var_6 = [123, '123'] # list var_7 = {'k1': 'v1'} # dict var_8 = {123, '123'} # set
- `kp-4-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: pass as stub def adder(n1, n2): if type(n1) == int and type(n2) == int: result = n1 + n2 else: pass # placeholder — won't cause IndentationError return result
- `kp-4-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Limiting replacements s = 'aaaa' print(s.replace('a', 'b', 2)) # 'bbaa'
- `kp-4-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Padding with `.format(...)` score = 91 print('Score: {:04d}'.format(score))
- `kp-4-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Series vs DataFrame result type(df.loc[2]) # Series type(df.loc[[2]]) # DataFrame
- `kp-4-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Filtering with isin vowels = list('aeiou') s[s.str[-1].str.lower().isin(vowels)]
- `kp-4-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Using walrus to avoid double squaring l1 = [(x, r) for x in range(1, 10) if 20 > (r := x**2) > 10]

### Objects and Names

- Snippet ID: `item:kp-6-d1`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `5`

- `kp-6-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Basic slicing examples l1 = [1, 2, 3, 4, 5, 6, 7, 8] print(l1[7]) # 8 print(l1[-1]) # 8 print(l1[-5:5]) # [4, 5] print(l1[:-5]) # [1, 2, 3]
- `kp-6-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Stripping whitespace and characters s = ' abc ' print(s.strip()) # 'abc' s2 = 'eeabcdee' print(s2.strip('e')) # 'abcd'
- `kp-6-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Valid vs invalid Pandas selection Code | Valid? | Meaning df.loc[2:4, ['B']] | yes | label-based rows + columns df.iloc[1:4, [1]] | yes | position-based rows + columns df.loc[df['A'] > 0, ['B', 'C']] | yes | boolean-mas…
- `kp-6-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Row-wise average df['Avg'] = df.apply(lambda x: x.mean(), axis=1)
- `kp-6-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Generator for large range gen = (x for x in range(1000000) if x % 3 == 0)

### Objects and Names

- Snippet ID: `item:kp-6-d2`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `3`

- `kp-6-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Negative step l1 = [1, 2, 3, 4, 5, 6, 7, 8] print(l1[5:1:-2]) # [6, 4] print(l1[5::-1]) # [6, 5, 4, 3, 2, 1] print(l1[:1:-1]) # [8, 7, 6, 5, 4, 3] print(l1[1:5:-2]) # [] (already past end)
- `kp-6-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Even-index row pattern df.loc[df.index % 2 == 0, ['B']]
- `kp-6-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Columnwise mean df.loc['Av'] = df.apply(lambda col: col.mean(), axis=0)

### Objects and Names

- Snippet ID: `item:kp-7-d1`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `3`

- `kp-7-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Simple function def size(length, width): return length * width print(size(2,3)) # 6
- `kp-7-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Handling NaNs df.fillna('No value') # Replaces all NaNs
- `kp-7-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Filtering dictionary items d = {k: v for k, v in {'a': 1, 'b': 2}.items() if v > 1}

### Objects and Names

- Snippet ID: `item:kp-manual-aliasing-copy-d1`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `kp-manual-aliasing-copy-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Aliasing vs slicing copy l1 = [1, 2, 3] l2 = l1 l3 = l1[:] l1[0] = 99 print(l2) # [99, 2, 3] print(l3) # [1, 2, 3]

### Objects and Names

- Snippet ID: `item:ks-0153de2f70`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-0153de2f70`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Functions — basics Functions are objects. Defined with def. Called with (). Built-in functions: print, id, len, type, del. Functions can return values. Methods are functions attached to objects. Simple function def size…

### Objects and Names

- Snippet ID: `item:ks-419e787b39`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-419e787b39`
  Bucket: `additional` | Type: `source_lecture`
  Preview: objects ### Everything in Python is an object. Objects in Python have one id, one value, one type, and zero or more names <br>An assignment statement is one of the ways to create an object. An object created with an ass…

### Objects and Names

- Snippet ID: `item:ks-61c5deec4a`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-61c5deec4a`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Assignment statements — reading right to left Python creates a new object with the value on the right, infers type from the value, then binds the name on the left to that object. Basic assignment name_1 = 300 print(name…

### Objects and Names

- Snippet ID: `item:ks-6f41148083`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-6f41148083`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Slicing Syntax: seq[start:end:step]. Start is inclusive, end is NOT inclusive. Defaults: start=0, end=len, step=1. Negative step goes from right to left. Slicing always creates a NEW object of the same type. Basic slici…

### Objects and Names

- Snippet ID: `item:ks-cb3a9e3fd2`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-cb3a9e3fd2`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Object types — the 8 types to know int, float, str, bool, tuple, list, dict, set All 8 types var_1 = 123 # int var_2 = 123.3 # float var_3 = '123' # str var_4 = True # bool var_5 = ('123', 123) # tuple var_6 = [123, '12…

### Objects and Names

- Snippet ID: `item:ks-d79a1899f6`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-d79a1899f6`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Names / variable naming rules Names can consist of letters (upper/lower), digits, and underscores. Names CANNOT start with a digit. Names ARE case-sensitive (name_1 != Name_1). Avoid Python reserved words (e.g., don't n…

### Objects and Names

- Snippet ID: `item:ks-df3b849d59`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-df3b849d59`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Exam question types Which code fragment will print the following output? / What will be printed by the following code fragment? / Which code fragment prints the SAME output as...? / One fragment prints different output…

### Objects and Names

- Snippet ID: `item:ks-e88d0a8060`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-e88d0a8060`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Objects: core properties Every object has exactly one unique id (cannot change), exactly one type (cannot change), and exactly one value. The type defines what value can be stored and whether the value is mutable or imm…

### Objects and Names

- Snippet ID: `item:ks-eae9bf47dd`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `1`

- `ks-eae9bf47dd`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Mutable vs immutable types Immutable: int, float, str, bool, tuple. Mutable: list, dict, set. The value of a mutable object CAN be changed in-place. The value of an immutable object CANNOT be changed — a new object must…

### Objects, Types, Mutability, Assignment, and Names

- Snippet ID: `subtopic:w1-objects-and-names:w1-objects-and-names-core`
- Topic: Objects and Names
- Card ID: `w1-objects-and-names`
- Piece count: `19`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: List is mutable — can change element in place l1 = [1, 2, 3] print(l1) # [1, 2, 3] l1[2] = 4 print(l1) # [1, 2, 4] Immutable types like `int`, `float`, `str`, and `tuple` cannot change in place. Mutable types like `list…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Tuple is immutable — assigning to index raises TypeError t1 = (1, 2, 3) t1[2] = 4 # TypeError: 'tuple' object does not support item assignment Immutable types like `int`, `float`, `str`, and `tuple` cannot change in pla…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Basic assignment name_1 = 300 print(name_1) # 300 print(type(name_1)) # <class 'int'> print(id(name_1)) # some unique integer Assignment binds the left-hand name to the object produced on the right-hand side.
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Two names bound to the same object (same id) name_3 = name_4 = name_5 = name_6 = 300 print(name_3 is name_4 is name_5 is name_6) # True Assignment binds the left-hand name to the object produced on the right-hand side.
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: All 8 types var_1 = 123 # int var_2 = 123.3 # float var_3 = '123' # str var_4 = True # bool var_5 = ('123', 123) # tuple var_6 = [123, '123'] # list var_7 = {'k1': 'v1'} # dict var_8 = {123, '123'} # set Core built-in t…
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Basic slicing examples l1 = [1, 2, 3, 4, 5, 6, 7, 8] print(l1[7]) # 8 print(l1[-1]) # 8 print(l1[-5:5]) # [4, 5] print(l1[:-5]) # [1, 2, 3] Syntax: seq[start:end:step]. Start is inclusive, end is NOT inclusive. Defaults…
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Negative step l1 = [1, 2, 3, 4, 5, 6, 7, 8] print(l1[5:1:-2]) # [6, 4] print(l1[5::-1]) # [6, 5, 4, 3, 2, 1] print(l1[:1:-1]) # [8, 7, 6, 5, 4, 3] print(l1[1:5:-2]) # [] (already past end) Syntax: seq[start:end:step]. S…
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Simple function def size(length, width): return length * width print(size(2,3)) # 6 Functions are objects. Defined with def. Called with (). Built-in functions: print, id, len, type, del. Functions can return values. Me…
- `manual-objects-aliasing`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Aliasing vs slicing copy l1 = [1, 2, 3] l2 = l1 l3 = l1[:] l1[0] = 99 print(l2) # [99, 2, 3] print(l3) # [1, 2, 3] For mutable objects, `l2 = l1` aliases the same object; use slicing like `l1[:]` when you need an indepe…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Each object has identity, type, and value. Names bind to objects; rebinding changes the name, while in-place changes only affect mutable objects.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Immutable types like `int`, `float`, `str`, and `tuple` cannot change in place. Mutable types like `list`, `dict`, and `set` can be changed through the same object.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Assignment binds the left-hand name to the object produced on the right-hand side.
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Core built-in types: `int`, `float`, `str`, `bool`, `tuple`, `list`, `dict`, `set`.
- `kp-5`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Names can consist of letters (upper/lower), digits, and underscores. Names CANNOT start with a digit. Names ARE case-sensitive (name_1 != Name_1). Avoid Python reserved words (e.g., don't name a variable 'sorted', 'list…
- `kp-6`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Syntax: seq[start:end:step]. Start is inclusive, end is NOT inclusive. Defaults: start=0, end=len, step=1. Negative step goes from right to left. Slicing always creates a NEW object of the same type.
- `kp-7`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Functions are objects. Defined with def. Called with (). Built-in functions: print, id, len, type, del. Functions can return values. Methods are functions attached to objects.
- `kp-8`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Which code fragment will print the following output? / What will be printed by the following code fragment? / Which code fragment prints the SAME output as...? / One fragment prints different output from the others.
- `kp-9`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: Everything in Python is an object. Objects in Python have one id, one value, one type, and zero or more names An assignment statement is one of the ways to create an object. An object created with an assignment statemen…
- `kp-manual-aliasing-copy`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Objects, Types, Mutability, Assignment, and Names
  Preview: For mutable objects, `l2 = l1` aliases the same object; use slicing like `l1[:]` when you need an independent copy.

### Arithmetic, Comparison, and Boolean Operators

- Snippet ID: `subtopic:w1-operators-and-truth:w1-operators-and-truth-core`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `11`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: Floor division and modulo print(5 // 3, 5 % 3) # 1 2 print(-5 // 3, -5 % 3) # -2 1 print(5 // 2, 5 % 2) # 2 1 print(-5 // 2, -5 % 2) # -3 1 a+b, a-b, a*b: standard. a/b: always returns float. a//b: floor division (highe…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: Float precision issue print(1.1 + 2.2 == 3.3) # False ==, !=, >, <, >=, <=. Always return True or False. Comparing floats can be tricky: 1.1+2.2 != 3.3 in Python due to floating-point precision. String/tuple/list compar…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: List/tuple comparison print([1, 2, 3] < [1, 2, 3, 0]) # True (shorter is less) print([2] < [1, 2, 3, 0]) # False (2 > 1 at index 0) ==, !=, >, <, >=, <=. Always return True or False. Comparing floats can be tricky: 1.1+…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: Precedence trap a=1; b=3 print(a==1 or a==2 and b==1 or b==2) # True (WRONG: and binds tighter) print((a==1 or a==2) and (b==1 or b==2)) # False (CORRECT) x and y: True only if both True. x or y: False only if both Fals…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: arithmetic_operators print(5//2, 5%2) 2 1
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: arithmetic_operators print(4 + 3) print(4 - 3) print(4 * 3) print(4 / 3) print(4 / 2) print(4 ** 3) 7 1 12 1.3333333333333333 2.0 64
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: arithmetic_operators print(5 // 3, 5 % 3) print(-5 // 3, -5 % 3) print(5 // 2, 5 % 2) print(-5 // 2, -5 % 2) 1 2 -2 1 2 1 -3 1
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: `==` versus `is` # import random # The random module that can be used to generate pseudo-random numbers is part of the standard Python installation # but the name has still to be importent a = random.randint(3, 9) # Thi…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: a+b, a-b, a*b: standard. a/b: always returns float. a//b: floor division (highest integer <= result). a%b: remainder. a**b: exponentiation. NOTE: ^ is NOT exponentiation in Python (it is XOR). (a//b)*b + a%b == a always.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: ==, !=, >, <, >=, <=. Always return True or False. Comparing floats can be tricky: 1.1+2.2 != 3.3 in Python due to floating-point precision. String/tuple/list comparison is element-by-element left to right; first differ…
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Arithmetic, Comparison, and Boolean Operators
  Preview: x and y: True only if both True. x or y: False only if both False. not x: inverts. NOTE: && and || are Python operators but do something different (bitwise). Precedence: 'not' first, then 'and', then 'or'. Use parenthes…

### Operators and Truth

- Snippet ID: `item:cs-266616a010`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `1`

- `cs-266616a010`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: arithmetic_operators print(5 // 3, 5 % 3) print(-5 // 3, -5 % 3) print(5 // 2, 5 % 2) print(-5 // 2, -5 % 2) 1 2 -2 1 2 1 -3 1

### Operators and Truth

- Snippet ID: `item:cs-3cb4b8e8f9`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `1`

- `cs-3cb4b8e8f9`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: arithmetic_operators print(4 + 3) print(4 - 3) print(4 * 3) print(4 / 3) print(4 / 2) print(4 ** 3) 7 1 12 1.3333333333333333 2.0 64

### Operators and Truth

- Snippet ID: `item:cs-4f8a5f420b`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `1`

- `cs-4f8a5f420b`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: arithmetic_operators # import random # The random module that can be used to generate pseudo-random numbers is part of the standard Python installation # but the name has still to be importent a = random.randint(3, 9) #…

### Operators and Truth

- Snippet ID: `item:cs-7eb8617d28`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `1`

- `cs-7eb8617d28`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: arithmetic_operators print(5//2, 5%2) 2 1

### Operators and Truth

- Snippet ID: `item:kp-1-d1`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `20`

- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Floor division and modulo print(5 // 3, 5 % 3) # 1 2 print(-5 // 3, -5 % 3) # -2 1 print(5 // 2, 5 % 2) # 2 1 print(-5 // 2, -5 % 2) # -3 1
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Pattern | Meaning | Example seq[i] | single element | x[-1] seq[a:b] | start inclusive, stop exclusive | x[1:4] seq[::-1] | reverse copy | x[::-1] seq[::2] | step through every other item | x[::2]
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Import styles import numpy numpy.random.randint(1, 10) # works import numpy as np np.random.randint(1, 10) # works numpy.random.randint(1, 10) # ERROR from numpy.random import randint randint(1, 10) # works from numpy.r…
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Creating and using dicts capitals = {} capitals = dict() capitals = {'Andorra': 'Andorra la Vella', 'Belgium': 'Brussels'} print(capitals['Belgium']) # Brussels del(capitals['Belgium']) # delete key capitals['Netherland…
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Ordering comparison print([1,2] == [2,1]) # False (ordered) print((1,2) == (2,1)) # False (ordered) print('12' == '21') # False (ordered) print({1,2} == {2,1}) # True (unordered) print({1:1,2:2}=={2:2,1:1}) # True (unor…
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Falsy values # All evaluate to False in a condition: [] # empty list () # empty tuple {} # empty dict set() # empty set '' # empty string 0 # zero int 0.0 # zero float
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Basic function def adder(n1, n2): total = n1 + n2 return total a = adder(1, 2) print(a) # 3
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Returning a tuple (multiple values) def powers(n1): return n1 ** 2, n1 ** 3 # returns a tuple power2, power3 = powers(3) print(power2, power3) # 9 27
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: *args usage def adder(*args): result = 0 for number in args: result += number return result print(adder(1, 2, 3, 4, 5)) # 15
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Function factory def function_factory(increment): def adder(n1): return n1 + increment return adder add4 = function_factory(4) add5 = function_factory(5) print(add4(3)) # 7 print(add5(3)) # 8
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Attempting to change a string s1 = 'abcd' s1.capitalize() # Returns 'Abcd' print(s1) # Still prints 'abcd'
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Behavior when substring is missing s = 'abc' print(s.find('z')) # -1 # print(s.index('z')) # Raises ValueError
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Simple f-string name = 'Jan' print(f'{name} studies Python.') # 'Jan studies Python.'
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Defining a simple class class Car: def __init__(self, color): self.color = color
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Handling a ValueError s = 'abc' try: idx = s.index('z') except ValueError: idx = -1
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Summary stats print(df.describe())
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Sorting by column values df.sort_values(by='Length', ascending=False)
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Vertical stack pd.concat([df1, df2], axis=0)
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Building a set of doubled odd numbers s1 = {x * 2 for x in [1, 3, 2, 5] if x % 2 != 0}
- `kp-1-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Simple step generator def count(start, stop, step): while start <= stop: yield start start += step

### Operators and Truth

- Snippet ID: `item:ks-03c874b8bb`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `1`

- `ks-03c874b8bb`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Arithmetic operators a+b, a-b, a*b: standard. a/b: always returns float. a//b: floor division (highest integer <= result). a%b: remainder. a**b: exponentiation. NOTE: ^ is NOT exponentiation in Python (it is XOR). (a//b…

### Operators and Truth

- Snippet ID: `item:ks-c0135e2a4a`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `1`

- `ks-c0135e2a4a`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Comparison operators ==, !=, >, <, >=, <=. Always return True or False. Comparing floats can be tricky: 1.1+2.2 != 3.3 in Python due to floating-point precision. String/tuple/list comparison is element-by-element left t…

### Operators and Truth

- Snippet ID: `item:ks-c815ffe1d5`
- Topic: Operators and Truth
- Card ID: `w1-operators-and-truth`
- Piece count: `1`

- `ks-c815ffe1d5`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Boolean operators x and y: True only if both True. x or y: False only if both False. not x: inverts. NOTE: && and || are Python operators but do something different (bitwise). Precedence: 'not' first, then 'and', then '…

### Execution Model, Logical Lines, and Comments

- Snippet ID: `subtopic:w1-python-basics:w1-python-basics-execution-model`
- Topic: Python Basics
- Card ID: `w1-python-basics`
- Piece count: `7`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Execution Model, Logical Lines, and Comments
  Preview: print('Hello World') # Everything after the hashtag is a comment print('Hello World') # Everything after the hashtag is a comment Hello World
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Execution Model, Logical Lines, and Comments
  Preview: print(_, __, ___) # print(_, __, ___)
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Execution Model, Logical Lines, and Comments
  Preview: print('Hello World') print('Hello World')
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Execution Model, Logical Lines, and Comments
  Preview: print(r"This gives no \" error") # print(r"This gives no \" error") print(r'This gives no \' error')
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Execution Model, Logical Lines, and Comments
  Preview: line_joining a = 'Two or more physical lines can be joined' +\ ' with the help of backward slashes' print(a)
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Execution Model, Logical Lines, and Comments
  Preview: line_joining a = ['Two or more physical lines can be joined', ' with the help of backward slashes'] print(a)
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Execution Model, Logical Lines, and Comments
  Preview: Python script is translated line by line into byte code, then byte code is translated into machine code. Writing code must be precise; ambiguities that humans handle fine will cause Python errors.

### Python Basics

- Snippet ID: `item:cs-09e2b215ee`
- Topic: Python Basics
- Card ID: `w1-python-basics`
- Piece count: `1`

- `cs-09e2b215ee`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: print('Hello World') # Everything after the hashtag is a comment print('Hello World') # Everything after the hashtag is a comment Hello World

### Python Basics

- Snippet ID: `item:cs-814a07a136`
- Topic: Python Basics
- Card ID: `w1-python-basics`
- Piece count: `1`

- `cs-814a07a136`
  Bucket: `additional` | Type: `source_notebook`
  Preview: 123*1 # 123*1

### Python Basics

- Snippet ID: `item:ks-95be7f9418`
- Topic: Python Basics
- Card ID: `w1-python-basics`
- Piece count: `1`

- `ks-95be7f9418`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Python execution model Python script is translated line by line into byte code, then byte code is translated into machine code. Writing code must be precise; ambiguities that humans handle fine will cause Python errors.

### Python Basics

- Snippet ID: `item:manual-comments`
- Topic: Python Basics
- Card ID: `w1-python-basics`
- Piece count: `1`

- `manual-comments`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do comments start, and what does Python ignore after `#`? Everything after `#` on that logical line is ignored by Python. x = 3 # this comment does not execute print(x)

### Python Basics

- Snippet ID: `item:manual-logical-lines`
- Topic: Python Basics
- Card ID: `w1-python-basics`
- Piece count: `1`

- `manual-logical-lines`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How can one logical line span multiple physical lines? Use open brackets or an explicit backslash to continue a statement across lines. numbers = [ 1, 2, 3, ]

### Indexing, Slicing, and range()

- Snippet ID: `subtopic:w1-sequences-and-access:w1-sequences-and-access-core`
- Topic: Sequences and Access
- Card ID: `w1-sequences-and-access`
- Piece count: `9`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Indexing, Slicing, and range()
  Preview: range() output patterns print(list(range(6))) # [0, 1, 2, 3, 4, 5] print(list(range(3,6))) # [3, 4, 5] print(list(range(3,6,2))) # [3, 5] `range(start, stop, step)` excludes `stop`; defaults are `start=0` and `step=1`,…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Indexing, Slicing, and range()
  Preview: print("This is a string") print("This is a string") print('This is another string')
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Indexing, Slicing, and range()
  Preview: String quotes and escaping print("This gives no ' error") print('This gives no " error')
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Indexing, Slicing, and range()
  Preview: a = 'This is a string' a = 'This is a string' b = "This is another string" print(a) print(b) print(a,b)
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Indexing, Slicing, and range()
  Preview: a = 'This is a string'; b = 6; c = 0.0 # a = 'This is a string'; b = 6; c = 0.0 print(f"We know {a =}, {b= }, and {c = }")
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Indexing, Slicing, and range()
  Preview: slicing l1 = ['a', 'b'] l2 = l1 l2[-1] = 'c' print(l1 == l3) l3 = l1[::] l3[-1] = 'c' print(l1 == l3)
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Indexing, Slicing, and range()
  Preview: Negative indices count from the end: `seq[-1]` is last and `seq[-len(seq)]` is first.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Indexing, Slicing, and range()
  Preview: `range(start, stop, step)` excludes `stop`; defaults are `start=0` and `step=1`, just like slicing excludes the stop index.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Indexing, Slicing, and range()
  Preview: Pattern to remember: subset = numbers[::2][::-1]

### Sequences and Access

- Snippet ID: `item:cs-curated-hw-seq-nth-occurrence`
- Topic: Sequences and Access
- Card ID: `w1-sequences-and-access`
- Piece count: `1`

- `cs-curated-hw-seq-nth-occurrence`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Find the nth occurrence by advancing .index() x = ['A', 'B', 'A', 'C', 'B', 'A', 'B'] n = 2 i = -1 for _ in range(n): i = x.index('B', i + 1) print(i) 4

### Sequences and Access

- Snippet ID: `item:cs-curated-hw-seq-slice-between-sentinels`
- Topic: Sequences and Access
- Card ID: `w1-sequences-and-access`
- Piece count: `1`

- `cs-curated-hw-seq-slice-between-sentinels`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Slice between two sentinel values without hard-coding indices x = [21, 15, 29, 20, 15, 21, 38, 26] left = x.index(15) + 1 right = left + x[left:].index(15) print(x[left:right]) [29, 20]

### Sequences and Access

- Snippet ID: `item:exam-extra_practice-6-w1-sequences-and-access`
- Topic: Sequences and Access
- Card ID: `w1-sequences-and-access`
- Piece count: `1`

- `exam-extra_practice-6-w1-sequences-and-access`
  Bucket: `recommended` | Type: `source_exam`
  Preview: numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] Which of the following lines of code will NOT create a list with the name subset, and the value [10, 8, 6, 4, 2]? a b c d d a: starts at -1 (10), step -2: [10,8,6,4,2]. Correct.…

### Sequences and Access

- Snippet ID: `item:exam-intro_python_sample_final_24_25-18-w2-conditions`
- Topic: Sequences and Access
- Card ID: `w1-sequences-and-access`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-18-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: How do you break a list into a list of lists, where each sublist contains 3 elements? A B C D A Option A uses range(0, 7, 3) which generates 0, 3, 6. The slices x[0:3], x[3:6], and x[6:9] correctly partition the list.

### Sequences and Access

- Snippet ID: `item:ks-685cd3d828`
- Topic: Sequences and Access
- Card ID: `w1-sequences-and-access`
- Piece count: `1`

- `ks-685cd3d828`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Indexing Forward: 0, 1, 2, ... len-1. Backward: -1 (last), -2 (second to last), ..., -len (first). l1[0] == l1[-len(l1)]

### Sequences and Access

- Snippet ID: `item:ks-be78ccac04`
- Topic: Sequences and Access
- Card ID: `w1-sequences-and-access`
- Piece count: `1`

- `ks-be78ccac04`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: range() range(start, stop, step). start default=0, step default=1. Stop is NOT inclusive. Works like slicing but defaults differ slightly. range examples print(list(range(6))) # [0, 1, 2, 3, 4, 5] print(list(range(3,6))…

## Week 2

Snippet families in this group: **102**

### Comparisons, `in`, Precedence, and Conditional Expressions

- Snippet ID: `subtopic:w2-conditions:w2-conditions-core`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `6`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Comparisons, `in`, Precedence, and Conditional Expressions
  Preview: Precedence trap a=1; b=3 # WRONG: Python evaluates 'and' before 'or' print(a==1 or a==2 and b==1 or b==2) # True (unexpected) # CORRECT: use brackets print((a==1 or a==2) and (b==1 or b==2)) # False Precedence (high to…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Comparisons, `in`, Precedence, and Conditional Expressions
  Preview: Inclusion check — 'in' operator print(1 in [1,2,3]) # True print(1 in (1,2,3)) # True print('1' in '123') # True (substring) print(1 in {1:4, 2:3}) # True (checks keys) print(4 in {1:4, 2:3}) # False (4 is value, not ke…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Comparisons, `in`, Precedence, and Conditional Expressions
  Preview: if/elif/else structure if condition_1: expression_1 elif condition_2: expression_2 expression_3 else: expression_4 if/elif/else. One if at start, at most one else at end, unlimited elif in between. Indentation is critic…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Comparisons, `in`, Precedence, and Conditional Expressions
  Preview: Conditional expression (ternary) # Statement form: if a > 0: b = a else: b = 0 # Expression form: b = a if a > 0 else 0 # Even simpler: b = max(0, a) if/elif/else. One if at start, at most one else at end, unlimited eli…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Comparisons, `in`, Precedence, and Conditional Expressions
  Preview: Comparison operators return booleans print(3 > 2) A comparison like `3 > 2` evaluates to either `True` or `False`. True
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Comparisons, `in`, Precedence, and Conditional Expressions
  Preview: `not` flips booleans print(not True) print(not False) `not True` becomes `False` and `not False` becomes `True`. False True

### Conditions

- Snippet ID: `item:cs-curated-hw-conditions-first-match-wins`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `cs-curated-hw-conditions-first-match-wins`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Branch order matters because the first matching condition wins x = [5, 10, 15, 20] a, b, c, d = 4, 9, 13, 15 result = [] for element in x: if element <= d: label = 'cat4' elif element >= c: label = 'cat3' elif element <…

### Conditions

- Snippet ID: `item:exam-Test Exam 07-06-22-4-w2-conditions`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `exam-Test Exam 07-06-22-4-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You're trying to write a function called is_anagram, which takes two strings as inputs and checks whether they are anagrams of each other. That is: whether one of them can be written by rearranging the letters of the ot…

### Conditions

- Snippet ID: `item:exam-midterm_2023-1-w2-conditions`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `exam-midterm_2023-1-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What is the output of the following code snippet?

### Conditions

- Snippet ID: `item:exam-midterm_2024-2-w2-conditions`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `exam-midterm_2024-2-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Assume you have the following variables: x = 3 y = 3.0 z = '3' What will be printed by the following code: print((x != z and x == int(z)) or (x != y and y != z)) A True B False C The code will result in an error. D 3

### Conditions

- Snippet ID: `item:exam-trial_midterm-13-w2-conditions`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `exam-trial_midterm-13-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called weather_alert that accepts a string argument, which is a color code of the weather alert system.

### Conditions

- Snippet ID: `item:exam-trial_midterm-6-w2-conditions`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `exam-trial_midterm-6-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: def main(lst, condition=lambda x: x): y = [] for x in lst: if condition(x): y.append(x) return y What will this function return, when called in the following way: main([1, 2, 3, 4, 5…

### Conditions

- Snippet ID: `item:kp-manual-precedence`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `kp-manual-precedence`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: `not` binds tighter than `and`, and `and` binds tighter than `or`; add parentheses when the intended grouping is not obvious.

### Conditions

- Snippet ID: `item:kp-manual-ternary`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `kp-manual-ternary`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Use `x if cond else y` when both branches are single expressions; use a full `if/elif/else` block when the branches need multiple statements.

### Conditions

- Snippet ID: `item:ks-4b427a2425`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `ks-4b427a2425`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Conditions and boolean operators — precedence Precedence (high to low): comparisons → not → and → or. Use parentheses to be explicit. 'in' checks membership in sequence/set/dict-keys. Precedence trap a=1; b=3 # WRONG: P…

### Conditions

- Snippet ID: `item:ks-c19999c074`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `ks-c19999c074`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Conditional statements and expressions if/elif/else. One if at start, at most one else at end, unlimited elif in between. Indentation is critical — all code in a block must have same indentation. Conditional expression…

### Conditions

- Snippet ID: `item:manual-bool-precedence`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `manual-bool-precedence`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do `not`, `and`, and `or` combine when there are no extra parentheses? `not` is evaluated first, then `and`, then `or`, so parenthesize whenever the intended logic is not obvious. print(not False and True or False)

### Conditions

- Snippet ID: `item:manual-conditional-expression`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `manual-conditional-expression`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: When should you use `x if cond else y` instead of a multi-line `if/else` block? Use the conditional expression for a single value choice; use a full block when each branch needs multiple statements. label = 'pass' if sc…

### Conditions

- Snippet ID: `item:manual-filter-condition`
- Topic: Conditions
- Card ID: `w2-conditions`
- Piece count: `1`

- `manual-filter-condition`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Trace `main(lst, condition)` and identify which values satisfy `lambda x: x % 2 != 0`. Apply the condition to one element first, then keep only the values for which it returns `True`. def main(lst, condition): return [x…

### Conversion and Truthiness

- Snippet ID: `item:cs-3e39a2f12f`
- Topic: Conversion and Truthiness
- Card ID: `w2-conversion-and-truthiness`
- Piece count: `1`

- `cs-3e39a2f12f`
  Bucket: `additional` | Type: `source_notebook`
  Preview: type_conversion print ('1' * 2, '1' * True, '1' * False)

### Conversion and Truthiness

- Snippet ID: `item:cs-fc8bdeb969`
- Topic: Conversion and Truthiness
- Card ID: `w2-conversion-and-truthiness`
- Piece count: `1`

- `cs-fc8bdeb969`
  Bucket: `additional` | Type: `source_notebook`
  Preview: type_conversion print (1==1.0, 1.0 == True, 0 == False)

### Conversion and Truthiness

- Snippet ID: `item:ks-d7e6d1b5b5`
- Topic: Conversion and Truthiness
- Card ID: `w2-conversion-and-truthiness`
- Piece count: `1`

- `ks-d7e6d1b5b5`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Truthy and Falsy In conditions, Python auto-converts to bool. Falsy: [], (), {}, set(), '', 0, 0.0, range(0), None. Truthy: everything else (non-empty collections, non-zero numbers). Falsy values # All evaluate to False…

### Conversion and Truthiness

- Snippet ID: `item:ks-d9760d8cd8`
- Topic: Conversion and Truthiness
- Card ID: `w2-conversion-and-truthiness`
- Piece count: `1`

- `ks-d9760d8cd8`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Type conversion (explicit) Python requires explicit conversion in most cases (unlike JavaScript). Conversion functions: str(), int(), float(), bool(), tuple(), list(), set(), dict(). Explicit conversions print(str(1) ==…

### Explicit Conversion and Truthy/Falsy Rules

- Snippet ID: `subtopic:w2-conversion-and-truthiness:w2-conversion-and-truthiness-core`
- Topic: Conversion and Truthiness
- Card ID: `w2-conversion-and-truthiness`
- Piece count: `10`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Falsy values # All evaluate to False in a condition: [] # empty list () # empty tuple {} # empty dict set() # empty set '' # empty string 0 # zero int 0.0 # zero float In conditions, Python auto-converts to bool. Falsy:…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Explicit conversions print(str(1) == '1') # True print(int('1') == 1) # True print(int('1a')) # ERROR print(float('1') == 1.0) # True print(float('1.0') == 1.0) # True print(tuple([1,2,3]) == (1,2,3)) # True print(tuple…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Implicit conversion (Python allows with bool/numeric mix) print(1 + True) # 2 print(1.0 + False) # 1.0 print('1' * 2) # '11' print('1' * True) # '1' print('1' * False) # '' Python requires explicit conversion in most ca…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: str(1) versus int('1') print(str(1) == '1') print(int('1') == 1)
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Why `'1' + 2` raises `TypeError` try: print ('1' + 2) except Exception as e: print(e)
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Why `dict([1, 2])` raises `ValueError` try: print(dict([1, 2])) except Exception as e: print(e)
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Why `int('1a')` raises `ValueError` try: print(int('1a') == 1) except Exception as e: print(e)
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Truthy list in a `while` condition l1 = [1, 2, 3, 4, 5, 6] total = 0 while l1: total += l1[0] del l1[0] print(total) For numeric variables, `a += 1` updates the stored value the same way as `a = a + 1`.
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: In conditions, Python auto-converts to bool. Falsy: [], (), {}, set(), '', 0, 0.0, range(0), None. Truthy: everything else (non-empty collections, non-zero numbers).
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Explicit Conversion and Truthy/Falsy Rules
  Preview: Python requires explicit conversion in most cases (unlike JavaScript). Conversion functions: str(), int(), float(), bool(), tuple(), list(), set(), dict().

### Creation, Lookup, Updates, and Key Constraints

- Snippet ID: `subtopic:w2-dictionaries-and-mappings:w2-dictionaries-and-mappings-core`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `10`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Creating and using dicts capitals = {} capitals = dict() capitals = {'Andorra': 'Andorra la Vella', 'Belgium': 'Brussels'} print(capitals['Belgium']) # Brussels del(capitals['Belgium']) # delete key capitals['Netherland…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Dict membership checks KEYS, not values d = {1: 4, 2: 3} print(1 in d) # True (1 is a key) print(4 in d) # False (4 is a value, not a key) Dicts map unique immutable keys to values. `key in d` checks keys, and equality…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Dictionary creation and lookup squares = {1:1, 2:4, 3:9, 4:16} print(squares) l1 = [1, 2, 3, 4] l2 = [1, 4, 9, 16] squares = dict(zip(l1, l2)) print(squares) Check whether the code is looking up a key, iterating with `.…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Dictionary creation and lookup squares = {} print(squares) squares = dict() print(squares) Check whether the code is looking up a key, iterating with `.items()`, or mutating the dictionary.
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Dictionary creation and lookup squares = {1:1, 2:4, 3:9, 4:16} del(squares[2]) print(squares) Check whether the code is looking up a key, iterating with `.items()`, or mutating the dictionary.
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Dictionary creation and lookup a = 1 b = {1:1} print({a:b}) try: print({b:a}) except Exception as e: print(e) Check whether the code is looking up a key, iterating with `.items()`, or mutating the dictionary.
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Dictionary creation and lookup capitals = {'Estonia': 'Tallinn', 'Belgium': 'Brussels', 'France': 'Paris'} print(capitals['Belgium']) Check whether the code is looking up a key, iterating with `.items()`, or mutating th…
- `manual-dict-construction-and-iteration`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Construct, iterate, count, and sort dictionaries words = ['pear', 'apple', 'pear'] counts = {} for word in words: counts[word] = counts.get(word, 0) + 1 print(dict(zip(['a', 'b'], [1, 2]))) for key in sorted(counts): pr…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Dicts map unique immutable keys to values. `key in d` checks keys, and equality ignores insertion order.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Creation, Lookup, Updates, and Key Constraints
  Preview: Use `.keys()`, `.values()`, and `.items()` for dictionary views; looping over a dict directly gives keys.

### Dictionaries and Mappings

- Snippet ID: `item:cs-curated-hw-dict-delete-shared-keys`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `cs-curated-hw-dict-delete-shared-keys`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Delete keys only when they also appear in a reference dict x = {'a': 1, 'b': 2, 'c': 3} to_remove = {'c': 3, 'd': 3} for key in to_remove: if key in x: del x[key] print(x) {'a': 1, 'b': 2}

### Dictionaries and Mappings

- Snippet ID: `item:cs-curated-hw-dict-digit-frequency`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `cs-curated-hw-dict-digit-frequency`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Count only digit characters that actually appear x = ['1', 'a', 'X', '2', 'b', 'Y', '1', 'a', 'X', '1', 'a', 'X'] counts = {} for digit in '0123456789': if digit in x: counts[digit] = x.count(digit) print(counts) {'1':…

### Dictionaries and Mappings

- Snippet ID: `item:cs-curated-hw-dict-project-values-sorted-keys`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `cs-curated-hw-dict-project-values-sorted-keys`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Sort keys first, then project values in that order x = {1: 3, 3: 4, 2: 5} sorted_keys = sorted(x.keys(), reverse=True) result = [x[key] for key in sorted_keys] print(result) [4, 5, 3]

### Dictionaries and Mappings

- Snippet ID: `item:exam-Resit 22/23-7-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-Resit 22/23-7-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Assume you already have a list of strings called words. You need to create a dictionary called word_lengths, where the keys are the strings in the list words and the values are their lengths. Which of the following code…

### Dictionaries and Mappings

- Snippet ID: `item:exam-Trial final - Introduction to Python - 22/23-4-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-Trial final - Introduction to Python - 22/23-4-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have to create a dictionary called vowels_ASCII where the keys are the lowercase vowels (a, e, i, o, u) and the values are their corresponding ASCII values. The ASCII (American Standard Code for Information Intercha…

### Dictionaries and Mappings

- Snippet ID: `item:exam-Trial final - Introduction to Python - 22/23-5-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-Trial final - Introduction to Python - 22/23-5-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have three variables called player1_goals, player2_goals, and player3_goals. Each of the variables contains a list of integers that represents the number of goals scored by the football players in five diffe…

### Dictionaries and Mappings

- Snippet ID: `item:exam-Trial final - Introduction to Python - 22/23-6-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-Trial final - Introduction to Python - 22/23-6-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have the following dictionary that represents the monthly sales of a store: monthly_sales = {'January': 1500, 'February': 2200, 'March': 1800, 'April': 2400, 'May': 2000, 'June': 2800} You need to calculate the aver…

### Dictionaries and Mappings

- Snippet ID: `item:exam-extra_practice-12-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-extra_practice-12-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: def counter(y): x = {} for index, element in enumerate(y): if index != int(element) and int(element) % 2 == 0: x[element] = len(element) return x What will this function return when called as: counter(['12345678', '1',…

### Dictionaries and Mappings

- Snippet ID: `item:exam-extra_practice-3-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-extra_practice-3-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Adelbrecht and Hortensia competed in a game. You have a dictionary with two subdictionaries: results = {'Adelbrecht':{'attempt1':3,'attempt2':2,'attempt3':6},'Hortensia':{'attempt1':1,'attempt2':6}} You would like to cr…

### Dictionaries and Mappings

- Snippet ID: `item:exam-extra_practice-4-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-extra_practice-4-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: math_scores = {'John': 85, 'Sarah': 92, 'Michael': 78, 'Emma': 90, 'David': 82} You want to find and print the names of the students who scored above the average score. Which of the following code segments will work as…

### Dictionaries and Mappings

- Snippet ID: `item:exam-extra_practice-5-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-extra_practice-5-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: students = ['A','B','C','D','E','F'] grades = [9,10,9,11,10,9] You need to create a dictionary called grade_counts that counts the number of students in each grade level. Expected: {9:3, 10:2, 11:1} Which of the followi…

### Dictionaries and Mappings

- Snippet ID: `item:exam-extra_practice-8-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-extra_practice-8-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: x = {'a': [1, 2], 'b':[3, 4], 'c':[5, 6], 'd':[7, 8]} Which of the following lines of code will print True? a b c d d a: x['a'][1]=2, x['b'][0]=3, 2*3=6, x['c'][1]=6. True. b: x['b'][0]=3, x['c'][0]=5, 3+5=8, x['d'][1]=…

### Dictionaries and Mappings

- Snippet ID: `item:exam-intro_python_sample_final_24_25-19-w3-defining-and-calling-functions`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-19-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which of the following programs correctly returns a dictionary where values are sums of input values whose keys are <= the output key? A B C D C Both methods correctly calculate the cumulative sums based on key values,…

### Dictionaries and Mappings

- Snippet ID: `item:exam-intro_python_sample_final_24_25-20-w3-defining-and-calling-functions`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-20-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What is the result of the program comparing d1 (from zip) and d2 (from enumerate)? A B C D A Both d1 and d2 result in the same dictionary: {1: 2, 2: 3, 3: 4, 4: 5}.

### Dictionaries and Mappings

- Snippet ID: `item:exam-intro_python_sample_final_24_25-21-w3-defining-and-calling-functions`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-21-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: The following codes all print the same value, except one. Which one? A B C D A Iterating directly over a dictionary (for key, value in d1) only yields keys. This will cause a ValueError when trying to unpack into two va…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2023-5-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2023-5-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: What is the output of the program below?

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2023-6-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2023-6-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following dictionary: sample_dict = { "name": "Kim", "age": 25, "birthdate": "3-2-1998", "city": "Amsterdam"} Suppose you want to create a dictionary that only contains the keys 'name' and 'city'. W…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2023-7-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2023-7-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following dictionary: closet = { "shirts" : 5, "colors" : ['red', 'yellow', 'blue', 'pink'] } You want to: - add a key "shoes" which has a value that is a list containing the strings "sneakers" and…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2023-8-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2023-8-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following function: def my_count_function(string): counts = {} for letter in string: counts[letter] = string.count(letter) return counts And you create the following two dictionaries: desk_count = m…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2024-10-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2024-10-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following dictionary: library = {"books": 5, "genres": ['action', 'romance', 'thriller', 'classics']} You want to: - add a key "years", of which the value is a list of strings that are the years of…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2024-11-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2024-11-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following function: def my_count_function(string): counts = {} for letter in string: if letter in counts: counts[letter] += 1 else: counts[letter] = 1 return counts And you create the following two…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2024-12-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2024-12-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following dictionary: x = {1: 10, 2: 20, 3: 30, 4: 40} What will the following line of code print? print(list(x.values()) + list(x.keys())) A [10, 20, 30, 40, 1, 2, 3, 4] B [11, 22, 33, 44] C This c…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2024-7-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2024-7-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following a dictionary called students, which contains three sub-dictionaries: students = {"james": {"name": "James", "homework": [90.0, 97.0, 75.0, 92.0], "quizzes": [88.0, 40.0, 94.0], "tests": [7…

### Dictionaries and Mappings

- Snippet ID: `item:exam-midterm_2024-8-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-midterm_2024-8-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: You need to write a function called dict_keys that checks whether a certain key is in available in a certain dictionary.

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial-final-exam-py22-4-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial-final-exam-py22-4-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have to create a dictionary called roman_nums where the keys are the integers from 1 to 5 (both are inclusive) and the values are their corresponding Roman numeral symbols. That is, if we execute the following comma…

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial-final-exam-py22-5-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial-final-exam-py22-5-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have two lists representing the names and ages of individuals: names = ['Alice', 'Bob', 'Charlie', 'David'] ages = [25, 30, 35, 40] You need to create a dictionary called person_dict where the keys are the names and…

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial-final-exam-py22-6-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial-final-exam-py22-6-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have the following dictionary that represents the performance ratings of employees in a company: employee_ratings = {'John': 8, 'Sarah': 9, 'Michael': 7, 'Emma': 9, 'David': 6} You need to find and print the name of…

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial_midterm-10-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial_midterm-10-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following dictionary: x = {1: 10, 2: 20, 3: 30, 4: 40} What will the following line of code print? print(list(x.values()) + list(x.keys())) A This code will result in an error because you cannot con…

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial_midterm-19-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial_midterm-19-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following function: def my_count_function(string): counts = {} for letter in string: if letter in counts: counts[letter] += 1 else: counts[letter] = 1 return counts And you create the following two…

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial_midterm-2-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial_midterm-2-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have a dictionary called characters, of which keys are strings and values are lists of strings.

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial_midterm-23-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial_midterm-23-w2-dictionaries-and-mappings`
  Bucket: `additional` | Type: `source_exam`
  Preview: You have to write a function called summarize which take a list of integers as an argument.

### Dictionaries and Mappings

- Snippet ID: `item:exam-trial_midterm-8-w2-dictionaries-and-mappings`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `exam-trial_midterm-8-w2-dictionaries-and-mappings`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following dictionary: library = {"books": 5, "genres": ['action', 'romance', 'thriller', 'classics']} You want to: - add a key "years", of which the value is a list of strings that are the years of…

### Dictionaries and Mappings

- Snippet ID: `item:kp-1-d3`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `kp-1-d3`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dense reference table Operation | What it gives | Exam note d[key] | value lookup | Key must exist key in d | membership on keys | not values d.items() | (key, value) pairs | good for loops d.update(...) | mutates dict…

### Dictionaries and Mappings

- Snippet ID: `item:kp-1-d4`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `kp-1-d4`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Construction and lookup patterns Pattern | What it does | Exam use {'a': 1} | literal dict | fastest way to show known pairs dict() | empty dict | start building inside a loop dict(zip(keys, values)) | pairs two iterabl…

### Dictionaries and Mappings

- Snippet ID: `item:kp-2-d3`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `kp-2-d3`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dictionary equality ignores insertion order print({1: 1, 2: 2} == {2: 2, 1: 1}) print([1, 2] == [2, 1])

### Dictionaries and Mappings

- Snippet ID: `item:ks-65c4de2e9d`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `ks-65c4de2e9d`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Dictionaries Sets of key:value pairs. Keys must be unique and immutable (hashable). Dictionaries are unordered for equality ({1:1,2:2}=={2:2,1:1} is True). Cannot be sorted. You can check membership with 'in' — this che…

### Dictionaries and Mappings

- Snippet ID: `item:ks-adb6d9f967`
- Topic: Dictionaries and Mappings
- Card ID: `w2-dictionaries-and-mappings`
- Piece count: `1`

- `ks-adb6d9f967`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Looping over dictionaries .keys() → key sequence. .values() → value sequence. .items() → sequence of (key, value) tuples. 'for key in dict' is the same as 'for key in dict.keys()'. Looping over dict capitals = {'Andorra…

### Lists and Sets

- Snippet ID: `item:exam-Resit 22/23-1-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-Resit 22/23-1-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have a list called x containing tuples. Which of the following lines of code will print True? a b c d d Option A evaluates to 2 * 3 == 6 (True). Option B evaluates to 3 + 5 == 8 (True). Option C evaluates to…

### Lists and Sets

- Snippet ID: `item:exam-Test Resit - Introduction to Python - 22/23-1-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-Test Resit - Introduction to Python - 22/23-1-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have a list called x containing tuples, where x = [(1, 2), (3, 4), (5, 6), (7, 8)] Which of the following lines of code will print True? a b c d d Option A evaluates to 2 * 3 == 6 (True). Option B evaluates…

### Lists and Sets

- Snippet ID: `item:exam-Test Resit - Introduction to Python - 22/23-5-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-Test Resit - Introduction to Python - 22/23-5-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have a list called x, where: Which of the following code segments will print the following list? [5, 4, 3, 2, 1] a b c d c Option A creates a set (removing duplicates) and sorts it in reverse order, yielding…

### Lists and Sets

- Snippet ID: `item:exam-extra_practice-1-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-extra_practice-1-w2-lists-and-sets`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following function: def func1(l1): return len(list(l1))==len(set(l1)) Which of the functions below returns the same values as the function above, if we call it in any of the following ways? func1(l1…

### Lists and Sets

- Snippet ID: `item:exam-midterm_2023-15-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-midterm_2023-15-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Assume you already have a variable a, which is an integer between 1 and 4. What is the ​output of the following ​code snippet?

### Lists and Sets

- Snippet ID: `item:exam-midterm_2023-16-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-midterm_2023-16-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: mylist = [1, 3, 2, 3, 4, 5, 3, 3] mylist.append('3') mylist.remove(3) print(mylist.count(3)) What will be the output? Hint: The remove() list method removes the first occurrence of t…

### Lists and Sets

- Snippet ID: `item:exam-midterm_2024-22-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-midterm_2024-22-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: x = ["a", "b", "c", "4"] print(x[-3] + x[3]*3) Which of the following code snippet will print the same output? A z = [["a", "b", "c"], [1, 2, 3, 4]] print(z[0][1] + str(z[1][3])*3) B…

### Lists and Sets

- Snippet ID: `item:exam-midterm_2024-23-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-midterm_2024-23-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: mylist = [1, 2, 5, 7, 9, 12] new_list1 = mylist[0:3] new_list2 = mylist[1:4] print(new_list1 + new_list2) What will be printed? A [1, 2, 5, 2, 5, 7] B [1, 2, 5, 7, 2, 5, 7, 9] C [2,…

### Lists and Sets

- Snippet ID: `item:exam-midterm_2024-24-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-midterm_2024-24-w2-lists-and-sets`
  Bucket: `additional` | Type: `source_exam`
  Preview: You have the following list: my_list = [1,2,3,4] Which one of the following lines of code lines does not print 4 as the output? A print(max(my_list)) B print(len(my_list)) C print(my_list[4]) D print(my_list[-1])

### Lists and Sets

- Snippet ID: `item:exam-trial-final-exam-py22-7-w2-lists-and-sets`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `exam-trial-final-exam-py22-7-w2-lists-and-sets`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What is the output of the following code segment? a b c d c The list comprehension filters numbers that are even (x % 2 == 0) and greater than 2 (x > 2). From the list, only 4 satisfies both conditions.

### Lists and Sets

- Snippet ID: `item:ks-08ac820c2f`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `ks-08ac820c2f`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Sets Unordered collection of unique values. Empty set MUST be set() — {} creates empty dict. Elements must be immutable. No indexing. Methods: .add(), .remove(), .update(). Set operations countries = set() # empty set (…

### Lists and Sets

- Snippet ID: `item:ks-4258f15a6c`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `1`

- `ks-4258f15a6c`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Lists vs Dictionaries vs Sets — ordered/unordered Lists, tuples, strings are SEQUENCES (ordered). Dicts and sets are NOT sequences (unordered for equality). All are called collections. Ordering comparison print([1,2] ==…

### Sequences, Uniqueness, and Common Operations

- Snippet ID: `subtopic:w2-lists-and-sets:w2-lists-and-sets-core`
- Topic: Lists and Sets
- Card ID: `w2-lists-and-sets`
- Piece count: `10`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Ordering comparison print([1,2] == [2,1]) # False (ordered) print((1,2) == (2,1)) # False (ordered) print('12' == '21') # False (ordered) print({1,2} == {2,1}) # True (unordered) print({1:1,2:2}=={2:2,1:1}) # True (unor…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Set operations countries = set() # empty set (NOT {}) countries = {'Andorra', 'Belgium'} print({1,2,2} == {2,1}) # True (duplicates ignored) print(len({1,2,2})) # 2 countries.remove('Andorra') countries.add('Greece') co…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Create a list literal squares = [1, 4, 9, 16] print(squares)
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Delete by index with `del` squares = [1, 4, 5, 9, 16] del(squares[2]) print(squares)
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Two ways to create an empty list squares = [] print(squares) squares = list() print(squares)
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Lists are mutable: replace by index squares = [1, 4, 8, 15] squares[2] = 9 squares[3] = 16 print(squares)
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: List method effects and resulting list squares = [1, 4, 9, 16] squares.append(16) squares.append(25) print(squares) Check whether the method mutates the list in place and what the list looks like after each call.
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: List method effects and resulting list if 16 not in squares: squares.append(16) if 25 not in squares: squares.append(25) print(squares) Check whether the method mutates the list in place and what the list looks like aft…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Lists, tuples, strings are SEQUENCES (ordered). Dicts and sets are NOT sequences (unordered for equality). All are called collections.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sequences, Uniqueness, and Common Operations
  Preview: Unordered collection of unique values. Empty set MUST be set() — {} creates empty dict. Elements must be immutable. No indexing. Methods: .add(), .remove(), .update().

### for, while, Dictionary Iteration, enumerate(), zip(), and Walrus

- Snippet ID: `subtopic:w2-loops:w2-loops-core`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `8`

- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: Skip certain values with `continue` total = 0 for number in [1, 2, '3', 3, 5, 7]: if type(number) == str: continue total += number print(total) # 18 Use `continue` to ignore the current item and jump straight to the nex…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: Loop variable not used — use _ for _ in range(5): print('Hello') # prints Hello 5 times Use `_` when the loop should repeat a fixed number of times but the loop variable itself is not needed. Hello Hello Hello Hello Hel…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: `enumerate(seq, start=1)` countries = ['Andorra', 'Belgium'] for index, country in enumerate(countries, 1): print(country, 'has index:', index) # Andorra has index: 1 # Belgium has index: 2 Use `enumerate` when you need…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: `zip(a, b)` pairs items in parallel countries = ['Andorra', 'Belgium'] capitals = ['Andorra la Vella', 'Brussels'] for country, capital in zip(countries, capitals): print(country, 'has capital:', capital) Use `zip` when…
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: `while items:` repeats until the list is empty l1 = [1, 2, 3, 4, 5, 6] total = 0 while l1: # truthy while list is non-empty total += l1[0] del l1[0] print(total) # 21 Non-empty lists are truthy and empty lists are falsy…
- `manual-loop-max-sublist-sum`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: Keep the sub-list whose elements have the largest sum lists = [[1, 2], [4, 4], [3, 3, 1]] best = lists[0] for current in lists[1:]: if sum(current) > sum(best): best = current print(best) Store the current best sub-list…
- `manual-loop-zip-enumerate-membership`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: Combine `zip`, `enumerate`, unpacking, and membership names = ['Ada', 'Bob', 'Cleo'] scores = [8, 5] for index, (name, score) in enumerate(zip(names, scores), start=1): passed = score in {5, 6, 7, 8, 9, 10} print(index,…
- `kp-iteration-traps`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: for, while, Dictionary Iteration, enumerate(), zip(), and Walrus
  Preview: `zip` stops at the shortest iterable, `in` checks membership, `//` floors division, `%` gives the remainder, and `sum(condition for ...)` counts how many times the condition is true.

### Loops

- Snippet ID: `item:cs-curated-hw-loops-enumerate-mark-max`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `cs-curated-hw-loops-enumerate-mark-max`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Use enumerate() to keep indices while relabeling one special case x = [65, 43, 1, 0, 59, 16, 86, 40, 60] max_value = max(x) result = {} for index, value in enumerate(x): key = 'highest' if value == max_value else index…

### Loops

- Snippet ID: `item:cs-curated-hw-loops-market-clearing`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `cs-curated-hw-loops-market-clearing`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Flatten, sort, and zip demand/supply curves to count trades buyers = {'buyer1': [24, 16, 13, 6, 5], 'buyer2': [23, 21, 19, 10, 7], 'buyer3': [21, 20, 15, 13, 10], 'buyer4': [20, 17, 9, 6, 5]} sellers = {'seller1': [8, 1…

### Loops

- Snippet ID: `item:cs-curated-hw-loops-nested-pairwise-dict`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `cs-curated-hw-loops-nested-pairwise-dict`
  Bucket: `additional` | Type: `source_notebook`
  Preview: Nested loops can build pairwise results for every combination def main(minimum, maximum): result = {} for first in range(minimum, maximum + 1): for second in range(minimum, maximum + 1): result[(first, second)] = first…

### Loops

- Snippet ID: `item:cs-curated-hw-loops-zip-filter-pairs`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `cs-curated-hw-loops-zip-filter-pairs`
  Bucket: `additional` | Type: `source_notebook`
  Preview: zip() aligns two lists so you can filter pairs into a dict keys = [3, 2, 1, 4] values = [3, 37, 60, 79] result = {} for key, value in zip(keys, values): if key != value and value % 5: result[key] = value print(result) {…

### Loops

- Snippet ID: `item:exam-Test Resit - Introduction to Python - 22/23-4-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-Test Resit - Introduction to Python - 22/23-4-w2-loops`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following function, which takes two integers as arguments: What will be printed by the following line of code: print(main(1)) a b c d b The function uses y=11 as a default argument. The while loop r…

### Loops

- Snippet ID: `item:exam-intro_python_sample_final_24_25-14-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-14-w2-loops`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Choose the program that iterates over integers from 1 to 10 and prints the sum of the current and previous number (starting with 0 as previous). A B C D B Option B correctly updates the 'previous' state at the end of ea…

### Loops

- Snippet ID: `item:exam-midterm_2023-14-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2023-14-w2-loops`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Assume you already have a variable called alphabet, which contains a string, e.g., alphabet = "abcdefghijklmnopqrstuvwxyz" Which of the following code snippets will give the same output as the following command? print(l…

### Loops

- Snippet ID: `item:exam-midterm_2023-2-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2023-2-w2-loops`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What is the output of the following code snippet?

### Loops

- Snippet ID: `item:exam-midterm_2024-17-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2024-17-w2-loops`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following function which take a list of numerical strings as an argument.

### Loops

- Snippet ID: `item:exam-midterm_2024-18-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2024-18-w2-loops`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have the following function count_characters, which takes two arguments: a list of strings which are names, and an optional keyword argument called character that has a default value of 'a'. def count_charac…

### Loops

- Snippet ID: `item:exam-midterm_2024-20-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2024-20-w2-loops`
  Bucket: `additional` | Type: `source_exam`
  Preview: What is the output of the program below?

### Loops

- Snippet ID: `item:exam-midterm_2024-21-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2024-21-w2-loops`
  Bucket: `additional` | Type: `source_exam`
  Preview: Assume you already have a variable called x, which contains a list of integers. Which of the following programs will print you a list of the squared values of the elements in x?

### Loops

- Snippet ID: `item:exam-midterm_2024-3-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2024-3-w2-loops`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: i = 1 while True: if i % 2 == 0: i += 1 continue elif i == 7: break else: print(i) i += 1 Which of the following code snippets will print the same output? A for i in range(1, 5, 2):…

### Loops

- Snippet ID: `item:exam-midterm_2024-9-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-midterm_2024-9-w2-loops`
  Bucket: `additional` | Type: `source_exam`
  Preview: Suppose you have a dictionary called characters, of which keys are strings and values are lists of strings.

### Loops

- Snippet ID: `item:exam-trial_midterm-5-w2-loops`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `exam-trial_midterm-5-w2-loops`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: i = 1 while True: if i % 2 == 0: i += 1 continue elif i == 7: break else: print(i) i += 1 Which of the following code snippets will print the same output? A for i in range(1, 5, 2):…

### Loops

- Snippet ID: `item:kp-iteration-traps-d1`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `kp-iteration-traps-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Iteration helpers and operator traps Pattern | Returns / does | Trap zip(a, b) | pairs items in parallel | extra items in the longer iterable are ignored x in d | checks dict keys | not dict values a // b | floor divisi…

### Loops

- Snippet ID: `item:kp-manual-break-continue`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `kp-manual-break-continue`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: `break` exits the loop immediately; `continue` skips the rest of the current iteration and moves to the next one.

### Loops

- Snippet ID: `item:kp-manual-enumerate`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `kp-manual-enumerate`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: `enumerate(seq, start)` gives `(index, value)` pairs; `zip(a, b)` gives tuples of items from multiple iterables in parallel.

### Loops

- Snippet ID: `item:kp-manual-enumerate-d1`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `kp-manual-enumerate-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Start offset and tuple unpacking letters = ['a', 'b', 'c'] for index, letter in enumerate(letters, start=1): print(index, letter) for left, right in zip(['x', 'y'], [10, 20]): print(left, right)

### Loops

- Snippet ID: `item:kp-manual-loop-core`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `kp-manual-loop-core`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Use `for` when you already have an iterable; use `while` when repetition should continue only while a condition stays `True`.

### Loops

- Snippet ID: `item:kp-manual-loop-core-d1`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `kp-manual-loop-core-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Pick the loop shape first Pattern | Use when | Common exam note for item in seq | you need the values | prefer this over indexing when position is irrelevant for i, item in enumerate(seq, start) | you need both index an…

### Loops

- Snippet ID: `item:kp-manual-while-truthy`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `kp-manual-while-truthy`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: A `while` condition is checked before every iteration, so a list loop like `while items:` keeps going only while the list is non-empty.

### Loops

- Snippet ID: `item:ks-4c6274845e`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `ks-4c6274845e`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: zip() Loops over multiple sequences in parallel. Zips sequences of equal length (Python handles unequal lengths but it can be messy). Can zip sequences of different types. Can zip more than 2. zip two lists countries =…

### Loops

- Snippet ID: `item:ks-59aaf6b0ee`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `ks-59aaf6b0ee`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: enumerate() Provides index alongside value when looping. enumerate(seq, start) — second arg sets the start index (default 0). enumerate with start=1 countries = ['Andorra', 'Belgium'] for index, country in enumerate(cou…

### Loops

- Snippet ID: `item:ks-624034d573`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `ks-624034d573`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Walrus operator := Introduced in Python 3.8. Assigns AND evaluates to a value (unlike = which is a statement). Useful in while conditions to assign and test at once. Walrus in while loop total = 0 while (number := int(i…

### Loops

- Snippet ID: `item:ks-72c9eada91`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `ks-72c9eada91`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Augmented assignment operators Shorthand for a = a OP b. All arithmetic operators have an augmented form. All augmented operators a += 1 # a = a + 1 a -= 2 # a = a - 2 a *= 3 # a = a * 3 a /= 4 # a = a / 4 a //= 5 # a =…

### Loops

- Snippet ID: `item:ks-8ad541fef7`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `ks-8ad541fef7`
  Bucket: `additional` | Type: `source_lecture`
  Preview: While-loops while condition: expression. Checks condition BEFORE each execution. Use break and continue. Watch for infinite loops (Ctrl+C to exit). Use when you don't know beforehand how many iterations are needed. For-…

### Loops

- Snippet ID: `item:ks-bddafc66a0`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `ks-bddafc66a0`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: For-loops for variable in sequence: expression. break: exit loop entirely. continue: skip to next iteration. You don't have to use the loop variable; use _ as convention when not needed. For-loop with continue total = 0…

### Loops

- Snippet ID: `item:manual-break-continue`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `manual-break-continue`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What is the difference between `break` and `continue` inside a loop? `break` exits the loop immediately; `continue` skips the rest of the current iteration and moves to the next one. for x in data: if x < 0: continue if…

### Loops

- Snippet ID: `item:manual-enumerate-zip`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `manual-enumerate-zip`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: When do you reach for `enumerate` versus `zip`? Use `enumerate(seq)` when you need index and value together; use `zip(a, b)` when you need items from multiple iterables in parallel. for i, value in enumerate(seq): ... f…

### Loops

- Snippet ID: `item:manual-loop-translate`
- Topic: Loops
- Card ID: `w2-loops`
- Piece count: `1`

- `manual-loop-translate`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Translate `alphabet[1::2]` into a loop that collects every second character starting at index 1. Initialize an empty result, loop over the needed indices, and append the selected characters in order. result = '' for i i…

## Week 3

Snippet families in this group: **65**

### Arguments

- Snippet ID: `item:exam-Resit 22/23-4-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-Resit 22/23-4-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following function, which takes two integers as arguments: What will be printed by the following line of code: print(main(1)) a b c d a The function `main` is called with `x=1`. `y` defaults to 11.…

### Arguments

- Snippet ID: `item:exam-Resit 22/23-6-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-Resit 22/23-6-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called main which accepts a flexible number of keyword arguments. The function should compute and return the sum of the values of the arguments. For example, if you call the function as: mai…

### Arguments

- Snippet ID: `item:exam-Test Resit - Introduction to Python - 22/23-6-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-Test Resit - Introduction to Python - 22/23-6-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called main which accepts a flexible number of keyword arguments. The function should compute and return the sum of the values of the arguments. For example, if you call the function as: mai…

### Arguments

- Snippet ID: `item:exam-intro_python_sample_final_24_25-23-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-23-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which of the following function calls would return the number 30 as a result? A B C D C The first call sums (6+7+8+9)=30. The second call sums (1+4+9+16)=30.

### Arguments

- Snippet ID: `item:exam-midterm_2023-10-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-midterm_2023-10-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called print_info which takes two required arguments called name and age, and a flexible number of keyword arguments. The function should return a dictionary with name, age, and all other ke…

### Arguments

- Snippet ID: `item:exam-midterm_2023-9-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-midterm_2023-9-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following function: def add_numbers(num1, num2 = 10, num3 = 20): return num1 + num2 + num3 What are the outputs if we call the function three times as follows: add_numbers(5, 15) add_numbers(5, num3…

### Arguments

- Snippet ID: `item:exam-midterm_2024-13-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-midterm_2024-13-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have to write a function called summarize which take a list of integers as an argument.

### Arguments

- Snippet ID: `item:exam-midterm_2024-14-w3-arguments`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `exam-midterm_2024-14-w3-arguments`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following function: def multiply(*args, factor=2): total = 1 for num in args: total *= num return total * factor Which of the following functions will return the same values as the function above, i…

### Arguments

- Snippet ID: `item:kp-manual-args-kwargs-return-d1`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `kp-manual-args-kwargs-return-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Flexible signature reference Piece | Meaning first, second=0 | fixed parameters, one with a default *args | extra positional arguments as a tuple **kwargs | extra keyword arguments as a dict return a, b | returns one tu…

### Arguments

- Snippet ID: `item:ks-40fee04740`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `ks-40fee04740`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: *args — undefined number of positional arguments Prefixing a parameter with * makes Python collect all extra positional arguments into a tuple named args. Can mix with defined parameters: def f(n1, n2, *args) — Python f…

### Arguments

- Snippet ID: `item:ks-d26b85265c`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `ks-d26b85265c`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Default arguments Default values are part of the function HEADER (not the call). When argument is omitted, the default is used. Keyword args in a call use =. CRITICAL: mutable defaults are evaluated ONCE at def time — n…

### Arguments

- Snippet ID: `item:ks-f5d65c7e89`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `1`

- `ks-f5d65c7e89`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Keyword arguments and **kwargs Arguments can be passed by name (keyword). **kwargs collects undefined keyword arguments into a dict. Order in function definition: positional, *args, keyword-with-defaults, **kwargs. Keyw…

### Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps

- Snippet ID: `subtopic:w3-arguments:w3-arguments-core`
- Topic: Arguments
- Card ID: `w3-arguments`
- Piece count: `13`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: *args usage def adder(*args): result = 0 for number in args: result += number return result print(adder(1, 2, 3, 4, 5)) # 15 Prefixing a parameter with * makes Python collect all extra positional arguments into a tuple…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Mix defined and *args def adder(n1, n2, *args): result = n1 + n2 for number in args: result += number return result print(adder(1, 2, 3, 4, 5)) # 15 Prefixing a parameter with * makes Python collect all extra positional…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Keyword arguments def calc(first, second, third, fourth, fifth, sixth): return first + 2*second + 3*third + 4*fourth + 5*fifth + 6*sixth print(calc(fifth=2, third=4, fourth=1, sixth=5, second=2, first=3)) # 63 Arguments…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: `**kwargs` behaves like a dict def calc(**kwargs): return kwargs['first'] + 2*kwargs['second'] + 3*kwargs['third'] print(calc(third=4, second=2, first=3)) Arguments can be passed by name (keyword). **kwargs collects und…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Default value def multiplier(first, second=2): return first * second print(multiplier(3)) # 6 (uses default second=2) print(multiplier(3, 3)) # 9 print(multiplier(2, second=3)) # 6 Default values are part of the functio…
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Mutable default BUG def main(addition, l1=[]): l1.append(addition) return l1 print(main(2)) # [2] print(main(3)) # [2, 3] ← BUG: l1 persists! Default values are part of the function HEADER (not the call). When argument…
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Return value with required positional args def adder(n1, n2): return n1 + n2 print(adder(1, 2)) Trace the returned value, not just what gets printed while the function runs.
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Default argument still returns one value def multiplier(first, second=2): return first * second print(multiplier(3)) Trace the returned value, not just what gets printed while the function runs.
- `manual-args-kwargs-return`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Flexible header plus tuple return def collect(first, *args, scale=1, **kwargs): return first * scale, args, kwargs result, extras, options = collect(2, 3, 4, scale=10, unit='cm') print(result) print(extras) print(option…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Prefixing a parameter with * makes Python collect all extra positional arguments into a tuple named args. Can mix with defined parameters: def f(n1, n2, *args) — Python fills n1,n2 first then collects remainder into arg…
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Arguments can be passed by name (keyword). **kwargs collects undefined keyword arguments into a dict. Order in function definition: positional, *args, keyword-with-defaults, **kwargs.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: Default values are part of the function HEADER (not the call). When argument is omitted, the default is used. Keyword args in a call use =. CRITICAL: mutable defaults are evaluated ONCE at def time — never use mutable d…
- `kp-manual-args-kwargs-return`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Positional, Keyword, Default, *args, **kwargs, and Mutable Argument Traps
  Preview: A flexible header can mix fixed parameters, defaults, `*args`, and `**kwargs`, and a `return a, b` statement sends one tuple back to the caller that can be unpacked later.

### def, Calls, and Methods vs Functions

- Snippet ID: `subtopic:w3-defining-and-calling-functions:w3-defining-and-calling-functions-core`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `7`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: def, Calls, and Methods vs Functions
  Preview: Define, call, and return a value def adder(n1, n2): total = n1 + n2 return total a = adder(1, 2) print(a) # 3 Define with `def name(params):` and call with `()`. `f[3]` tries to index, while `lst(0)` tries to call a lis…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: def, Calls, and Methods vs Functions
  Preview: Wrong bracket errors print[1] # TypeError: 'function' object is not subscriptable l1 = [1,2,3] l1(1) # TypeError: 'list' object is not callable Define with `def name(params):` and call with `()`. `f[3]` tries to index,…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: def, Calls, and Methods vs Functions
  Preview: Method on immutable — must capture return value s1 = 'UVA Amsterdam' s1 = s1.upper() # CORRECT — captures new string s1.upper() # WRONG — result is lost, s1 unchanged Methods are functions attached to objects. Some muta…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: def, Calls, and Methods vs Functions
  Preview: `list.sort()` mutates in place and returns `None` l1 = [3, 1, 2] l1.sort() # changes l1 in place, returns None print(l1) # [1, 2, 3] print(l1.index(2)) # 1 (returns index, doesn't change l1) Mutating methods and value-r…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: def, Calls, and Methods vs Functions
  Preview: Define with `def name(params):` and call with `()`. `f[3]` tries to index, while `lst(0)` tries to call a list and raises `TypeError`.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: def, Calls, and Methods vs Functions
  Preview: Methods are functions attached to objects. Some mutate the object in place, while others return a value; string methods always return a new string.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: def, Calls, and Methods vs Functions
  Preview: Function skeleton: `def f(x): return result`. Define with `def ...`, call with `()`, and use `[]` only for indexing.

### Defining and Calling Functions

- Snippet ID: `item:exam-Test Exam 07-06-22-3-w3-defining-and-calling-functions`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `exam-Test Exam 07-06-22-3-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You would like to write a function called get_tld that extracts the top-level domain from the URL of a website. The function takes the URL as the input string in the following format: "https://www.[SECOND-LEVEL DOMAIN].…

### Defining and Calling Functions

- Snippet ID: `item:exam-Test Exam 07-06-22-4-w3-defining-and-calling-functions`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `exam-Test Exam 07-06-22-4-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You're trying to write a function called is_anagram, which takes two strings as inputs and checks whether they are anagrams of each other. That is: whether one of them can be written by rearranging the letters of the ot…

### Defining and Calling Functions

- Snippet ID: `item:exam-Trial final exam Introduction to Python-4-w3-defining-and-calling-functions`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `exam-Trial final exam Introduction to Python-4-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called format_phone_number that formats phone numbers. The output of the function should be a string that represents a 10-digit number. The input argument is also a string with 10 digits, bu…

### Defining and Calling Functions

- Snippet ID: `item:exam-intro_python_sample_final_24_25-11-w3-defining-and-calling-functions`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-11-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which of the following code lines will create a dictionary, in which the keys are the elements of list_1 and the values are the number of characters in the corresponding key? A B C D A This is a standard dictionary comp…

### Defining and Calling Functions

- Snippet ID: `item:exam-intro_python_sample_final_24_25-17-w3-defining-and-calling-functions`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-17-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What will be printed by the function calls in the main function provided? A B C D D The function checks if all elements in the input list are either all empty or all non-empty. For the sets and lists provided, they are…

### Defining and Calling Functions

- Snippet ID: `item:exam-intro_python_sample_final_24_25-3-w3-defining-and-calling-functions`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-3-w3-defining-and-calling-functions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Imagine that you have a list called students, which is populated by a number of dictionaries. Each dictionary has keys: "Name" and "Grade". You'd like to print the text: [NAME] has received a grade of [GRADE], with the…

### Defining and Calling Functions

- Snippet ID: `item:ks-ab66f3bab6`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `ks-ab66f3bab6`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Methods vs functions Methods are functions attached to objects. Calling obj.method() is equivalent to Class.method(obj). For mutable objects: some methods CHANGE the object (e.g. list.sort()), some RETURN a value (e.g.…

### Defining and Calling Functions

- Snippet ID: `item:ks-e09d7f145b`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `ks-e09d7f145b`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Function definition and calling def keyword, function name, parameters in parentheses, colon, indented body. Call with round brackets (). Using [] gives TypeError 'not subscriptable'. Using [] on a list with () gives Ty…

### Defining and Calling Functions

- Snippet ID: `item:manual-call-vs-index`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `manual-call-vs-index`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What error do you get from `print[1]` and from `[1, 2, 3](0)`? `print[1]` tries to subscript a function, while `[1, 2, 3](0)` tries to call a list. Both raise `TypeError`, but for opposite reasons. print[1] [1, 2, 3](0)

### Defining and Calling Functions

- Snippet ID: `item:manual-list-of-dicts-loop`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `manual-list-of-dicts-loop`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do you access values when looping over a list of dictionaries? Each loop iteration gives one dictionary, so read fields with keys like `student['Name']` and `student['Grade']`. for student in students: print(student…

### Defining and Calling Functions

- Snippet ID: `item:manual-string-return-shape`
- Topic: Defining and Calling Functions
- Card ID: `w3-defining-and-calling-functions`
- Piece count: `1`

- `manual-string-return-shape`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do you recognize that a function should `return` a string instead of `print` it? If the result must be reused later, the function should `return` the string so the caller can store, combine, or print it afterwards.…

### Higher-Order Patterns

- Snippet ID: `item:cs-curated-hw-hof-nested-helper-hhi`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `cs-curated-hw-hof-nested-helper-hhi`
  Bucket: `additional` | Type: `source_notebook`
  Preview: A nested helper can hide repeated domain math inside one outer function def main(sales_before_entry): def calculate_hhi(sales_volumes): total_sales = sum(sales_volumes) return sum(round(100 * volume / total_sales) ** 2…

### Higher-Order Patterns

- Snippet ID: `item:exam-extra_practice-10-w3-higher-order-patterns`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `exam-extra_practice-10-w3-higher-order-patterns`
  Bucket: `additional` | Type: `source_exam`
  Preview: You need to write a function main(target_num, list_num) that returns all unique pairs of numbers that add up to target_num. Example: main(11, [4,5,6,9,3,7,2,8]) should return [(5,6),(4,7),(9,2),(3,8)]. Note: (6,5) is no…

### Higher-Order Patterns

- Snippet ID: `item:exam-intro_python_sample_final_24_25-16-w3-higher-order-patterns`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-16-w3-higher-order-patterns`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What would be printed by the following code snippet: print(list_1[0](1, 2) ** list_1[1](1, 2)) A B C D D list_1[0](1, 2) is 1 + 2 = 3. list_1[1](1, 2) is 1 * 2 = 2. 3 ** 2 = 9.

### Higher-Order Patterns

- Snippet ID: `item:exam-midterm_2023-11-w3-higher-order-patterns`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `exam-midterm_2023-11-w3-higher-order-patterns`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You need to write a function called sort_list that accepts a list of integers. The function should return a new list, in which the elements are sorted from highest to lowest based on their absolute values.

### Higher-Order Patterns

- Snippet ID: `item:exam-midterm_2023-13-w3-higher-order-patterns`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `exam-midterm_2023-13-w3-higher-order-patterns`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose you have the following functions, one to elevates a number to square and the second elevates to cube: def square(n): return (n**2) def cube(n): return (n**3) You want to apply both functions to the elements in a…

### Higher-Order Patterns

- Snippet ID: `item:exam-midterm_2024-19-w3-higher-order-patterns`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `exam-midterm_2024-19-w3-higher-order-patterns`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have four different blocks of code. Three of them return the same list, one of them returns something different. Which block of code prints something different than the other blocks print?

### Higher-Order Patterns

- Snippet ID: `item:exam-trial_midterm-17-w3-higher-order-patterns`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `exam-trial_midterm-17-w3-higher-order-patterns`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have four different blocks of code. Three of them return the same list, one of them returns something different. Which block of code prints something different than the other blocks print?

### Higher-Order Patterns

- Snippet ID: `item:ks-58858d6d96`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `ks-58858d6d96`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Lambda functions Anonymous one-line functions. Syntax: lambda params: expression. Equivalent to a regular def but more concise. Most useful with map, filter, reduce, sorted, max. Lambda basics add_two = lambda x, y: x +…

### Higher-Order Patterns

- Snippet ID: `item:ks-994a4083e3`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `ks-994a4083e3`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: function_factories def function_factory(increment): def adder(n1): return n1 + increment return adder add4 = function_factory(4) add5 = function_factory (5) print(add4(3)) print(add5(3))

### Higher-Order Patterns

- Snippet ID: `item:ks-f069ee6a0b`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `1`

- `ks-f069ee6a0b`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Nested functions and function factories Functions can be defined inside other functions. The inner function is only visible to the outer function. Functions are objects — a function can return another function (factory…

### Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)

- Snippet ID: `subtopic:w3-higher-order-patterns:w3-higher-order-patterns-core`
- Topic: Higher-Order Patterns
- Card ID: `w3-higher-order-patterns`
- Piece count: `11`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: Function factory def function_factory(increment): def adder(n1): return n1 + increment return adder add4 = function_factory(4) add5 = function_factory(5) print(add4(3)) # 7 print(add5(3)) # 8 Functions can be defined in…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: Lambda basics add_two = lambda x, y: x + y print(add_two(1, 2)) # 3 # Equivalent to: def add_two(x, y): return x + y Anonymous one-line functions. Syntax: lambda params: expression. Equivalent to a regular def but more…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: map() with lambda l1 = [1, 2, 3, 4, 5, 6] print(list(map(lambda x: x * 2, l1))) # [2, 4, 6, 8, 10, 12] # Need list() to convert map object to list Anonymous one-line functions. Syntax: lambda params: expression. Equival…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: `map` can combine multiple iterables left = [1, 2, 3] right = [10, 20, 30] print(list(map(lambda x, y: x + y, left, right))) A lambda can take multiple parameters, and `map(...)` then feeds one element from each iterabl…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: sorted_key l1 = ['a', 'B', 'c'] print(sorted(l1))
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: sorted_key l1 = ['ad', 'dc', 'ce'] print(sorted(l1))
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: sorted_builtins l1 = ['aaa', 'bb', 'c'] print(sorted(l1))
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: sorted_builtins l1 = ['aaa', 'bb', 'c'] print(sorted(l1, key=len))
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: Functions can be defined inside other functions. The inner function is only visible to the outer function. Functions are objects — a function can return another function (factory pattern).
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: Anonymous one-line functions. Syntax: lambda params: expression. Equivalent to a regular def but more concise. Most useful with map, filter, reduce, sorted, max.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Nested Functions, Factories, lambda, map, filter, reduce, and sorted(key=...)
  Preview: `lambda x: expr` names one element at a time, and `map(f, seq)` returns a lazy iterable. Wrap it in `list(...)` when you need to inspect or print the mapped results.

### Return Behavior

- Snippet ID: `item:exam-Resit 22/23-3-w3-return-behavior`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `exam-Resit 22/23-3-w3-return-behavior`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What will be printed by the following code segment? a b c d b The function checks if the type of each element `i` in the list `x` is the same as the type of `x` (which is a list). The only element in `x` that is a list…

### Return Behavior

- Snippet ID: `item:exam-Trial final - Introduction to Python - 22/23-3-w3-return-behavior`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `exam-Trial final - Introduction to Python - 22/23-3-w3-return-behavior`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What is the output of the following code segment? a b c d a The types of the elements are: 'abc' is str, 0 is int, None is NoneType, True is bool, 123.456 is float, 'False' is str (since it's in quotes), and {} is dict.

### Return Behavior

- Snippet ID: `item:exam-extra_practice-7-w3-return-behavior`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `exam-extra_practice-7-w3-return-behavior`
  Bucket: `recommended` | Type: `source_exam`
  Preview: def multiply(num1, num2): global result result = num1 * num2 print(multiply(2, 3)) print(result) a b c d b multiply() has no return statement, so it returns None. print(multiply(2,3)) prints None. But inside, global res…

### Return Behavior

- Snippet ID: `item:exam-extra_practice-9-w3-return-behavior`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `exam-extra_practice-9-w3-return-behavior`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Assume sum_even_in_list(l1) filters non-integers and sums even integers. You want sum_even_integers that accepts a flexible number of arguments. For example: sum_even_integers(1,'2', 3.0, 4) should return 4. Which of th…

### Return Behavior

- Snippet ID: `item:exam-midterm_2024-1-w3-return-behavior`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `exam-midterm_2024-1-w3-return-behavior`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Consider the following code snippet: a = True b = False c = True d = False if not (a or b) and (c or d): print("True") else: print("False") What will be printed by the code? A True B False C The code will result in an e…

### Return Behavior

- Snippet ID: `item:exam-trial-final-exam-py22-3-w3-return-behavior`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `exam-trial-final-exam-py22-3-w3-return-behavior`
  Bucket: `recommended` | Type: `source_exam`
  Preview: What will be returned by the following code segment? a b c d a The function checks if the type is exactly int. 1.0, 3.50 are floats, and '9' is a string, so they are replaced by None.

### Return Behavior

- Snippet ID: `item:kp-manual-mutating-methods-none-d1`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `kp-manual-mutating-methods-none-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Common `None` traps Code | What comes back function with no `return` hit | None l1.sort() | None l1.append(x) | None s.upper() | new string

### Return Behavior

- Snippet ID: `item:ks-00b2983ca8`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `ks-00b2983ca8`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Return statement Returns a value to the caller. If you don't capture the return value it's lost. A function leaves no traces — local names are gone after function ends. Common error: using print() instead of return in h…

### Return Behavior

- Snippet ID: `item:ks-14515a5856`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `ks-14515a5856`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Implicit return — None If a function reaches the end without a return statement, Python returns None automatically. This is bad practice but you must know it. Test with: if a != None: or if a is not None: Implicit None…

### Return Behavior

- Snippet ID: `item:ks-d1a2d7739d`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `ks-d1a2d7739d`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Single-element tuple (1) is NOT a tuple — it's just the integer 1. To create a 1-element tuple: t = (1,) or t = 1,. Neat swap trick: x, y = y, x 1-element tuple gotcha t1 = (1) print(type(t1) == tuple) # False print(typ…

### Return Behavior

- Snippet ID: `item:ks-db93da9e3e`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `1`

- `ks-db93da9e3e`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: pass keyword Does nothing. Used as a placeholder when an indented block is required but you have nothing to put there yet (stub). After a colon you must have an indented block — pass satisfies this. pass as stub def add…

### return, Implicit None, Multiple Returns, pass, and Single-Element Tuples

- Snippet ID: `subtopic:w3-return-behavior:w3-return-behavior-core`
- Topic: Return Behavior
- Card ID: `w3-return-behavior`
- Piece count: `13`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Returning a tuple (multiple values) def powers(n1): return n1 ** 2, n1 ** 3 # returns a tuple power2, power3 = powers(3) print(power2, power3) # 9 27 Returns a value to the caller. If you don't capture the return value…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Implicit None return def adder(n1, n2): if type(n1) == type(n2) == int: total = n1 + n2 return total a = adder('1', 2) # Returns None (no return hit) print(a) # None If a function reaches the end without a return statem…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: 1-element tuple gotcha t1 = (1) print(type(t1) == tuple) # False print(type(t1) == int) # True t1 = (1,) # correct 1-element tuple t1 = 1, # also correct x, y = y, x # swap using tuple unpacking (1) is NOT a tuple — it'…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Mutating method returns `None` l1 = [3, 1, 2] result = l1.sort() print(result) print(l1) A missing `return` is not the only source of `None`: mutating methods such as `sort()` often change the object in place and return…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Function return value and trace def adder(n1, n2): return n1 + n2 a = adder(1,2) print(a) Trace the returned value, not just what gets printed while the function runs.
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Computed a local variable but forgot to return it def adder(n1, n2): total = n1 + n2 a = adder(1, 2) print(a) Trace the returned value, not just what gets printed while the function runs.
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: A tuple return stays one tuple value def powers(n1): return n1 ** 2, n1 ** 3 a = powers(3) print(a) Trace the returned value, not just what gets printed while the function runs.
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Unpack a tuple return into multiple names def powers(n1): return n1 ** 2, n1 ** 3 power2, power3 = powers(3) print(power2, power3) Trace the returned value, not just what gets printed while the function runs.
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Returns a value to the caller. If you don't capture the return value it's lost. A function leaves no traces — local names are gone after function ends. Common error: using print() instead of return in homework functions.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: If a function reaches the end without a return statement, Python returns None automatically. This is bad practice but you must know it. Test with: if a != None: or if a is not None:
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: (1) is NOT a tuple — it's just the integer 1. To create a 1-element tuple: t = (1,) or t = 1,. Neat swap trick: x, y = y, x
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: Does nothing. Used as a placeholder when an indented block is required but you have nothing to put there yet (stub). After a colon you must have an indented block — pass satisfies this.
- `kp-manual-mutating-methods-none`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: return, Implicit None, Multiple Returns, pass, and Single-Element Tuples
  Preview: A missing `return` is not the only source of `None`: many mutating methods also return `None`. Keep the mutated object, not the method call result.

### Global vs Local Names and Scope Errors

- Snippet ID: `subtopic:w3-scope:w3-scope-core`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `4`

- `manual-scope-global-change`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Global vs Local Names and Scope Errors
  Preview: Use `global` to rebind a global name n1 = 1 def changer(): global n1 n1 = n1 + 1 changer() print(n1) With `global n1`, the assignment updates the global name instead of creating a local one. 2
- `manual-scope-local-name`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Global vs Local Names and Scope Errors
  Preview: Local names disappear after the call def adder(n1, n2): return n1 + n2 print(adder(1, 2)) print(n1) After the function call, `n1` and `n2` no longer exist outside the function body. Return the value if the caller needs…
- `manual-scope-rebind-parameter`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Global vs Local Names and Scope Errors
  Preview: Rebinding a parameter does not change the caller's name def changer(n1): n1 = n1 + 1 return n1 a = 1 a = changer(a) print(a) The function works with its local parameter; the caller changes only because the returned valu…
- `manual-scope-unbound`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Global vs Local Names and Scope Errors
  Preview: Assignment makes the name local b = 1 def main(a): b = b return a print(main(1)) Because `b` is assigned inside `main`, Python treats it as local before the `b = b` line runs. UnboundLocalError

### Scope

- Snippet ID: `item:exam-Resit 22/23-2-w3-scope`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-Resit 22/23-2-w3-scope`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Executing the following program will produce an error. Why? a b c d a The variable `result` is defined inside the `power` function, giving it local scope. It cannot be accessed outside the function in the global scope w…

### Scope

- Snippet ID: `item:exam-Test Resit - Introduction to Python - 22/23-2-w3-scope`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-Test Resit - Introduction to Python - 22/23-2-w3-scope`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Executing the following program will produce an error. Why? a b c d d The variable 'result' is defined inside the scope of the 'power' function and is therefore a local variable. It cannot be accessed outside the functi…

### Scope

- Snippet ID: `item:exam-Trial final - Introduction to Python - 22/23-2-w3-scope`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-Trial final - Introduction to Python - 22/23-2-w3-scope`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Calling the function func_1() will produce an error. Which line of the following code segment produces the error? a b c d a var_1 is a local variable inside func_2, so it is not accessible in the scope of func_1. Furthe…

### Scope

- Snippet ID: `item:exam-extra_practice-2-w3-scope`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-extra_practice-2-w3-scope`
  Bucket: `recommended` | Type: `source_exam`
  Preview: val = 2 def func(): val = 3 print(val) func() print(val) Which of the following code snippets produces the same output as the above code snippet? a b c d c Original output: 3, 2. Option a: UnboundLocalError (val1 used b…

### Scope

- Snippet ID: `item:exam-intro_python_sample_final_24_25-15-w2-conditions`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-15-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Executing the following program will produce an error. Why? A B C D A The variable 'result' is defined inside the 'cube' function, making it local to that function. It cannot be accessed from the global scope.

### Scope

- Snippet ID: `item:exam-midterm_2023-3-w3-scope`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-midterm_2023-3-w3-scope`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which other program will give the same output as the following code snippet?

### Scope

- Snippet ID: `item:exam-midterm_2024-5-w3-scope`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-midterm_2024-5-w3-scope`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which other program will produce the same output as the following code snippet?

### Scope

- Snippet ID: `item:exam-trial-final-exam-py22-2-w3-scope`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `exam-trial-final-exam-py22-2-w3-scope`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Take a look at the following code segment. Will executing this code segment produce an error? If yes, then why? a b c d b The global variable 'a' is accessible inside the inner function without error. The code evaluates…

### Scope

- Snippet ID: `item:kp-manual-scope-global`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `kp-manual-scope-global`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Use `global x` only when the function should rebind the global name `x`; mutating an object passed in as an argument does not require `global`.

### Scope

- Snippet ID: `item:kp-manual-scope-local`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `kp-manual-scope-local`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Names assigned inside a function are local by default, including parameter names.

### Scope

- Snippet ID: `item:kp-manual-scope-return-outside`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `kp-manual-scope-return-outside`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: A local variable disappears after the function ends. If you need that value outside the function, return it and assign the result in the caller.

### Scope

- Snippet ID: `item:kp-manual-scope-unbound`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `kp-manual-scope-unbound`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: If a function assigns to a name anywhere, Python treats that name as local throughout that function unless `global` or `nonlocal` says otherwise.

### Scope

- Snippet ID: `item:ks-2a6510492d`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `ks-2a6510492d`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Global and local scope Local names: defined inside a function (parameter names + any assignment inside). Only known inside the function. Global names: defined outside any function, known everywhere EXCEPT when a same-na…

### Scope

- Snippet ID: `item:manual-global`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `manual-global`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: When do you need `global`? Use `global name` only when the function should rebind a global variable; simple reads of a global name do not need it. n1 = 1 def changer(): global n1 n1 = n1 + 1

### Scope

- Snippet ID: `item:manual-local-name`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `manual-local-name`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Why does `print(n1)` fail outside `def adder(n1, n2): ...`? Parameter names are local to the function body, so they do not exist in the global scope after the call finishes. def adder(n1, n2): return n1 + n2 adder(1, 2)…

### Scope

- Snippet ID: `item:manual-unboundlocal`
- Topic: Scope
- Card ID: `w3-scope`
- Piece count: `1`

- `manual-unboundlocal`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Why can assigning to a name inside a function cause `UnboundLocalError`? If a function assigns to a name anywhere in its body, Python treats that name as local throughout the function unless you declare it `global` or `…

## Week 4

Snippet families in this group: **47**

### Error Handling

- Snippet ID: `item:ks-2c73fabc68`
- Topic: Error Handling
- Card ID: `w4-error-handling`
- Piece count: `1`

- `ks-2c73fabc68`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Error Handling: try-except The try block lets you test a block of code for errors, and the except block lets you handle the error without the program crashing. Handling a ValueError s = 'abc' try: idx = s.index('z') exc…

### Error Handling

- Snippet ID: `item:ks-40d373c410`
- Topic: Error Handling
- Card ID: `w4-error-handling`
- Piece count: `1`

- `ks-40d373c410`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: The raise Keyword You can use 'raise' to manually trigger an exception when a specific condition occurs. Raising an error def check_positive(n): if n < 0: raise ValueError('Number must be positive') return n

### try/except and raise

- Snippet ID: `subtopic:w4-error-handling:w4-error-handling-core`
- Topic: Error Handling
- Card ID: `w4-error-handling`
- Piece count: `7`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: try/except and raise
  Preview: Handling a ValueError s = 'abc' try: idx = s.index('z') except ValueError: idx = -1 The try block lets you test a block of code for errors, and the except block lets you handle the error without the program crashing.
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: try/except and raise
  Preview: Raising an error def check_positive(n): if n < 0: raise ValueError('Number must be positive') return n You can use 'raise' to manually trigger an exception when a specific condition occurs.
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: try/except and raise
  Preview: def my_find(s,needle): def my_find(s,needle): if (result := s.find(needle)) == -1: raise ValueError("substring not found") return result s1 ='abcdefghabcdefgh' print(my_find(s1, 'e')) print(my_find(s1, 'i')) Trace the r…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: try/except and raise
  Preview: def my_index(s,needle): def my_index(s,needle): try: result = s.index(needle) except: result = -1 return result s1 ='abcdefghabcdefgh' print(my_index(s1, 'e')) print(my_index(s1, 'i')) Trace the returned value, not just…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: try/except and raise
  Preview: The try block lets you test a block of code for errors, and the except block lets you handle the error without the program crashing.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: try/except and raise
  Preview: You can use 'raise' to manually trigger an exception when a specific condition occurs.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: try/except and raise
  Preview: Catch the specific exception you expect when you know the failure mode. `except ValueError` documents the substring-missing case more clearly than a bare `except:`.

### Class Definition, __init__, self, and Attribute Basics

- Snippet ID: `subtopic:w4-oop-fundamentals:w4-oop-fundamentals-core`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `16`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Defining a simple class class Car: def __init__(self, color): self.color = color A class defines methods and attribute layout; `__init__` runs when you create an object and stores instance data on `self`.
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Using self to access attributes class Dog: def __init__(self, name): self.name = name def bark(self): return f'{self.name} says woof!' `self` refers to the current instance, so instance methods read and write data throu…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Shared class attribute class Counter: count = 0 def __init__(self): Counter.count += 1 `self.x` is per object; a class attribute is shared until an instance shadows it with its own value.
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: `self` is passed automatically in method calls class Clock: def set_hour(self, hour): self.hour = hour c = Clock() c.set_hour(9) # c.set_hour(c, 9) # wrong: passes one argument too many Writing `obj.method(x)` already p…
- `manual-oop-attrs`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Class attribute vs instance attribute class Rectangle: units = 'cm' def __init__(self, width): self.width = width r1 = Rectangle(3) r2 = Rectangle(5) r2.units = 'm' print(r1.units, r2.units) `self.width` is per object;…
- `manual-oop-compare-none-case`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Return `None` when neither object clearly wins class Book: def __init__(self, title, scores): self.title = title self.scores = scores def average(self): return sum(self.scores) / len(self.scores) def winner_against(self…
- `manual-oop-constructor-defaults`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Constructor defaults belong in `__init__` parameters class Vehicle: def __init__(self, name, mode="land"): self.name = name self.mode = mode car = Vehicle("Mazda") print(car.name, car.mode) Default constructor arguments…
- `manual-oop-init-defaults`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Safe default state in `__init__` class Book: def __init__(self, title, review_scores=None): self.title = title self.review_scores = [] if review_scores is None else review_scores Constructor defaults can make arguments…
- `manual-oop-state-compare`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Trace `self` state across multiple method calls class Book: def __init__(self, title): self.title = title self.scores = [] def add_review(self, score): self.scores.append(score) def average(self): return sum(self.scores…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: A class defines methods and attribute layout; `__init__` runs when you create an object and stores instance data on `self`.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: `self` refers to the current instance, so instance methods read and write data through `self.attr`.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: `self.x` is per object; a class attribute is shared until an instance shadows it with its own value.
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Method calls pass `self` automatically: `obj.set_date(x)` is correct; `obj.set_date(obj, x)` passes one argument too many.
- `kp-manual-init-defaults`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Constructor defaults can make arguments optional, but mutable per-instance state should start from `None` and be created inside `__init__`.
- `kp-manual-oop-compare`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Comparison methods often combine state from `self` and `other`. Write the winning condition(s) explicitly, and return a clear fallback such as `None` when neither object clearly wins.
- `kp-manual-self-attr`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Class Definition, __init__, self, and Attribute Basics
  Preview: Use `self.attr = ...` to store per-object state. A bare assignment like `attr = ...` inside a method only creates or updates a local variable.

### OOP Fundamentals

- Snippet ID: `item:cs-0d319e4faf`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `cs-0d319e4faf`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: class Rectangle: class Rectangle: total_size = 0 def __init__(self, length, width=1): self.length = length self.width = width Rectangle.total_size += self.length * self.width print(f'{self.length} by {self.width} create…

### OOP Fundamentals

- Snippet ID: `item:cs-30e53467b8`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `cs-30e53467b8`
  Bucket: `additional` | Type: `source_notebook`
  Preview: class Rectangle: class Rectangle: total_size = 0 def __init__(self, length, width=1): self.length = length self.width = width Rectangle.total_size += self.length * self.width print(f'rectangle {self.length} by {self.wid…

### OOP Fundamentals

- Snippet ID: `item:exam-Test Exam 07-06-22-1-w4-oop-fundamentals`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `exam-Test Exam 07-06-22-1-w4-oop-fundamentals`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Given the class definition above, trying to execute the following two code lines will result in a Python error. my_flight = Flight("KLM", "Amsterdam", "Paris") # Code line 1 my_flight.set_date(my_flight, "29-02-2022") #…

### OOP Fundamentals

- Snippet ID: `item:exam-Test Exam 07-06-22-2-w4-oop-fundamentals`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `exam-Test Exam 07-06-22-2-w4-oop-fundamentals`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose that you also want to write a method called compare that compares the book to another book and gives a recommendation for which one to read. A book is better than another book if its average review score is high…

### OOP Fundamentals

- Snippet ID: `item:exam-Trial final exam Introduction to Python-1-w4-oop-fundamentals`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `exam-Trial final exam Introduction to Python-1-w4-oop-fundamentals`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You'd like to define a class called Vehicle. It should have two attributes: "name" and "mode", which you want to be initialized at the time of object construction. The "name" attribute can be any string, and it must be…

### OOP Fundamentals

- Snippet ID: `item:exam-Trial final exam Introduction to Python-2-w4-oop-fundamentals`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `exam-Trial final exam Introduction to Python-2-w4-oop-fundamentals`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Take a look at the following class definition. Suppose that we create a Book object and call its add_review method three times, like this: book_1 = Book("The Lightning Thief", "Rick Riordan") book_1.add_review(5) book_1…

### OOP Fundamentals

- Snippet ID: `item:exam-intro_python_sample_final_24_25-1-w5-pandas-core-structures`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-1-w5-pandas-core-structures`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You'd like to define a class called Vehicle. It should have two attributes: name and mode, which you want to be initialized during object creation. The name attribute can be any string, and it must be passed to the obje…

### OOP Fundamentals

- Snippet ID: `item:exam-intro_python_sample_final_24_25-2-w5-pandas-core-structures`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-2-w5-pandas-core-structures`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose that we create a Book object and call its add_review method three times, like this: book_1 = Book("The Lightning Thief", "Rick Riordan"), book_1.add_review(5), book_1.add_review(3), book_1.add_review(3). What wi…

### OOP Fundamentals

- Snippet ID: `item:kp-manual-init-defaults-d1`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `kp-manual-init-defaults-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Optional constructor argument class Vehicle: def __init__(self, name, mode='land'): self.name = name self.mode = mode

### OOP Fundamentals

- Snippet ID: `item:kp-manual-init-defaults-d2`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `kp-manual-init-defaults-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Fresh list per object class Book: def __init__(self, title, review_scores=None): self.title = title self.review_scores = [] if review_scores is None else review_scores

### OOP Fundamentals

- Snippet ID: `item:kp-manual-oop-compare-d1`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `kp-manual-oop-compare-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Comparison method template Case | Return self score > other score | winner based on `self` self score < other score | winner based on `other` tie / no clear winner | explicit fallback such as `None`

### OOP Fundamentals

- Snippet ID: `item:kp-manual-self-attr-d1`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `kp-manual-self-attr-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Store state on `self`, not in a local class Counter: def __init__(self): self.count = 0 def bump(self): count = self.count + 1 self.count = count

### OOP Fundamentals

- Snippet ID: `item:ks-06b21ad349`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `ks-06b21ad349`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Class Definition and __init__ A class is a blueprint. The __init__ method is the constructor called automatically when a new object is created to initialize attributes. Defining a simple class class Car: def __init__(se…

### OOP Fundamentals

- Snippet ID: `item:ks-5cbba26b09`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `ks-5cbba26b09`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Class vs Instance Attributes Instance attributes (self.x) are unique to each object. Class attributes are defined outside methods and shared by all instances of the class. Shared class attribute class Counter: count = 0…

### OOP Fundamentals

- Snippet ID: `item:ks-9e278d1ee6`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `ks-9e278d1ee6`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: The self Parameter In class methods, 'self' refers to the specific instance of the object. It must be the first parameter of any instance method. Using self to access attributes class Dog: def __init__(self, name): self…

### OOP Fundamentals

- Snippet ID: `item:manual-init-default`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `manual-init-default`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do default values in `__init__` make constructor arguments optional? A default like `vehicle_mode='land'` can be omitted when the object is created, but the instance still receives that attribute value. class Vehicl…

### OOP Fundamentals

- Snippet ID: `item:manual-method-call`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `manual-method-call`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Why does `obj.set_date(obj, x)` pass too many arguments? When you call a method on an object, Python passes the object as `self` automatically. Writing it again adds one argument too many. obj.set_date(x) # correct obj.…

### OOP Fundamentals

- Snippet ID: `item:manual-self`
- Topic: OOP Fundamentals
- Card ID: `w4-oop-fundamentals`
- Piece count: `1`

- `manual-self`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Why is `self` the first parameter of an instance method? `self` is the current object, so the method can read and update that object's attributes. class Flight: def set_date(self, date): self.date = date

### f-strings Basics, Formatting, and Debug Form

- Snippet ID: `subtopic:w4-string-formatting:w4-string-formatting-core`
- Topic: String Formatting
- Card ID: `w4-string-formatting`
- Piece count: `10`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Simple f-string name = 'Jan' print(f'{name} studies Python.') # 'Jan studies Python.' F-strings (formatted string literals) allow embedding expressions inside curly braces {}. They are more readable than traditional con…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Debug shortcut val = 10 print(f'{val=}') # 'val=10' Using f'{var=}' is a convenient shortcut for debugging that prints both the variable name and its value.
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Zero-padding an integer num = 7 print(f'{num:03d}') # '007' You can specify formatting after a colon, such as padding numbers with zeros.
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Using `.format(...)` with placeholders name = 'Jan' score = 7 print('Student {} scored {:03d}'.format(name, score)) The official resit material still uses `.format(...)`, so it is worth recognizing positional placeholde…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Build formatted output with custom separators cities = ['Amsterdam', 'Utrecht', 'Leiden'] text = ', '.join(cities[:-1]) + ', and ' + cities[-1] print(f'Visited: {text}') print('Average: {:.1f}'.format(7.25)) When the ou…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: F-strings (formatted string literals) allow embedding expressions inside curly braces {}. They are more readable than traditional concatenation.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Using f'{var=}' is a convenient shortcut for debugging that prints both the variable name and its value.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: You can specify formatting after a colon, such as padding numbers with zeros.
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Official assessments also use `.format(...)` placeholders. The same width and zero-padding ideas still apply there, for example `'{:04d}'.format(n)`.
- `kp-5`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: f-strings Basics, Formatting, and Debug Form
  Preview: Use f-strings for direct interpolation and `.format(...)` when the template string already exists; both support width, alignment, and precision specs such as `{:03d}` and `{:.2f}`.

### String Formatting

- Snippet ID: `item:ks-72dda5450c`
- Topic: String Formatting
- Card ID: `w4-string-formatting`
- Piece count: `1`

- `ks-72dda5450c`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: F-strings Basics F-strings (formatted string literals) allow embedding expressions inside curly braces {}. They are more readable than traditional concatenation. Simple f-string name = 'Jan' print(f'{name} studies Pytho…

### String Formatting

- Snippet ID: `item:ks-acb7f400b2`
- Topic: String Formatting
- Card ID: `w4-string-formatting`
- Piece count: `1`

- `ks-acb7f400b2`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: F-strings Formatting You can specify formatting after a colon, such as padding numbers with zeros. Zero-padding an integer num = 7 print(f'{num:03d}') # '007'

### String Formatting

- Snippet ID: `item:ks-ea5a4acb43`
- Topic: String Formatting
- Card ID: `w4-string-formatting`
- Piece count: `1`

- `ks-ea5a4acb43`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: F-strings Debugging Using f'{var=}' is a convenient shortcut for debugging that prints both the variable name and its value. Debug shortcut val = 10 print(f'{val=}') # 'val=10'

### Quotes, Escape Characters, and Immutability

- Snippet ID: `subtopic:w4-string-fundamentals:w4-string-fundamentals-core`
- Topic: String Fundamentals
- Card ID: `w4-string-fundamentals`
- Piece count: `8`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: Methods return new strings s1 = 'abcd' s1.capitalize() # Returns 'Abcd' print(s1) # Still prints 'abcd' Strings are immutable: methods like `.upper()` and `.replace()` return a new string, so assign the result back if y…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: Newlines and tabs print('Line 1\nLine 2\tTabbed') print("It\'s a string") Escape sequences: `\n` newline, `\t` tab, and `\'` or `\"` for literal quotes.
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: Filter uppercase letters with a helper function def my_isupper(s1): for el in s1: if el not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": return False return True x = "Harry Potter and the Philosopher's Stone" y = '' for i in x: if…
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: `len(s)` counts characters a = 'adbc' print(len(a)) Count every character in the string, including letters, spaces, and punctuation if they are present. 4
- `manual-string-literals-example`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: Quotes and newline escapes print("it's") print('He said "hi"') print("Line 1\nLine 2") Use matching quotes or escape the inner quote; `\n` inserts a newline. it's He said "hi" Line 1 Line 2
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: Strings are immutable: methods like `.upper()` and `.replace()` return a new string, so assign the result back if you want the change to stick.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: Escape sequences: `\n` newline, `\t` tab, and `\'` or `\"` for literal quotes.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Quotes, Escape Characters, and Immutability
  Preview: Strings are immutable: `s[0] = 'A'` fails, so rebuild or rebind, for example `s = 'A' + s[1:]`.

### String Fundamentals

- Snippet ID: `item:cs-14245b8c1f`
- Topic: String Fundamentals
- Card ID: `w4-string-fundamentals`
- Piece count: `1`

- `cs-14245b8c1f`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: def my_isupper(s1): def my_isupper(s1): for el in s1: if el not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ": return False return True x = "Harry Potter and the Philosopher's Stone" y = '' for i in x: if my_isupper(i): y += i print(…

### String Fundamentals

- Snippet ID: `item:cs-e7bc165499`
- Topic: String Fundamentals
- Card ID: `w4-string-fundamentals`
- Piece count: `1`

- `cs-e7bc165499`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: def main(a, b): def main(a, b): return f'''The first number is: {a:04d} The second number is: {b:04d} The product is: {a * b:04d}''' print(main(7,13)) The first number is: 0007 The second number is: 0013 The product is:…

### String Fundamentals

- Snippet ID: `item:ks-309158a68c`
- Topic: String Fundamentals
- Card ID: `w4-string-fundamentals`
- Piece count: `1`

- `ks-309158a68c`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Escape Characters Special characters like newlines (\n), tabs (\t), or literal quotes can be included using the backslash (\). Newlines and tabs print('Line 1\nLine 2\tTabbed') print("It\'s a string")

### String Fundamentals

- Snippet ID: `item:ks-b734a22f46`
- Topic: String Fundamentals
- Card ID: `w4-string-fundamentals`
- Piece count: `1`

- `ks-b734a22f46`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: String Immutability Strings in Python are immutable, meaning they cannot be changed in place. Methods like upper() or replace() return a new string object rather than modifying the original. Attempting to change a strin…

### String Fundamentals

- Snippet ID: `item:manual-string-escapes`
- Topic: String Fundamentals
- Card ID: `w4-string-fundamentals`
- Piece count: `1`

- `manual-string-escapes`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do you include quotes or a newline inside a string literal? Pick the other quote style or escape the inner quote; use `\n` for a newline. print("it's") print('He said "hi"') print("Line 1\nLine 2")

### String Fundamentals

- Snippet ID: `item:manual-string-immutability`
- Topic: String Fundamentals
- Card ID: `w4-string-fundamentals`
- Piece count: `1`

- `manual-string-immutability`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Why does `s[0] = 'A'` fail? Strings are immutable, so you must build a new string such as `s = 'A' + s[1:]` instead of assigning by index. s = 'abcd' s = 'A' + s[1:]

### Slicing with Step, Search, replace, join, strip, and the string Module

- Snippet ID: `subtopic:w4-string-operations-and-methods:w4-string-operations-and-methods-core`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `23`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Behavior when substring is missing s = 'abc' print(s.find('z')) # -1 # print(s.index('z')) # Raises ValueError Both find() and index() search for a substring. The key difference is that find() returns -1 if the substrin…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Slicing examples s = '01234567' print(s[::4]) # '04' print(s[::-2]) # '7531' Slicing allows a third parameter 'step'. s[::2] takes every second character, while s[::-1] reverses the string.
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Joining a list into a string words = ['a', 'b', 'c'] print('-'.join(words)) # 'a-b-c' print(''.join(words)) # 'abc' The join() method takes an iterable (like a list) and concatenates its elements using the string it is…
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Limiting replacements s = 'aaaa' print(s.replace('a', 'b', 2)) # 'bbaa' Replaces occurrences of a substring. It accepts an optional 'count' argument to limit the number of replacements.
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Importing string constants import string print(string.ascii_lowercase) # 'abcdef...' print(string.digits) # '0123456789' The 'string' module provides pre-defined constants like all lowercase letters, digits, and punctua…
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Stripping whitespace and characters s = ' abc ' print(s.strip()) # 'abc' s2 = 'eeabcdee' print(s2.strip('e')) # 'abcd' strip() removes leading and trailing characters. lstrip() and rstrip() target the left and right sid…
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: s1 = 'abcdefghabcdefgh' s1 = 'abcdefghabcdefgh' print(s1.find('i')) print(s1[s1.find('i')]) print(s1.index('i'))
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: s1 = 'abcdefghabcdefgh' s1 = 'abcdefghabcdefgh' print(s1.find('e')) print(s1.index('e', 5)) print(s1.find('e', 5, 10)) print(s1.index('e', 5, 13)) print(s1.find('ef')) print(s1.index('q'))
- `manual-string-format-method`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Build strings with `.format(...)` template = "{} scored {} points" print(template.format("Ada", 9)) Use `.format(...)` on the template string, and remember it returns a new string instead of changing the original text i…
- `manual-string-indexing-reference`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Indexing, negative indices, and slices s = 'python' print(s[0], s[-1]) print(s[1:4]) print(s[::2]) print(s[::-1]) This compact reference covers the most repeated string-selection patterns: direct indexing, negative inde…
- `manual-string-islower-method`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Check lowercase letters with `.islower()` print("amsterdam".islower()) print("Amsterdam".islower()) print("123".islower()) `.islower()` only returns `True` when the string contains at least one cased character and all c…
- `manual-string-output-construction`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Join values into exam-style output text names = ['Ada', 'Bob', 'Cleo'] body = ', '.join(names[:-1]) print(f'{body}, and {names[-1]}') print('{:.2f}'.format(3.5)) Use `join` for the repeated separator, then add the custo…
- `manual-string-repetition`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Repeat text with string multiplication print(3 * "ha") print("ab" * 2) Both `n * text` and `text * n` repeat the string `n` times, which is a common concise exam pattern. hahaha abab
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Both find() and index() search for a substring. The key difference is that find() returns -1 if the substring is not found, while index() raises a ValueError.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Slicing allows a third parameter 'step'. s[::2] takes every second character, while s[::-1] reverses the string.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: The join() method takes an iterable (like a list) and concatenates its elements using the string it is called on as a separator.
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Replaces occurrences of a substring. It accepts an optional 'count' argument to limit the number of replacements.
- `kp-5`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: The 'string' module provides pre-defined constants like all lowercase letters, digits, and punctuation.
- `kp-6`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: strip() removes leading and trailing characters. lstrip() and rstrip() target the left and right sides respectively.
- `kp-7`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Pattern to remember: `find` returns `-1`; `index` raises `ValueError` if the substring is missing.
- `kp-8`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Indexing and slicing are exam staples: `s[i]` gets one character, `s[-1]` starts from the end, and slices use an exclusive stop with optional step values such as `s[1:5]`, `s[::2]`, and `s[::-1]`.
- `kp-9`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: Boolean string predicates answer slightly different questions: `.islower()` and `.isupper()` need at least one cased character, `.isdigit()` checks digits only, and spaces or punctuation usually make the result `False`.
- `kp-manual-string-method-results`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Slicing with Step, Search, replace, join, strip, and the string Module
  Preview: String methods like `replace`, `capitalize`, `split`, and `join` return new values; the original string stays unchanged unless you assign the result.

### String Operations and Methods

- Snippet ID: `item:exam-intro_python_sample_final_24_25-22-w2-conditions`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-22-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which script, using the count string method, would print the value 1 for x = 'Amsterdam'? A B C D B The count() method is a string method, not a standalone function. It is called using the dot notation on a string objec…

### String Operations and Methods

- Snippet ID: `item:exam-intro_python_sample_final_24_25-4-w2-conditions`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-4-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which of the following code segments does NOT achieve the goal of returning a string with 10 digits by removing dashes? A B C D A Strings in Python are immutable. The .replace() method returns a new string but does not…

### String Operations and Methods

- Snippet ID: `item:kp-5-d1`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `5`

- `kp-5-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Importing string constants import string print(string.ascii_lowercase) # 'abcdef...' print(string.digits) # '0123456789'
- `kp-5-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Formatting patterns at a glance Goal | f-string | .format(...) insert a value | f'{name}' | '{}'.format(name) zero-pad an int | f'{n:03d}' | '{:03d}'.format(n) 2 decimals | f'{x:.2f}' | '{:.2f}'.format(x)
- `kp-5-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Filter by condition df[df['Weight'] > 60] df.loc[df.Age < 155]
- `kp-5-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Formatting with map df['W_g'] = df['Weight'].map(lambda x: f'{x*1000} g')
- `kp-5-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Equivalent logic using map/filter l2 = list(map(lambda x: x*2, filter(lambda x: x%3 != 0, [1, 2, 3, 4])))

### String Operations and Methods

- Snippet ID: `item:kp-8-d1`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `2`

- `kp-8-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Indexing and slicing quick rules Pattern | Meaning | Trap s[0], s[-1] | first / last character | single-index access can raise IndexError s[a:b] | start inclusive, stop exclusive | safe even if b is past the end s[::2]…
- `kp-8-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Divide by index plus offset res = [val // (i + 6) for i, val in enumerate([46, 48])]

### String Operations and Methods

- Snippet ID: `item:kp-9-d1`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `kp-9-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Predicate truth table Input | Check | Result 'abc'.islower() | all cased chars lowercase | True 'Abc'.islower() | contains uppercase | False '123'.isdigit() | all chars are digits | True 'abc!'.islower() | punctuation i…

### String Operations and Methods

- Snippet ID: `item:kp-manual-string-method-results-d1`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `kp-manual-string-method-results-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: replace() returns a new string number = '020-525-1400' cleaned = number.replace('-', '') print(number) # '020-525-1400' print(cleaned) # '0205251400'

### String Operations and Methods

- Snippet ID: `item:ks-45aead894c`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `ks-45aead894c`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: The replace Method Replaces occurrences of a substring. It accepts an optional 'count' argument to limit the number of replacements. Limiting replacements s = 'aaaa' print(s.replace('a', 'b', 2)) # 'bbaa'

### String Operations and Methods

- Snippet ID: `item:ks-5198d93ec1`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `ks-5198d93ec1`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: String Searching: find vs index Both find() and index() search for a substring. The key difference is that find() returns -1 if the substring is not found, while index() raises a ValueError. Behavior when substring is m…

### String Operations and Methods

- Snippet ID: `item:ks-bdea67862f`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `ks-bdea67862f`
  Bucket: `additional` | Type: `source_lecture`
  Preview: The string Module The 'string' module provides pre-defined constants like all lowercase letters, digits, and punctuation. Importing string constants import string print(string.ascii_lowercase) # 'abcdef...' print(string…

### String Operations and Methods

- Snippet ID: `item:ks-cdb152720e`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `ks-cdb152720e`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: The join Method The join() method takes an iterable (like a list) and concatenates its elements using the string it is called on as a separator. Joining a list into a string words = ['a', 'b', 'c'] print('-'.join(words)…

### String Operations and Methods

- Snippet ID: `item:ks-e4dc502d3e`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `ks-e4dc502d3e`
  Bucket: `additional` | Type: `source_lecture`
  Preview: String Stripping strip() removes leading and trailing characters. lstrip() and rstrip() target the left and right sides respectively. Stripping whitespace and characters s = ' abc ' print(s.strip()) # 'abc' s2 = 'eeabcd…

### String Operations and Methods

- Snippet ID: `item:ks-f80f1bf556`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `ks-f80f1bf556`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: String Slicing with Step Slicing allows a third parameter 'step'. s[::2] takes every second character, while s[::-1] reverses the string. Slicing examples s = '01234567' print(s[::4]) # '04' print(s[::-2]) # '7531'

### String Operations and Methods

- Snippet ID: `item:manual-find-vs-index`
- Topic: String Operations and Methods
- Card ID: `w4-string-operations-and-methods`
- Piece count: `1`

- `manual-find-vs-index`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What is the difference between `s.find(x)` and `s.index(x)` when `x` is missing? `find` returns `-1`; `index` raises `ValueError`. s = 'banana' print(s.find('x')) print(s.index('x')) # ValueError

## Week 5

Snippet families in this group: **55**

### Combining Data

- Snippet ID: `item:cs-b46633d18d`
- Topic: Combining Data
- Card ID: `w5-combining-data`
- Piece count: `1`

- `cs-b46633d18d`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd dftax = pd.DataFrame({'Name':['A', 'B', 'C'], 'Income':[100, 200, 150], 'Tax':[10, 60, 30], 'City':['Amsterdam', 'Rotterdam', 'London']} ) #print(dftax) dfprov = pd.DataFrame({'Ci…

### Combining Data

- Snippet ID: `item:ks-21496ff1cd`
- Topic: Combining Data
- Card ID: `w5-combining-data`
- Piece count: `1`

- `ks-21496ff1cd`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Merging Database-style joins using .merge(). 'how' determines the type (left, right, inner, outer). Left join on a key df1.merge(df2, on='Town', how='left')

### Combining Data

- Snippet ID: `item:ks-591dd1aa33`
- Topic: Combining Data
- Card ID: `w5-combining-data`
- Piece count: `1`

- `ks-591dd1aa33`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Concatenation Gluing DataFrames together using pd.concat(). Vertical stack pd.concat([df1, df2], axis=0)

### Combining Data

- Snippet ID: `item:ks-f1be187b50`
- Topic: Combining Data
- Card ID: `w5-combining-data`
- Piece count: `1`

- `ks-f1be187b50`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Grouping The Split-Apply-Combine pattern using .groupby(). Grouped aggregation df.groupby('Nationality')['Height'].median()

### Concatenation, Merging, and Grouping

- Snippet ID: `subtopic:w5-combining-data:w5-combining-data-core`
- Topic: Combining Data
- Card ID: `w5-combining-data`
- Piece count: `8`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: Vertical stack pd.concat([df1, df2], axis=0) Gluing DataFrames together using pd.concat().
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: Left join on a key df1.merge(df2, on='Town', how='left') Database-style joins using .merge(). 'how' determines the type (left, right, inner, outer).
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: Grouped aggregation df.groupby('Nationality')['Height'].median() The Split-Apply-Combine pattern using .groupby().
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: import pandas as pd import pandas as pd dftax = pd.DataFrame({'Name':['A', 'B', 'C'], 'Income':[100, 200, 150], 'Tax':[10, 60, 30], 'City':['Amsterdam', 'Rotterdam', 'London']} ) #print(dftax) dfprov = pd.DataFrame({'Ci…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: import pandas as pd import pandas as pd dftax = pd.DataFrame({'Name':['A', 'B', 'C'], 'Income':[100, 200, 150], 'Tax':[10, 60, 30], 'City':['Amsterdam', 'Rotterdam', 'London']} ) print(dftax) dfprov = pd.DataFrame({'Cit…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: Gluing DataFrames together using pd.concat().
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: Database-style joins using .merge(). 'how' determines the type (left, right, inner, outer).
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Concatenation, Merging, and Grouping
  Preview: The Split-Apply-Combine pattern using .groupby().

### head, tail, describe, loc, iloc, Result Types, and Boolean Indexing

- Snippet ID: `subtopic:w5-inspecting-and-selecting-data:w5-inspecting-and-selecting-data-core`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `14`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Summary stats print(df.describe()) Use .head(n) for the first n rows, .tail(n) for the last n rows, and .describe() for summary statistics.
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Select rows/cols by name df.loc['First':'Third', ['Name', 'Weight']] Label-based selection. Slicing with .loc is inclusive of the end name.
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Select by position df.iloc[0:2, 0:1] # Rows 0,1; Col 0 Integer-position based selection. Slicing with .iloc is exclusive of the end index (like standard Python lists).
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Series vs DataFrame result type(df.loc[2]) # Series type(df.loc[[2]]) # DataFrame Selecting a single row/column with a label returns a Series; using a list/slice returns a DataFrame.
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Filter by condition df[df['Weight'] > 60] df.loc[df.Age < 155] Filtering data by passing a mask of True/False values (often created via comparisons).
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: import pandas as pd import pandas as pd d1 = [['A', 'B', 'C'],[153, 160, 150],[55, 70, 60]] df1 = pd.DataFrame (d1) df1 = df1.drop(1, axis = 0) df1 = df1.drop(1, axis = 1) print(df1) result = df1.iloc[2, 2] print(result…
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Label, mask, and step-based row selection import pandas as pd d1 = {10:['A', 'B', 'C', 'D'], 13:[153, 160, 150, 190], 12:[55, 70, 60, 80], 17:[10, 11, 12, 13]} df1 = pd.DataFrame (d1, index=[3, 2, 1, 0]) print(df1) prin…
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Valid vs invalid indexing forms df.loc[2:4, ['B']] df.iloc[1:4, [1]] df.loc[df['A'] > 0, ['B', 'C']] # invalid shortcut: # df[2, 'B'] Keep the rule simple: plain `df[...]` is not the place for a row selector plus a colu…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Use .head(n) for the first n rows, .tail(n) for the last n rows, and .describe() for summary statistics.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Label-based selection. Slicing with .loc is inclusive of the end name.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Integer-position based selection. Slicing with .iloc is exclusive of the end index (like standard Python lists).
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Selecting a single row/column with a label returns a Series; using a list/slice returns a DataFrame.
- `kp-5`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Filtering data by passing a mask of True/False values (often created via comparisons).
- `kp-6`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: head, tail, describe, loc, iloc, Result Types, and Boolean Indexing
  Preview: Selection rule: plain `df[...]` handles columns or a row mask, while `.loc[row_sel, col_sel]` and `.iloc[row_sel, col_sel]` handle both axes explicitly. `df[row, col]` is not the shortcut you want.

### Inspecting and Selecting Data

- Snippet ID: `item:cs-3d987070d4`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `cs-3d987070d4`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = [['A', 'B', 'C'],[153, 160, 150],[55, 70, 60]] df1 = pd.DataFrame (d1) df1 = df1.drop(1, axis = 0) df1 = df1.drop(1, axis = 1) print(df1) result = df1.iloc[2, 2] print(result…

### Inspecting and Selecting Data

- Snippet ID: `item:exam-Trial final exam Introduction to Python-6-w5-inspecting-and-selecting-data`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `exam-Trial final exam Introduction to Python-6-w5-inspecting-and-selecting-data`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have a pandas DataFrame called df that looks like this, when printed: A B C D 1 9.1 9.5 9.0 6.0 2 6.4 8.2 7.5 1.7 3 2.5 5.3 8.8 3.0 4 6.7 3.6 7.2 6.9 5 8.4 1.9 8.2 3.3 6 8.1 8.4 9.9 2.2 Suppose that you'd like to cr…

### Inspecting and Selecting Data

- Snippet ID: `item:exam-intro_python_sample_final_24_25-6-w4-string-operations-and-methods`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-6-w4-string-operations-and-methods`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose that you'd like to create a new DataFrame that contains only column 'B' for rows with indices 2, 4, and 6. Which of the following code lines will achieve what you want? A B C D A Option A uses a boolean mask on…

### Inspecting and Selecting Data

- Snippet ID: `item:ks-0114a2cff0`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `ks-0114a2cff0`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Viewing Data Use .head(n) for the first n rows, .tail(n) for the last n rows, and .describe() for summary statistics. Summary stats print(df.describe())

### Inspecting and Selecting Data

- Snippet ID: `item:ks-57ff66f9f1`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `ks-57ff66f9f1`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Selection: loc Label-based selection. Slicing with .loc is inclusive of the end name. Select rows/cols by name df.loc['First':'Third', ['Name', 'Weight']]

### Inspecting and Selecting Data

- Snippet ID: `item:ks-99fe849762`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `ks-99fe849762`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Selection Result Types Selecting a single row/column with a label returns a Series; using a list/slice returns a DataFrame. Series vs DataFrame result type(df.loc[2]) # Series type(df.loc[[2]]) # DataFrame

### Inspecting and Selecting Data

- Snippet ID: `item:ks-dfc064979d`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `ks-dfc064979d`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Selection: iloc Integer-position based selection. Slicing with .iloc is exclusive of the end index (like standard Python lists). Select by position df.iloc[0:2, 0:1] # Rows 0,1; Col 0

### Inspecting and Selecting Data

- Snippet ID: `item:ks-f550a3ffc7`
- Topic: Inspecting and Selecting Data
- Card ID: `w5-inspecting-and-selecting-data`
- Piece count: `1`

- `ks-f550a3ffc7`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Boolean Indexing Filtering data by passing a mask of True/False values (often created via comparisons). Filter by condition df[df['Weight'] > 60] df.loc[df.Age < 155]

### Pandas Core Structures

- Snippet ID: `item:cs-2e178eda82`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-2e178eda82`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2.loc[[1,2]] += 1 print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0 2 3 1 6 5 2 7 8

### Pandas Core Structures

- Snippet ID: `item:cs-49cf15967e`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-49cf15967e`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2.A += 1 print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0 3 3 1 6 4 2 7 7

### Pandas Core Structures

- Snippet ID: `item:cs-82ef14b9d5`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-82ef14b9d5`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2 += 1 print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0 3 4 1 6 5 2 7 8

### Pandas Core Structures

- Snippet ID: `item:cs-8bae99d6de`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-8bae99d6de`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2.A += [1, 2] print(df2) A B 0 2 3 1 5 4 2 6 7

### Pandas Core Structures

- Snippet ID: `item:cs-8ec741987c`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-8ec741987c`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2 += pd.DataFrame({'A':[1, 2, 3], 'B':[4, 5, 6]}) print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0…

### Pandas Core Structures

- Snippet ID: `item:cs-b069af91f4`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-b069af91f4`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2 += pd.DataFrame({'A':[2, 5, 6], 'B':[3, 4, 7]}, index=[4,5,6]) print(df2) A B 0 2 3 1 5…

### Pandas Core Structures

- Snippet ID: `item:cs-b3e0b57d7a`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-b3e0b57d7a`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2.A = df2.A.map(lambda x: 3 * x) print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0 6 3 1 15 4 2 18 7

### Pandas Core Structures

- Snippet ID: `item:cs-c4c296595e`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-c4c296595e`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2.loc[1] += 1 print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0 2 3 1 6 5 2 6 7

### Pandas Core Structures

- Snippet ID: `item:cs-cdfd529b3d`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-cdfd529b3d`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2.A += [1, 2, 3] print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0 3 3 1 7 4 2 9 7

### Pandas Core Structures

- Snippet ID: `item:cs-e6b6bd65f0`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `cs-e6b6bd65f0`
  Bucket: `additional` | Type: `source_notebook`
  Preview: import pandas as pd import pandas as pd d1 = {'A':[2, 5, 6], 'B':[3, 4, 7]} df1 = pd.DataFrame (d1) print(df1) df2 = df1.loc[:] df2.loc[1] = df2.loc[1].map(lambda x: 3 * x) print(df2) A B 0 2 3 1 5 4 2 6 7 A B 0 2 3 1 1…

### Pandas Core Structures

- Snippet ID: `item:exam-Test Exam 07-06-22-5-w5-pandas-core-structures`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `exam-Test Exam 07-06-22-5-w5-pandas-core-structures`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have a pandas Series called s, which contains floats. You'd like to create a new Series, in which each element is equal to the square of the difference between the corresponding element in s and the mean of the elem…

### Pandas Core Structures

- Snippet ID: `item:exam-Trial final exam Introduction to Python-5-w5-pandas-core-structures`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `exam-Trial final exam Introduction to Python-5-w5-pandas-core-structures`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have a pandas DataFrame called df. It has a column called "A" and a column called "B". Both contain numbers. You'd like to create a column called "C", which contains the sum of the numbers in columns "A" and "B". Wh…

### Pandas Core Structures

- Snippet ID: `item:exam-intro_python_sample_final_24_25-5-w4-string-fundamentals`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-5-w4-string-fundamentals`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have a pandas DataFrame called df with columns "A" and "B". You'd like to create a column called "C", which contains the sum of the numbers in columns "A" and "B". Which of the following code lines will achieve what…

### Pandas Core Structures

- Snippet ID: `item:kp-manual-df-constructor`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `kp-manual-df-constructor`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: A `DataFrame` is a 2D table; a dict of column names to equal-length lists is the standard constructor pattern.

### Pandas Core Structures

- Snippet ID: `item:kp-manual-pandas-two-axis`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `kp-manual-pandas-two-axis`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Plain `df[...]` is for column selection or a row mask. If you need both rows and columns, switch to `.loc[row_sel, col_sel]` or `.iloc[row_sel, col_sel]` instead of writing `df[row, col]`.

### Pandas Core Structures

- Snippet ID: `item:kp-manual-pandas-two-axis-d1`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `kp-manual-pandas-two-axis-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Valid vs invalid two-axis selection Form | Valid? | Use for df['A'] | yes | one column df[['A', 'B']] | yes | multiple columns df.loc[2:4, ['A']] | yes | label-based row + column selection df.iloc[1:3, [0]] | yes | posi…

### Pandas Core Structures

- Snippet ID: `item:kp-manual-series-default-index`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `kp-manual-series-default-index`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: A `Series` is 1D labeled data; if you do not supply an index, pandas uses `0, 1, 2, ...`.

### Pandas Core Structures

- Snippet ID: `item:kp-manual-series-vs-df`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `kp-manual-series-vs-df`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Single-column brackets return a `Series`, while a list of column names returns a `DataFrame`: `df['A']` -> Series, `df[['A']]` -> one-column DataFrame, `df[['A', 'B']]` -> two-column DataFrame.

### Pandas Core Structures

- Snippet ID: `item:kp-manual-series-vs-df-d1`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `kp-manual-series-vs-df-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Column-selection shape rules Code | Returns | Why it matters df['A'] | Series | one column, one bracket pair df[['A']] | DataFrame | list of columns keeps 2D shape df[['A', 'B']] | DataFrame | multi-column subset

### Pandas Core Structures

- Snippet ID: `item:ks-052ed25923`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `ks-052ed25923`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: pd.Series A one-dimensional labeled array. If no index is provided, it defaults to integers starting from 0. Creating a Series from a list import pandas as pd s1 = pd.Series([153, 160, 150], name='Length')

### Pandas Core Structures

- Snippet ID: `item:ks-75cf35c8b4`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `ks-75cf35c8b4`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: DatetimeIndex A specialized index for dates. Elements have attributes like .year, .month, and .day. Filtering by month df.loc[[r for r in df.index if r.month == 4]]

### Pandas Core Structures

- Snippet ID: `item:ks-9a5d2c05fb`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `ks-9a5d2c05fb`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: pd.DataFrame A two-dimensional tabular data structure. Most commonly created from a dictionary where keys are column names and values are lists. Creating from dictionary d = {'Name': ['A', 'B'], 'Weight': [55, 70]} df =…

### Pandas Core Structures

- Snippet ID: `item:manual-df-constructor`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `manual-df-constructor`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How do you build a `DataFrame` from a dict of column names to lists? Each key becomes a column, and each list supplies that column's values row by row. df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]})

### Pandas Core Structures

- Snippet ID: `item:manual-series-index`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `manual-series-index`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What index does a `Series` get if you do not provide one explicitly? Pandas uses the default integer index `0, 1, 2, ...`. s = pd.Series([10, 20, 30])

### Pandas Core Structures

- Snippet ID: `item:manual-series-vs-dataframe`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `1`

- `manual-series-vs-dataframe`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: What does `df['A']` return versus `df[['A']]`? `df['A']` returns a `Series`; `df[['A']]` returns a one-column `DataFrame`. df['A'] df[['A']]

### Series, DataFrame, and Creation Patterns

- Snippet ID: `subtopic:w5-pandas-core-structures:w5-pandas-core-structures-core`
- Topic: Pandas Core Structures
- Card ID: `w5-pandas-core-structures`
- Piece count: `5`

- `manual-pandas-df`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Series, DataFrame, and Creation Patterns
  Preview: Build a `DataFrame` from a dict of columns df = pd.DataFrame({'A': [1, 2], 'B': [3, 4]}) print(df) Each dict key becomes a column and the lists provide the row values for that column. A B 0 1 3 1 2 4
- `manual-pandas-import`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Series, DataFrame, and Creation Patterns
  Preview: Import pandas with the conventional alias import pandas as pd Use the `pd` alias so constructors and methods stay short and readable during the exam.
- `manual-pandas-invalid-two-axis`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Series, DataFrame, and Creation Patterns
  Preview: Use `.loc` or `.iloc` for row-plus-column selection df.loc[2:4, ['A']] df.iloc[1:3, [0]] # invalid shortcut: # df[2, 'A'] Once both a row selector and a column selector appear, switch to `.loc[...]` or `.iloc[...]` inst…
- `manual-pandas-select-shape`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Series, DataFrame, and Creation Patterns
  Preview: Single brackets vs list-of-columns brackets df['A'] # Series df[['A']] # one-column DataFrame df[['A', 'B']] # two-column DataFrame Single-column brackets drop to 1D `Series` shape; wrapping the column name(s) in a list…
- `manual-pandas-series`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Series, DataFrame, and Creation Patterns
  Preview: Create a `Series` from a list s = pd.Series([153, 160, 150], name='Length') print(s) Without an explicit index, pandas labels the rows `0, 1, 2, ...`. 0 153 1 160 2 150 Name: Length, dtype: int64

### Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply

- Snippet ID: `subtopic:w5-working-with-values:w5-working-with-values-core`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `22`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Sorting by column values df.sort_values(by='Length', ascending=False) Sort by labels with .sort_index() or by values with .sort_values(). axis=0 is rows, axis=1 is columns.
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Scalar broadcasting df['Height'] += 10 # Adds 10 to every cell in the column Applying a scalar operation (like + or *) to an entire Series or DataFrame automatically.
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Chained string operations s.str.upper().str.count('A') Accessible via .str, these allow string operations on every element of a Series.
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Filtering with isin vowels = list('aeiou') s[s.str[-1].str.lower().isin(vowels)] A vectorized version of 'in' to check if elements are within a collection.
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Formatting with map df['W_g'] = df['Weight'].map(lambda x: f'{x*1000} g') Applies a function (often a lambda) to every element of a Series.
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Row-wise average df['Avg'] = df.apply(lambda x: x.mean(), axis=1) Applies a function along an axis (0 for columns, 1 for rows) of a DataFrame.
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Handling NaNs df.fillna('No value') # Replaces all NaNs Represented by np.nan. Use .isna() to detect and .fillna() to replace them.
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Vectorized column arithmetic df['C'] = df['A'] + df['B'] df['D'] = df['A'] - df['B'] If the exam asks for elementwise column arithmetic, direct Series expressions are usually the clearest solution and do not need `apply…
- `manual-pandas-filter-aggregate`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Filter rows, then aggregate one column result = df.loc[df['A'] > 0, 'B'].mean() print(result) A common Pandas exam pattern is: build a boolean mask first, then run `mean()`, `sum()`, or `count()` on the selected column.
- `manual-pandas-map-column-sum`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Trace `map(lambda x: x + df['B'].sum())` import pandas as pd df = pd.DataFrame({"A": [1, 2], "B": [10, 20]}) result = df["A"].map(lambda x: x + df["B"].sum()) print(result.tolist()) `df["B"].sum()` is computed from the…
- `manual-pandas-split-into-columns`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Split string data into multiple DataFrame columns import pandas as pd df = pd.DataFrame({"place": ["Amsterdam; Noord-Holland", "Utrecht; Utrecht"]}) df[["municipality", "province"]] = df["place"].str.split("; ", expand=…
- `manual-working-values-axis-apply`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: `map` vs `apply(axis=0)` vs `apply(axis=1)` s.map(lambda x: x * 2) df.apply(lambda col: col.mean(), axis=0) df.apply(lambda row: row['A'] + row['B'], axis=1) `map` is elementwise on one Series, `apply(..., axis=0)` work…
- `manual-working-values-string-vs-map`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: `.str` methods vs `map(...)` s = pd.Series(['Aap', 'Nota', 'MIES']) print(s.map(lambda x: x.lower())) print(s.str.lower()) Use `.str` for vectorized string operations; `map(...)` is useful when you need a custom per-val…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Sort by labels with .sort_index() or by values with .sort_values(). axis=0 is rows, axis=1 is columns.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Applying a scalar operation (like + or *) to an entire Series or DataFrame automatically.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Accessible via .str, these allow string operations on every element of a Series.
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: A vectorized version of 'in' to check if elements are within a collection.
- `kp-5`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Use `Series.map(f)` for elementwise work on one Series. It expects a function, dict, or mapping-style Series; for arithmetic that already works columnwise, write the vectorized expression directly instead.
- `kp-6`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Use `DataFrame.apply(f, axis=0)` columnwise and `axis=1` rowwise. Reach for `apply` only when the function needs a whole row or column; otherwise direct column expressions are usually shorter and clearer.
- `kp-7`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Represented by np.nan. Use .isna() to detect and .fillna() to replace them.
- `kp-manual-drop-missing`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Use `.drop(...)` to remove labels and `.dropna()` to remove incomplete rows or columns; use `.fillna(...)` when you want to keep the shape and replace the missing values instead.
- `kp-manual-filter-aggregate`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Sorting, Missing Data, Broadcasting, Vectorized Strings, isin, map, and apply
  Preview: Filter first, then aggregate the resulting Series or DataFrame: `sum()`, `mean()`, `count()`, and `sort_values(...)` are common exam follow-ups after a boolean mask.

### Working With Values

- Snippet ID: `item:exam-intro_python_sample_final_24_25-7-w4-string-fundamentals`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-7-w4-string-fundamentals`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which of the following code lines could NOT have created df2 from df1? A B C D A Option A would sort all 5 rows of df1 and keep columns A, C, D, resulting in a 5-row DataFrame. df2 only has 3 rows (indices 4, 3, 2).

### Working With Values

- Snippet ID: `item:exam-intro_python_sample_final_24_25-8-w4-string-fundamentals`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-8-w4-string-fundamentals`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You have a Series s with municipality and province names separated by "; ". You'd like to create a new Series that only contains the municipality names. Which of the following code lines will achieve what you want? A B…

### Working With Values

- Snippet ID: `item:kp-5-d2`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `kp-5-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: `map` vs direct column arithmetic Pattern | Best when | Example s.map(f) | one value in, one value out | df['W_g'] = df['Weight'].map(...) df['A'] + df['B'] | plain vectorized arithmetic | df['C'] = df['A'] + df['B'] df…

### Working With Values

- Snippet ID: `item:kp-manual-drop-missing-d1`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `kp-manual-drop-missing-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Dropping a column by label df = df.drop(1, axis=1)

### Working With Values

- Snippet ID: `item:kp-manual-drop-missing-d2`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `kp-manual-drop-missing-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Removing rows with missing values df.dropna()

### Working With Values

- Snippet ID: `item:kp-manual-filter-aggregate-d1`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `kp-manual-filter-aggregate-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Filter then take the mean df.loc[df['A'] > 0, 'B'].mean()

### Working With Values

- Snippet ID: `item:kp-manual-filter-aggregate-d2`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `kp-manual-filter-aggregate-d2`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Common follow-up operations Goal | Pattern sum selected values | df.loc[mask, 'B'].sum() mean selected values | df.loc[mask, 'B'].mean() count selected rows | df.loc[mask, 'B'].count() sort rows by a column | df.sort_va…

### Working With Values

- Snippet ID: `item:ks-0d2d15f8d2`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `ks-0d2d15f8d2`
  Bucket: `additional` | Type: `source_lecture`
  Preview: apply() Applies a function along an axis (0 for columns, 1 for rows) of a DataFrame. Row-wise average df['Avg'] = df.apply(lambda x: x.mean(), axis=1)

### Working With Values

- Snippet ID: `item:ks-115ab52188`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `ks-115ab52188`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Vectorized String Methods Accessible via .str, these allow string operations on every element of a Series. Chained string operations s.str.upper().str.count('A')

### Working With Values

- Snippet ID: `item:ks-17e621a20d`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `ks-17e621a20d`
  Bucket: `additional` | Type: `source_lecture`
  Preview: map() Applies a function (often a lambda) to every element of a Series. Formatting with map df['W_g'] = df['Weight'].map(lambda x: f'{x*1000} g')

### Working With Values

- Snippet ID: `item:ks-18a9645168`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `ks-18a9645168`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Missing Data Represented by np.nan. Use .isna() to detect and .fillna() to replace them. Handling NaNs df.fillna('No value') # Replaces all NaNs

### Working With Values

- Snippet ID: `item:ks-2bed6c308f`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `ks-2bed6c308f`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: isin() A vectorized version of 'in' to check if elements are within a collection. Filtering with isin vowels = list('aeiou') s[s.str[-1].str.lower().isin(vowels)]

### Working With Values

- Snippet ID: `item:ks-305a41a33e`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `ks-305a41a33e`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Sorting Sort by labels with .sort_index() or by values with .sort_values(). axis=0 is rows, axis=1 is columns. Sorting by column values df.sort_values(by='Length', ascending=False)

### Working With Values

- Snippet ID: `item:ks-f8eec928e1`
- Topic: Working With Values
- Card ID: `w5-working-with-values`
- Piece count: `1`

- `ks-f8eec928e1`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Broadcasting Applying a scalar operation (like + or *) to an entire Series or DataFrame automatically. Scalar broadcasting df['Height'] += 10 # Adds 10 to every cell in the column

## Week 6

Snippet families in this group: **36**

### Comprehensions

- Snippet ID: `item:exam-intro_python_sample_final_24_25-12-w2-conditions`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-12-w2-conditions`
  Bucket: `recommended` | Type: `source_exam`
  Preview: You'd like to turn every upper case letter in a list into lower case and vice versa. Which code line achieves this? A B C D C Both options implement the conditional logic required to flip the case of each character in t…

### Comprehensions

- Snippet ID: `item:kp-manual-comprehension-syntax-d1`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `kp-manual-comprehension-syntax-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Syntax-first comprehension reference Target | Template | Exam cue list | [expr for x in seq if cond] | filter at the end list with else | [a if cond else b for x in seq] | conditional expression stays before `for` dict…

### Comprehensions

- Snippet ID: `item:ks-0a4fcae36d`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-0a4fcae36d`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Generator Comprehensions Created using parentheses (). Highly memory efficient because they calculate values on the fly rather than storing the whole list in memory. Generator for large range gen = (x for x in range(100…

### Comprehensions

- Snippet ID: `item:ks-0e5c8b8b42`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-0e5c8b8b42`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: String Transformations via List Comprehension Since 'string comprehensions' don't exist natively, use a list comprehension to process characters and then '.join()' them back into a string. Double vowels in a string s2 =…

### Comprehensions

- Snippet ID: `item:ks-1bc815f6d1`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-1bc815f6d1`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Map and Filter vs. Comprehensions Comprehensions are generally preferred over combining map() and filter() with lambda functions for readability. Equivalent logic using map/filter l2 = list(map(lambda x: x*2, filter(lam…

### Comprehensions

- Snippet ID: `item:ks-3e04c4d5e8`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-3e04c4d5e8`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Nested Dictionary Comprehensions Allows creating complex nested structures like dictionaries within dictionaries in a single concise line. Dictionary with sub-dictionaries result = {x: {y: x + y for y in range(x, 4)} fo…

### Comprehensions

- Snippet ID: `item:ks-72c58bb6b2`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-72c58bb6b2`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Dictionary Comprehensions with Logic Can include 'if' conditions to filter keys or values during dictionary creation. Filtering dictionary items d = {k: v for k, v in {'a': 1, 'b': 2}.items() if v > 1}

### Comprehensions

- Snippet ID: `item:ks-b9d93f2bc1`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-b9d93f2bc1`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Walrus Operator in Comprehensions The walrus operator (:=) allows assigning a value to a variable within an expression, avoiding redundant calculations in filters or transformations. Using walrus to avoid double squarin…

### Comprehensions

- Snippet ID: `item:ks-cacc4fbc21`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-cacc4fbc21`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Set Comprehensions Creates a set using curly braces with a single expression (not key:value pairs). Automatically handles uniqueness and ignores order. Building a set of doubled odd numbers s1 = {x * 2 for x in [1, 3, 2…

### Comprehensions

- Snippet ID: `item:ks-dd2965ef50`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `1`

- `ks-dd2965ef50`
  Bucket: `additional` | Type: `source_lecture`
  Preview: Enumerate in Comprehensions Use enumerate() to access both the index and the value of items within a comprehension. Divide by index plus offset res = [val // (i + 6) for i, val in enumerate([46, 48])]

### List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns

- Snippet ID: `subtopic:w6-comprehensions:w6-comprehensions-core`
- Topic: Comprehensions
- Card ID: `w6-comprehensions`
- Piece count: `19`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Building a set of doubled odd numbers s1 = {x * 2 for x in [1, 3, 2, 5] if x % 2 != 0} Creates a set using curly braces with a single expression (not key:value pairs). Automatically handles uniqueness and ignores order.
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Double vowels in a string s2 = ''.join([x*2 if x.lower() in 'aeiou' else x for x in 'Python']) Since 'string comprehensions' don't exist natively, use a list comprehension to process characters and then '.join()' them b…
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Dictionary with sub-dictionaries result = {x: {y: x + y for y in range(x, 4)} for x in range(1, 4)} Allows creating complex nested structures like dictionaries within dictionaries in a single concise line.
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Using walrus to avoid double squaring l1 = [(x, r) for x in range(1, 10) if 20 > (r := x**2) > 10] The walrus operator (:=) allows assigning a value to a variable within an expression, avoiding redundant calculations in…
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Equivalent logic using map/filter l2 = list(map(lambda x: x*2, filter(lambda x: x%3 != 0, [1, 2, 3, 4]))) Comprehensions are generally preferred over combining map() and filter() with lambda functions for readability.
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Generator for large range gen = (x for x in range(1000000) if x % 3 == 0) Created using parentheses (). Highly memory efficient because they calculate values on the fly rather than storing the whole list in memory.
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Filtering dictionary items d = {k: v for k, v in {'a': 1, 'b': 2}.items() if v > 1} Can include 'if' conditions to filter keys or values during dictionary creation.
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Divide by index plus offset res = [val // (i + 6) for i, val in enumerate([46, 48])] Use enumerate() to access both the index and the value of items within a comprehension.
- `manual-comprehension-conditional-patterns`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Filter vs transform inside a comprehension flipped = [letter.lower() if letter.isupper() else letter.upper() for letter in letters] positives = [value for value in nums if value > 0] Use trailing `if` to filter items ou…
- `manual-comprehension-syntax-core`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: One-line syntax reference for list, dict, and set comprehensions evens = [x for x in nums if x % 2 == 0] labels = {name: len(name) for name in names} unique_lengths = {len(name) for name in names} These three forms cove…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Creates a set using curly braces with a single expression (not key:value pairs). Automatically handles uniqueness and ignores order.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Since 'string comprehensions' don't exist natively, use a list comprehension to process characters and then '.join()' them back into a string.
- `kp-3`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Allows creating complex nested structures like dictionaries within dictionaries in a single concise line.
- `kp-4`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: The walrus operator (:=) allows assigning a value to a variable within an expression, avoiding redundant calculations in filters or transformations.
- `kp-5`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Comprehensions are generally preferred over combining map() and filter() with lambda functions for readability.
- `kp-6`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Created using parentheses (). Highly memory efficient because they calculate values on the fly rather than storing the whole list in memory.
- `kp-7`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Can include 'if' conditions to filter keys or values during dictionary creation.
- `kp-8`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Use enumerate() to access both the index and the value of items within a comprehension.
- `kp-manual-comprehension-syntax`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: List/Dict/Set Comprehensions, Nested Variants, Logic Filters, Walrus, and enumerate Patterns
  Preview: Read comprehension syntax left to right: output expression first, then `for`, then an optional trailing `if`; inline `a if cond else b` belongs in the output expression, not after the loop.

### Datetime

- Snippet ID: `item:cs-905c77e1f3`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `cs-905c77e1f3`
  Bucket: `recommended` | Type: `source_notebook`
  Preview: from datetime import datetime from datetime import datetime d = datetime.strptime("2024$05%20","%Y$%m%%%d") print(d) from datetime import datetime d = datetime.strptime("24$05%20","%y$%m%%%d") print(d) from datetime imp…

### Datetime

- Snippet ID: `item:exam-intro_python_sample_final_24_25-10-w6-datetime`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-10-w6-datetime`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Which of the following code segments will return the number of the day (1-366) that a datetime value represents within the year? A B C D A Subtracting two datetime objects results in a timedelta object. Accessing the .d…

### Datetime

- Snippet ID: `item:exam-intro_python_sample_final_24_25-9-w6-datetime`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `exam-intro_python_sample_final_24_25-9-w6-datetime`
  Bucket: `recommended` | Type: `source_exam`
  Preview: Suppose that you call the function like this: get_months(["03/02/2013", "03.02.2013", "03-02-2013"]). What does the function call return? A B C D A 1st string: contains '/' so it uses %m/%d/%Y -> month 3. 2nd: contains…

### Datetime

- Snippet ID: `item:kp-manual-datetime-day-of-year`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-day-of-year`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: The day number within the year can be formatted with `%j` or computed with `(dt - datetime(dt.year, 1, 1)).days + 1`.

### Datetime

- Snippet ID: `item:kp-manual-datetime-delta`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-delta`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Subtracting two datetimes gives a `timedelta`; its most-used direct attributes are `.days`, `.seconds`, and `.microseconds`.

### Datetime

- Snippet ID: `item:kp-manual-datetime-format`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-format`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: `strftime` formats a datetime into text; `strptime` parses text into a datetime object.

### Datetime

- Snippet ID: `item:kp-manual-datetime-format-codes`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-format-codes`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Memorize the core format codes: `%Y` year, `%m` month, `%d` day, `%H` hour, `%M` minute, `%S` second, `%j` day-of-year.

### Datetime

- Snippet ID: `item:kp-manual-datetime-format-codes-d1`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-format-codes-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Core datetime format codes Code | Meaning | Example %Y | 4-digit year | 2024 %m | 2-digit month | 05 %d | 2-digit day | 20 %H | hour (24h) | 14 %M | minute | 30 %S | second | 09 %j | day of year | 141

### Datetime

- Snippet ID: `item:kp-manual-datetime-iso`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-iso`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Use `isoformat()` for an ISO-style timestamp, `isoweekday()` for Monday=1..Sunday=7, and `isocalendar()` when you need ISO year/week information.

### Datetime

- Snippet ID: `item:kp-manual-datetime-now`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-now`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: `datetime.now()` gives the current local datetime; use `.timestamp()` only when you specifically need seconds since the Unix epoch.

### Datetime

- Snippet ID: `item:kp-manual-datetime-objects-vs-strings`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-objects-vs-strings`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: `strptime(...)` returns a `datetime`, while `strftime(...)` returns a string. Do arithmetic and attribute access on the datetime object first, then format to text at the end.

### Datetime

- Snippet ID: `item:kp-manual-datetime-objects-vs-strings-d1`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-objects-vs-strings-d1`
  Bucket: `keyPoints` | Type: `key_point_detail`
  Preview: Object vs string workflow Operation | Return type | Can use `.year` / `+ timedelta(...)`? datetime.strptime(...) | datetime | yes dt.strftime(...) | str | no

### Datetime

- Snippet ID: `item:kp-manual-datetime-replace`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `kp-manual-datetime-replace`
  Bucket: `keyPoints` | Type: `key_point`
  Preview: Datetime objects are immutable, so `.replace(...)` returns a new datetime instead of modifying the original one.

### Datetime

- Snippet ID: `item:ks-169cc25be1`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `ks-169cc25be1`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: strptime: String to Date Parses a string into a datetime object based on a provided format template. Parsing a date string from datetime import datetime d = datetime.strptime('2024-05-20', '%Y-%m-%d')

### Datetime

- Snippet ID: `item:ks-662456da41`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `ks-662456da41`
  Bucket: `additional` | Type: `source_lecture`
  Preview: The replace() Method Datetime objects are immutable. The replace() method creates a new datetime object with specific attributes changed. Changing the year of a date from datetime import datetime d = datetime.now().repl…

### Datetime

- Snippet ID: `item:ks-755c23c4be`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `ks-755c23c4be`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: strftime: Date to String Formats a datetime object into a readable string using format codes (e.g., %Y for 4-digit year, %m for month). Formatting a date from datetime import datetime print(datetime.now().strftime('%Y-%…

### Datetime

- Snippet ID: `item:ks-86cd7ede1c`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `ks-86cd7ede1c`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Timedelta and Date Arithmetic Timedelta objects represent durations. Subtracting two datetimes creates a timedelta; adding a timedelta to a datetime shifts the date. Calculating days difference from datetime import date…

### Datetime

- Snippet ID: `item:ks-e643ee5e77`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `ks-e643ee5e77`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: datetime.now and Timestamps datetime.now() retrieves the current local time. timestamp() returns the seconds since the Unix Epoch (Jan 1, 1970). Getting current timestamp from datetime import datetime print(datetime.now…

### Datetime

- Snippet ID: `item:manual-day-of-year`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `manual-day-of-year`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: How can you compute the day number within the year from a datetime? Subtract January 1st of the same year, take `.days`, and add 1 so January 1st becomes day 1. def day_of_year(dt): return (dt - datetime(dt.year, 1, 1))…

### Datetime

- Snippet ID: `item:manual-strftime-vs-strptime`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `manual-strftime-vs-strptime`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: When do you use `strftime` versus `strptime`? `strftime` formats a datetime into text; `strptime` parses text into a datetime object. dt.strftime('%Y-%m-%d') datetime.strptime('2024-05-20', '%Y-%m-%d')

### Datetime

- Snippet ID: `item:manual-timedelta-attrs`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `1`

- `manual-timedelta-attrs`
  Bucket: `aiQuestions` | Type: `ai_common_question`
  Preview: Which attributes exist directly on a `timedelta` object? A `timedelta` stores `days`, `seconds`, and `microseconds`; hours or weeks must be derived or supplied when constructing it. delta = end - start print(delta.days,…

### now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic

- Snippet ID: `subtopic:w6-datetime:w6-datetime-core`
- Topic: Datetime
- Card ID: `w6-datetime`
- Piece count: `10`

- `manual-datetime-add-before-format`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Parse, do arithmetic, then format from datetime import datetime, timedelta dt = datetime.strptime('2024-05-20 14:30', '%Y-%m-%d %H:%M') updated = dt + timedelta(days=2, minutes=15) print(updated.strftime('%Y-%m-%d %H:%M…
- `manual-datetime-day-of-year`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Compute the day number within the year from datetime import datetime def day_of_year(dt): return (dt - datetime(dt.year, 1, 1)).days + 1 print(day_of_year(datetime(2024, 5, 20))) Subtract January 1st of the same year, t…
- `manual-datetime-delta`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Subtract datetimes to get a `timedelta` from datetime import datetime start = datetime(2024, 1, 1) end = datetime(2024, 1, 4) print((end - start).days) Datetime subtraction gives a `timedelta`, whose `.days` attribute i…
- `manual-datetime-format`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Format a datetime with `strftime` from datetime import datetime dt = datetime(2024, 5, 20, 14, 30) print(dt.strftime('%Y-%m-%d %H:%M')) Use `strftime` when the exam asks for a formatted string such as year-month-day or…
- `manual-datetime-iso`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: ISO and week-based helpers from datetime import datetime d = datetime(2024, 5, 20) print(d.isoformat()) print(d.isoweekday()) print(d.isocalendar()[1]) Use ISO helpers when the exam asks for an ISO string, the weekday w…
- `manual-datetime-overlap`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Check whether two datetime intervals overlap from datetime import datetime start_a = datetime(2024, 5, 20, 9, 0) end_a = datetime(2024, 5, 20, 11, 0) start_b = datetime(2024, 5, 20, 10, 30) end_b = datetime(2024, 5, 20,…
- `manual-datetime-parse`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Parse text with `strptime` from datetime import datetime dt = datetime.strptime('2024-05-20', '%Y-%m-%d') print(dt) The format string must match the input text exactly, including separators. 2024-05-20 00:00:00
- `manual-datetime-replace`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: `.replace(...)` returns a new datetime from datetime import datetime d = datetime(2024, 5, 20) print(d.replace(year=2026)) print(d) Datetime objects are immutable, so `.replace(...)` does not modify the original object…
- `manual-datetime-strftime-loop`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Do datetime math before `strftime` turns values into strings from datetime import datetime, timedelta day = datetime(2024, 1, 1) labels = [] for _ in range(3): labels.append(day.strftime("%Y-%m-%d")) day += timedelta(da…
- `manual-datetime-year-month-day`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: now, Timestamps, strftime, strptime, timedelta, and Date Arithmetic
  Preview: Datetime attributes stay on the object, not on the formatted string from datetime import datetime dt = datetime.strptime('03-02-2013', '%d-%m-%Y') print(dt.year, dt.month, dt.day) print(dt.strftime('%Y-%m-%d')) After `s…

### Generators and Iterators

- Snippet ID: `item:ks-900b394f8e`
- Topic: Generators and Iterators
- Card ID: `w6-generators-and-iterators`
- Piece count: `1`

- `ks-900b394f8e`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Generator Functions Functions using the 'yield' keyword. They produce values one at a time and maintain their local state (variables) between calls. Simple step generator def count(start, stop, step): while start <= sto…

### Generators and Iterators

- Snippet ID: `item:ks-cd030b9520`
- Topic: Generators and Iterators
- Card ID: `w6-generators-and-iterators`
- Piece count: `1`

- `ks-cd030b9520`
  Bucket: `recommended` | Type: `source_lecture`
  Preview: Iterators Objects that can be traversed using next(). Lists can be turned into iterators using iter(). They raise StopIteration when exhausted. Manual iteration it = iter([1, 2]); print(next(it)); print(next(it))

### Iterator Protocol, Generator Functions, and Generator Comprehensions

- Snippet ID: `subtopic:w6-generators-and-iterators:w6-generators-and-iterators-core`
- Topic: Generators and Iterators
- Card ID: `w6-generators-and-iterators`
- Piece count: `10`

- `ai-example-1`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: Simple step generator def count(start, stop, step): while start <= stop: yield start start += step Functions using the 'yield' keyword. They produce values one at a time and maintain their local state (variables) betwee…
- `ai-example-2`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: Manual iteration it = iter([1, 2]); print(next(it)); print(next(it)) Objects that can be traversed using next(). Lists can be turned into iterators using iter(). They raise StopIteration when exhausted.
- `ai-example-3`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: myiterator = iter([1,3,5]) myiterator = iter([1,3,5]) print(next(myiterator)) print(next(myiterator)) print(next(myiterator)) print(next(myiterator))
- `ai-example-4`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: class Mylist(list): class Mylist(list): pass myiterator = iter(Mylist([1,3,5])) print(next(myiterator)) print(next(myiterator)) print(next(myiterator)) print(next(myiterator))
- `ai-example-5`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: mygenerator = (x for x in range(100000000) if x%3 == 0 or x%4 == 0) mygenerator = (x for x in range(100000000) if x%3 == 0 or x%4 == 0) print(next(mygenerator)) print(next(mygenerator)) print(next(mygenerator)) print(ne…
- `ai-example-6`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: class Mylist(list): class Mylist(list): def __iter__ (self): pass myiterator = iter(Mylist([1,3,5])) print(next(myiterator)) print(next(myiterator)) print(next(myiterator)) print(next(myiterator))
- `ai-example-7`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: def generatorfunction(start, stop, step): def generatorfunction(start, stop, step): while (num:=start) <= stop: yield num start += step return 'End of numbers' for x in generatorfunction(1, 5, 2): print(x) For numeric v…
- `ai-example-8`
  Bucket: `aiExamples` | Type: `ai_example`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: def generatorfunction(start, stop, step): def generatorfunction(start, stop, step): while True: num = start start += step if num <= stop: yield num else: return 'End of numbers' print(list(generatorfunction(1, 5, 2))) F…
- `kp-1`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: Functions using the 'yield' keyword. They produce values one at a time and maintain their local state (variables) between calls.
- `kp-2`
  Bucket: `keyPoints` | Type: `key_point`
  Subtopic: Iterator Protocol, Generator Functions, and Generator Comprehensions
  Preview: Objects that can be traversed using next(). Lists can be turned into iterators using iter(). They raise StopIteration when exhausted.
