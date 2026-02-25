#!/usr/bin/env python3
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
CARDS_FILE = ROOT / "topic_cards.json"


def example_detail(title: str, text: str = "", code: str = "") -> dict[str, Any]:
    return {
        "kind": "example",
        "title": title,
        "text": text.strip(),
        "code": code.strip(),
    }


def table_detail(title: str, headers: list[str], rows: list[list[str]], text: str = "") -> dict[str, Any]:
    return {
        "kind": "table",
        "title": title,
        "text": text.strip(),
        "table": {
            "headers": headers,
            "rows": rows,
        },
    }


def explanation_detail(title: str, text: str) -> dict[str, Any]:
    return {
        "kind": "explanation",
        "title": title,
        "text": text.strip(),
    }


def details_for_point(topic: str, text: str) -> list[dict[str, Any]]:
    lower = text.lower()
    topic_lower = (topic or "").strip().lower()

    if "list.sort()" in lower and "sorted" in lower:
        return [
            table_detail(
                "In-place vs new object",
                ["Operation", "Mutates original?", "Return value"],
                [
                    ["`lst.sort()`", "Yes", "`None`"],
                    ["`sorted(lst)`", "No", "New sorted list"],
                ],
            ),
            example_detail(
                "Optional code example",
                code=(
                    "lst = [3, 1, 2]\n"
                    "result = lst.sort()      # lst becomes [1, 2, 3]\n"
                    "print(result)            # None\n"
                    "new_lst = sorted(lst)    # new list object"
                ),
            ),
        ]

    if "string methods" in lower or ".upper()" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "s = 'uva'\n"
                    "s.upper()          # ignored result\n"
                    "print(s)           # 'uva'\n"
                    "s = s.upper()\n"
                    "print(s)           # 'UVA'"
                ),
            ),
        ]

    if "mutable types" in lower and "immutable types" in lower:
        return [
            table_detail(
                "Mutable vs immutable",
                ["Category", "Examples", "Can change in place?"],
                [
                    ["Mutable", "`list`, `dict`, `set`", "Yes"],
                    ["Immutable", "`int`, `str`, `tuple`, `bool`", "No"],
                ],
            ),
        ]

    if "x = y" in lower and "same object" in lower:
        return [
            table_detail(
                "Assignment vs copy",
                ["Statement", "Meaning"],
                [
                    ["`y = x`", "Alias: both names point to same object"],
                    ["`y = x[:]` / `x.copy()`", "New shallow copy (list)"],
                ],
            ),
            example_detail(
                "Optional code example",
                code=(
                    "a = [1, 2]\n"
                    "b = a\n"
                    "b.append(3)\n"
                    "print(a)           # [1, 2, 3] (same object)\n"
                    "c = a[:]\n"
                    "c.append(4)\n"
                    "print(a, c)        # [1, 2, 3], [1, 2, 3, 4]"
                ),
            ),
        ]

    if "function definition uses `def`" in lower or ("defined with def" in lower and "called with ()" in lower):
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def add(a, b):\n"
                    "    return a + b\n"
                    "\n"
                    "result = add(2, 3)\n"
                    "print(result)  # 5"
                ),
            ),
        ]

    if "keys must be unique and immutable" in lower or "unhashable type" in lower:
        return [
            table_detail(
                "Hashable key quick check",
                ["Type", "Valid as dict key?"],
                [
                    ["`str`, `int`, `tuple`", "Yes"],
                    ["`list`, `dict`, `set`", "No (mutable/unhashable)"],
                ],
            ),
        ]

    if "in operator checks" in lower and "key" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "d = {'a': 1, 'b': 2}\n"
                    "print('a' in d)    # True (key)\n"
                    "print(1 in d)      # False (value is not checked by `in`)"
                ),
            ),
        ]

    if "raises a `keyerror`" in lower or ("dict.get" in lower and "without error" in lower):
        return [
            table_detail(
                "Missing-key behavior",
                ["Access form", "Missing key result"],
                [
                    ["`d[key]`", "`KeyError`"],
                    ["`d.get(key)`", "`None` (or provided default)"],
                ],
            ),
            example_detail(
                "Optional code example",
                code=(
                    "d = {'x': 10}\n"
                    "print(d.get('y', 0))   # 0\n"
                    "# d['y'] would raise KeyError"
                ),
            ),
        ]

    if "dict.keys()" in lower or "dict.values()" in lower or "dict.items()" in lower:
        return [
            table_detail(
                "Dict iteration targets",
                ["Form", "Yields"],
                [
                    ["`for k in d` / `d.keys()`", "Keys"],
                    ["`d.values()`", "Values"],
                    ["`d.items()`", "`(key, value)` pairs"],
                ],
            ),
        ]

    if "set()" in lower and "{}" in lower and "empty" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "empty_dict = {}\n"
                    "empty_set = set()\n"
                    "print(type(empty_dict).__name__)  # dict\n"
                    "print(type(empty_set).__name__)   # set"
                ),
            ),
        ]

    if "sets are unordered" in lower or "duplicate values are ignored" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "s = {1, 2, 2, 3}\n"
                    "print(s)        # {1, 2, 3} (order may vary)\n"
                    "print(len(s))   # 3"
                ),
            ),
        ]

    if "unboundlocalerror" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = 10\n"
                    "def f():\n"
                    "    x += 1      # UnboundLocalError: local x referenced before assignment\n"
                    "\n"
                    "# fix:\n"
                    "def g():\n"
                    "    global x\n"
                    "    x += 1"
                ),
            ),
        ]

    if "legb" in lower:
        return [
            table_detail(
                "LEGB order",
                ["Lookup order", "Meaning"],
                [
                    ["Local", "Current function scope"],
                    ["Enclosing", "Nearest outer function scope"],
                    ["Global", "Module-level scope"],
                    ["Builtins", "Python built-in names"],
                ],
            ),
        ]

    if "global" in lower and ("local" in lower or "nonlocal" in lower):
        return [
            example_detail(
                "Optional code example",
                code=(
                    "count = 0\n"
                    "def inc_global():\n"
                    "    global count\n"
                    "    count += 1\n"
                    "\n"
                    "def outer():\n"
                    "    n = 0\n"
                    "    def inner():\n"
                    "        nonlocal n\n"
                    "        n += 1"
                ),
            ),
        ]

    if "forward indexing starts at `0`" in lower or "negative indexing" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "seq = ['a', 'b', 'c', 'd']\n"
                    "print(seq[0])    # 'a'\n"
                    "print(seq[-1])   # 'd'\n"
                    "print(seq[-4])   # 'a'"
                ),
            ),
        ]

    if "slicing syntax is `seq[start:end:step]`" in lower or "slice syntax `seq[start:end:step]`" in lower:
        return [
            table_detail(
                "Slice fields",
                ["Field", "Meaning"],
                [
                    ["`start`", "First included index"],
                    ["`end`", "First excluded index"],
                    ["`step`", "Stride (+/- direction and gap)"],
                ],
            ),
            example_detail(
                "Optional code example",
                code=(
                    "s = 'abcdef'\n"
                    "print(s[1:4])    # 'bcd'\n"
                    "print(s[::2])    # 'ace'\n"
                    "print(s[::-1])   # 'fedcba'"
                ),
            ),
        ]

    if "shallow copy" in lower or "same object" in lower and "[:]" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "a = [[1], [2]]\n"
                    "b = a[:]         # shallow copy\n"
                    "b[0].append(9)\n"
                    "print(a)         # [[1, 9], [2]] (inner list shared)"
                ),
            ),
            explanation_detail(
                "Optional note",
                "Use `copy.deepcopy(...)` when nested mutable objects must be fully independent.",
            ),
        ]

    if "negative step" in lower and "slice" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = [0, 1, 2, 3, 4, 5]\n"
                    "print(x[5:1:-2])   # [5, 3]\n"
                    "print(x[1:5:-2])   # []"
                ),
            ),
        ]

    if "range(" in lower and ("exclusive" in lower or "stop-1" in lower):
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print(list(range(5)))      # [0, 1, 2, 3, 4]\n"
                    "print(list(range(2, 6)))   # [2, 3, 4, 5]"
                ),
            ),
        ]

    if "`break`" in lower and "`continue`" in lower:
        return [
            table_detail(
                "Loop control quick table",
                ["Keyword", "Effect"],
                [
                    ["`break`", "Exit current loop immediately"],
                    ["`continue`", "Skip rest of current iteration"],
                    ["`pass`", "Do nothing (placeholder statement)"],
                ],
            ),
        ]

    if "enumerate(" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "items = ['a', 'b']\n"
                    "for i, v in enumerate(items, start=1):\n"
                    "    print(i, v)\n"
                    "# 1 a\n"
                    "# 2 b"
                ),
            ),
        ]

    if "zip(" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "names = ['Ana', 'Bo', 'Cy']\n"
                    "scores = [8, 9]\n"
                    "print(list(zip(names, scores)))\n"
                    "# [('Ana', 8), ('Bo', 9)]"
                ),
            ),
        ]

    if "falsy values include" in lower or "boolean context" in lower:
        return [
            table_detail(
                "Truthy/Falsy quick table",
                ["Expression", "Boolean value"],
                [
                    ["`0`, `0.0`, `''`, `[]`, `{}`, `None`", "Falsy"],
                    ["Non-empty collections, non-zero numbers", "Truthy"],
                ],
            ),
        ]

    if "precedence" in lower and "not" in lower and "and" in lower and "or" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "expr = True or False and False\n"
                    "print(expr)  # True (`and` evaluated before `or`)\n"
                    "print((True or False) and False)  # False"
                ),
            ),
        ]

    if "*args" in lower and "tuple" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def f(*args):\n"
                    "    print(type(args).__name__, args)\n"
                    "\n"
                    "f(1, 2, 3)  # tuple (1, 2, 3)"
                ),
            ),
        ]

    if "**kwargs" in lower and "dict" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def g(**kwargs):\n"
                    "    for k, v in kwargs.items():\n"
                    "        print(k, v)\n"
                    "\n"
                    "g(name='Ana', score=10)"
                ),
            ),
        ]

    if "lambda" in lower or "map(" in lower or "filter(" in lower or "reduce" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "nums = [1, 2, 3, 4]\n"
                    "print(list(map(lambda x: x * 2, nums)))      # [2, 4, 6, 8]\n"
                    "print(list(filter(lambda x: x % 2 == 0, nums)))  # [2, 4]"
                ),
            ),
        ]

    if "without an explicit `return`" in lower or "implicitly returns `none`" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def f():\n"
                    "    x = 1\n"
                    "\n"
                    "print(f())  # None"
                ),
            ),
        ]

    if "uncaught exception" in lower and "later lines do not run" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print('A')\n"
                    "1 / 0              # ZeroDivisionError\n"
                    "print('B')         # never runs"
                ),
            ),
        ]

    if "`is` checks" in lower and "`==` checks" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "a = [1, 2]\n"
                    "b = [1, 2]\n"
                    "c = a\n"
                    "print(a == b)  # True  (same value)\n"
                    "print(a is b)  # False (different objects)\n"
                    "print(a is c)  # True"
                ),
            ),
        ]

    if "mutable default" in lower or ("default" in lower and "list" in lower and "function" in lower):
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def bad(acc=[]):\n"
                    "    acc.append(1)\n"
                    "    return acc\n"
                    "\n"
                    "def good(acc=None):\n"
                    "    if acc is None:\n"
                    "        acc = []\n"
                    "    acc.append(1)\n"
                    "    return acc"
                ),
            ),
        ]

    if "walrus" in topic_lower or ":=" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "while (line := input().strip()) != 'stop':\n"
                    "    print(line)\n"
                    "# assigns and checks in one expression"
                ),
            ),
        ]

    if "unpack" in lower and "*" in text:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "nums = [1, 2, 3]\n"
                    "print(*nums)  # 1 2 3\n"
                    "\n"
                    "def add(a, b, c):\n"
                    "    return a + b + c\n"
                    "print(add(*nums))  # 6"
                ),
            ),
        ]

    if "single-element tuple" in topic_lower or "not a tuple" in lower and "(5)" in lower:
        return [
            table_detail(
                "Tuple comma rule",
                ["Expression", "Type/meaning"],
                [
                    ["`(5)`", "`int` value `5`"],
                    ["`(5,)`", "Single-element `tuple`"],
                ],
            ),
            example_detail(
                "Optional code example",
                code=(
                    "print(type((5)).__name__)    # int\n"
                    "print(type((5,)).__name__)   # tuple"
                ),
            ),
        ]

    if "explicit type conversion" in lower or "str` + `int" in lower or "str + int" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "a = '12'\n"
                    "b = 3\n"
                    "# print(a + b)   # TypeError\n"
                    "print(int(a) + b)   # 15\n"
                    "print(a + str(b))   # '123'"
                ),
            ),
        ]

    if "keyword arguments must follow all positional arguments" in lower or "causes a `syntaxerror`" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def f(a, b=0):\n"
                    "    return a + b\n"
                    "\n"
                    "f(1, b=2)      # valid\n"
                    "# f(a=1, 2)    # SyntaxError"
                ),
            ),
        ]

    if "continue" in lower and "infinite loop" in lower and "while" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "i = 0\n"
                    "while i < 3:\n"
                    "    if i == 1:\n"
                    "        continue   # bug: i not incremented here\n"
                    "    i += 1"
                ),
            ),
            explanation_detail(
                "Optional note",
                "Place loop-state updates before `continue`, or duplicate the update in all paths.",
            ),
        ]

    if "tuple assignment" in lower or "d, e, f =" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x, y, z = (10, 20, 30)\n"
                    "print(x, y, z)\n"
                    "\n"
                    "a, b = b, a   # swap values"
                ),
            ),
        ]

    if "and returns the first falsy operand" in lower or "or returns the first truthy operand" in lower or "short-circuit" in lower:
        return [
            table_detail(
                "Short-circuit return value",
                ["Expression", "Returns"],
                [
                    ["`A and B`", "First falsy operand, else `B`"],
                    ["`A or B`", "First truthy operand, else `B`"],
                ],
            ),
            example_detail(
                "Optional code example",
                code=(
                    "print(0 and 5)      # 0\n"
                    "print(3 and 5)      # 5\n"
                    "print('' or 'x')    # 'x'"
                ),
            ),
        ]

    if "x == 1 or 2" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = 3\n"
                    "print(x == 1 or 2)          # 2 -> truthy\n"
                    "print(x == 1 or x == 2)     # False\n"
                    "print(x in (1, 2))          # False"
                ),
            ),
        ]

    if "floor division" in lower and "negative" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print(5 // 3)     # 1\n"
                    "print(-5 // 3)    # -2  (toward negative infinity)"
                ),
            ),
        ]

    if "`/` (division) always returns a float" in lower or "`//` (floor division)" in lower:
        return [
            table_detail(
                "Division operators",
                ["Operator", "Meaning"],
                [
                    ["`/`", "True division (float result)"],
                    ["`//`", "Floor division (round down)"],
                ],
            ),
        ]

    if "sequence comparison" in lower and "shorter sequence is considered" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print([1, 2] < [1, 2, 0])   # True\n"
                    "print((1, 3) > (1, 2, 9))   # True (compares at first differing element)"
                ),
            ),
        ]

    if "pass is a null operation" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "for x in [1, 2, 3]:\n"
                    "    if x % 2 == 0:\n"
                    "        pass    # placeholder for future logic"
                ),
            ),
        ]

    if "`print()` displays output" in lower and "`return` sends a value back" in lower:
        return [
            table_detail(
                "print vs return",
                ["Keyword/function", "Purpose"],
                [
                    ["`print(...)`", "Show text/value to console"],
                    ["`return ...`", "Send value back to caller"],
                ],
            ),
        ]

    if "in-place modifying methods" in lower and "return `none`" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "nums = [3, 1, 2]\n"
                    "out = nums.sort()\n"
                    "print(nums)   # [1, 2, 3]\n"
                    "print(out)    # None"
                ),
            ),
        ]

    if "bool" in lower and "subclass of `<class 'int'>`" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print(isinstance(True, int))   # True\n"
                    "print(True + True)             # 2\n"
                    "print(False * 10)              # 0"
                ),
            ),
        ]

    if "set.add" in lower and "set.remove" in lower and "set.discard" in lower:
        return [
            table_detail(
                "Set remove behavior",
                ["Method", "If element missing"],
                [
                    ["`remove(x)`", "Raises `KeyError`"],
                    ["`discard(x)`", "No error"],
                ],
            ),
        ]

    if "list.append(item)" in lower and "list.insert(index, item)" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "lst = [1, 3]\n"
                    "lst.append(4)      # [1, 3, 4]\n"
                    "lst.insert(1, 2)   # [1, 2, 3, 4]"
                ),
            ),
        ]

    if "list(set(" in lower and "not preserve original order" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "items = ['b', 'a', 'b', 'c']\n"
                    "unique = list(set(items))\n"
                    "print(unique)   # order not guaranteed"
                ),
            ),
        ]

    if "conditional returns" in lower and "returns `none`" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def f(x):\n"
                    "    if x > 0:\n"
                    "        return x\n"
                    "\n"
                    "print(f(-1))   # None"
                ),
            ),
        ]

    if "`return val1, val2` packs multiple values" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def split_name(full):\n"
                    "    first, last = full.split()\n"
                    "    return first, last\n"
                    "\n"
                    "a, b = split_name('Ada Lovelace')"
                ),
            ),
        ]

    if "global keyword is not needed to mutate elements" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "nums = []\n"
                    "def add_ok():\n"
                    "    nums.append(1)   # no `global` needed (mutation)\n"
                    "\n"
                    "def rebind_needs_global():\n"
                    "    global nums\n"
                    "    nums = [1, 2]"
                ),
            ),
        ]

    if "use `_` as a loop variable name" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "for _ in range(3):\n"
                    "    print('repeat')"
                ),
            ),
        ]

    if "while condition:" in lower and "prevent infinite loops" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "n = 3\n"
                    "while n > 0:\n"
                    "    print(n)\n"
                    "    n -= 1   # state update prevents infinite loop"
                ),
            ),
        ]

    if "manual variable updates are crucial" in lower and "bypass these if not carefully placed" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "i = 0\n"
                    "while i < 4:\n"
                    "    if i == 2:\n"
                    "        i += 1    # update before continue\n"
                    "        continue\n"
                    "    i += 1"
                ),
            ),
        ]

    if "use `_` as a convention for loop variables" in lower and "for _ in range(5)" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "for _ in range(5):\n"
                    "    do_work()"
                ),
            ),
        ]

    if "explicitly declare it using the `global` keyword" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "count = 0\n"
                    "def inc():\n"
                    "    global count\n"
                    "    count += 1"
                ),
            ),
        ]

    if "'key_name' in my_dict" in lower and "not if it's a value" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "d = {'age': 21}\n"
                    "print('age' in d)      # True\n"
                    "print(21 in d)         # False\n"
                    "print(21 in d.values())  # True"
                ),
            ),
        ]

    if "dictionaries are unordered for equality" in lower and "sequence types" in lower:
        return [
            table_detail(
                "Ordered vs unordered equality",
                ["Type", "Order affects equality?"],
                [
                    ["`list`, `tuple`, `str`", "Yes"],
                    ["`dict`, `set`", "No"],
                ],
            ),
        ]

    if "seq[::-1]" in lower and "effectively reversing the sequence" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "s = 'python'\n"
                    "print(s[::-1])     # 'nohtyp'\n"
                    "print(s[-1::-1])   # same result"
                ),
            ),
        ]

    if "falsy values in python" in lower and "all other values are truthy" in lower:
        return [
            table_detail(
                "Falsy quick list",
                ["Falsy examples", "Truthy examples"],
                [
                    ["`0`, `None`, `''`, `[]`, `{}`", "`1`, `'0'`, `[0]`, `{'a': 0}`"],
                ],
            ),
        ]

    if "the `in` operator checks for membership" in lower and "x in [1, 2]" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print('a' in 'cat')   # True (substring)\n"
                    "print(2 in [1, 2])    # True (element)\n"
                    "print('x' in {'x': 1}) # True (dict key)"
                ),
            ),
        ]

    if "use `enumerate` to access both the element and its sequential index" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "letters = ['a', 'b']\n"
                    "for idx, letter in enumerate(letters):\n"
                    "    print(idx, letter)"
                ),
            ),
        ]

    if "use `list(set(my_list))`" in lower and "does not guarantee the original order" in lower:
        return [
            explanation_detail(
                "Optional note",
                "If order matters, use `list(dict.fromkeys(my_list))` to remove duplicates while preserving first appearance order.",
            ),
        ]

    if "assigning mutable `y = x`" in lower and "changes via `y` affect `x`" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = [1]\n"
                    "y = x\n"
                    "y.append(2)\n"
                    "print(x)   # [1, 2]"
                ),
            ),
        ]

    if "assignment `y = x` creates a new reference `y`" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = {'k': 1}\n"
                    "y = x\n"
                    "y['k'] = 2\n"
                    "print(x['k'])   # 2 (same object)"
                ),
            ),
        ]

    if "`x = y` creates a new reference" in lower and "`x = value` points `x` to a new `value` object" in lower:
        return [
            table_detail(
                "Name binding behavior",
                ["Statement", "Effect"],
                [
                    ["`x = y`", "Bind `x` to existing object referenced by `y`"],
                    ["`x = value`", "Bind `x` to object produced by `value` expression"],
                ],
            ),
        ]

    if "integers in the range [-5, 256]" in lower:
        return [
            explanation_detail(
                "Optional exam-safe rule",
                "Treat interning as implementation detail; use `==` for values, not `is`.",
            ),
        ]

    if "string multiplication (`'char' * n`)" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print('ab' * 3)       # 'ababab'\n"
                    "print('ab' * True)    # 'ab'\n"
                    "print('ab' * False)   # ''"
                ),
            ),
        ]

    if "int(float('3.5'))" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "print(int('3'))          # 3\n"
                    "# int('3.5') -> ValueError\n"
                    "print(int(float('3.5'))) # 3"
                ),
            ),
        ]

    if topic_lower == "exam question types":
        return [
            explanation_detail(
                "Optional trace template",
                "Create a tiny table with columns `(line, variable state, output)` and fill it step by step.",
            ),
            example_detail(
                "Optional code example",
                code=(
                    "x = 0\n"
                    "for i in range(3):\n"
                    "    x += i\n"
                    "print(x)\n"
                    "# Trace rows: i=0 -> x=0, i=1 -> x=1, i=2 -> x=3"
                ),
            ),
        ]

    if "def f(a, *args, **kwargs)" in lower:
        return [
            table_detail(
                "Parameter binding map",
                ["Syntax part", "Binds to"],
                [
                    ["`a`", "First positional argument"],
                    ["`*args`", "Remaining positional arguments (tuple)"],
                    ["`**kwargs`", "Keyword arguments (dict)"],
                ],
            ),
        ]

    if "key in my_dict" in lower and "value" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "d = {'x': 1}\n"
                    "print('x' in d)   # True\n"
                    "print(1 in d)     # False\n"
                    "print(1 in d.values())  # True"
                ),
            ),
        ]

    if "nested loops iterate fully" in lower or "inner loop completes all its iterations" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "for i in range(2):\n"
                    "    for j in range(3):\n"
                    "        print(i, j)\n"
                    "# inner loop runs 3 times for each i"
                ),
            ),
        ]

    if "unique pairs" in lower and "range(i+1" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "items = [10, 20, 30, 40]\n"
                    "pairs = []\n"
                    "for i in range(len(items)):\n"
                    "    for j in range(i + 1, len(items)):\n"
                    "        pairs.append((items[i], items[j]))"
                ),
            ),
        ]

    if "type(variable) ==" in lower:
        return [
            explanation_detail(
                "Optional note",
                "Prefer `isinstance(x, T)` when subtype compatibility is desired.",
            ),
            example_detail(
                "Optional code example",
                code=(
                    "values = [1, '2', 3]\n"
                    "for v in values:\n"
                    "    if isinstance(v, int):\n"
                    "        print(v * 2)"
                ),
            ),
        ]

    if "closure" in lower and "enclosing scope" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def make_adder(k):\n"
                    "    def add(x):\n"
                    "        return x + k\n"
                    "    return add\n"
                    "\n"
                    "add5 = make_adder(5)\n"
                    "print(add5(3))   # 8"
                ),
            ),
        ]

    if "without `nonlocal`" in lower and "inner function" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def outer():\n"
                    "    n = 0\n"
                    "    def bad():\n"
                    "        n = n + 1   # UnboundLocalError\n"
                    "    def good():\n"
                    "        nonlocal n\n"
                    "        n += 1"
                ),
            ),
        ]

    if "sets do not maintain element order" in lower:
        return [
            explanation_detail(
                "Optional note",
                "Use `dict.fromkeys(lst)` or an ordered loop if uniqueness plus order must be preserved.",
            ),
        ]

    if "list[index] = value" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "lst = ['a', 'b', 'c']\n"
                    "lst[1] = 'B'\n"
                    "print(lst)    # ['a', 'B', 'c']"
                ),
            ),
        ]

    if "reassigning a parameter within a function" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "def rebind(lst):\n"
                    "    lst = [99]      # local rebinding only\n"
                    "\n"
                    "a = [1, 2]\n"
                    "rebind(a)\n"
                    "print(a)            # [1, 2]"
                ),
            ),
        ]

    if "do not use python keywords" in lower or "built-in function names" in lower:
        return [
            table_detail(
                "Naming pitfalls",
                ["Bad name", "Issue"],
                [
                    ["`for`, `if`, `class`", "Syntax error (keywords)"],
                    ["`list`, `print`, `str`", "Shadows built-ins"],
                ],
            ),
        ]

    if "small integers" in lower and "interned" in lower:
        return [
            explanation_detail(
                "Optional exam-safe rule",
                "Use `==` for value comparison in exams; reserve `is` for identity checks (`None`, singleton objects).",
            ),
        ]

    if "both modify global state" in lower and "return a value" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "total = 0\n"
                    "def add_and_store(x):\n"
                    "    global total\n"
                    "    total += x      # side effect\n"
                    "    return total    # return value"
                ),
            ),
        ]

    if "attempting arithmetic" in lower and "`none` value" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "result = None\n"
                    "# print(result + 5)   # TypeError\n"
                    "if result is None:\n"
                    "    result = 0"
                ),
            ),
        ]

    if "left side of an assignment" in lower and "treated as local" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = 10\n"
                    "def f():\n"
                    "    print(x)   # UnboundLocalError (x is local due to next line)\n"
                    "    x = 20"
                ),
            ),
        ]

    if "chained comparisons" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = 3\n"
                    "print(1 < x < 5)          # True\n"
                    "print((1 < x) and (x < 5))  # equivalent"
                ),
            ),
        ]

    if "automatically converts expressions to boolean" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "value = []\n"
                    "if value:\n"
                    "    print('truthy')\n"
                    "else:\n"
                    "    print('falsy')   # runs"
                ),
            ),
        ]

    if "for variable in sequence" in lower and "for _ in range(n)" in lower:
        return [
            table_detail(
                "Loop form selection",
                ["Use case", "Preferred form"],
                [
                    ["Iterate real items", "`for item in sequence`"],
                    ["Repeat fixed N times", "`for _ in range(N)`"],
                ],
            ),
        ]

    if "use `_` as a variable name when the loop iteration value is not needed" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "for _ in range(3):\n"
                    "    print('tick')\n"
                    "# `_` signals intentionally-unused loop variable"
                ),
            ),
        ]

    if "are immutable (operations create new objects); `list`, `dict`, `set` are mutable" in lower:
        return [
            table_detail(
                "Mutability quick table",
                ["Type family", "In-place update?"],
                [
                    ["`int`, `float`, `str`, `tuple`, `bool`", "No"],
                    ["`list`, `dict`, `set`", "Yes"],
                ],
            ),
        ]

    if "python assignment `name = value`" in lower:
        return [
            explanation_detail(
                "Optional note",
                "Assignment binds a name to an object; it does not copy object contents unless an explicit copy operation is used.",
            ),
        ]

    if "`and` returns the first falsy operand" in lower:
        return [
            table_detail(
                "and/or value behavior",
                ["Expression", "Returns"],
                [
                    ["`A and B`", "First falsy value, else `B`"],
                    ["`A or B`", "First truthy value, else `B`"],
                ],
            ),
        ]

    if "`a is b` checks" in lower and "`a == b` checks" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = [1]\n"
                    "y = [1]\n"
                    "z = x\n"
                    "print(x == y)  # True\n"
                    "print(x is y)  # False\n"
                    "print(x is z)  # True"
                ),
            ),
        ]

    if "`pass` is a null operation" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "if True:\n"
                    "    pass   # TODO: fill logic later"
                ),
            ),
        ]

    if "left side of an assignment" in lower and "treats it as local" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "x = 1\n"
                    "def f():\n"
                    "    print(x)   # error: x considered local due assignment below\n"
                    "    x = 2"
                ),
            ),
        ]

    if "`global` keyword is not needed to mutate elements" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "items = []\n"
                    "def add_item(v):\n"
                    "    items.append(v)   # mutate global list, no global needed\n"
                    "\n"
                    "def reset_items():\n"
                    "    global items\n"
                    "    items = []        # rebinding requires global"
                ),
            ),
        ]

    if "`*=` on strings repeats" in lower:
        return [
            example_detail(
                "Optional code example",
                code=(
                    "s = 'ab'\n"
                    "s *= 3\n"
                    "print(s)        # 'ababab'\n"
                    "lst = [1, 2]\n"
                    "lst *= 2\n"
                    "print(lst)      # [1, 2, 1, 2]"
                ),
            ),
        ]

    return []


def unique_detail_id(base_id: str, taken: set[str], index: int) -> str:
    candidate = f"{base_id}-d{index}"
    serial = index
    while candidate in taken:
        serial += 1
        candidate = f"{base_id}-d{serial}"
    taken.add(candidate)
    return candidate


def main() -> None:
    data = json.loads(CARDS_FILE.read_text(encoding="utf-8"))
    cards = data.get("cards", [])

    points_with_details = 0
    details_added = 0
    cards_changed = 0

    for card in cards:
        sections = card.get("sections", {})
        key_points = sections.get("key_points_to_remember", [])
        if not isinstance(key_points, list) or not key_points:
            continue

        changed_this_card = False
        taken_ids = {str(kp.get("id", "")).strip() for kp in key_points}
        for kp in key_points:
            for detail in kp.get("details", []) if isinstance(kp.get("details", []), list) else []:
                if detail.get("id"):
                    taken_ids.add(str(detail["id"]).strip())

        for kp in key_points:
            text = str(kp.get("text", "")).strip()
            if not text:
                continue

            existing_details = kp.get("details", [])
            if isinstance(existing_details, list) and existing_details:
                points_with_details += 1
                continue

            generated = details_for_point(str(card.get("topic", "")), text)
            if not generated:
                continue

            base_id = str(kp.get("id", "")).strip() or "kp"
            materialized = []
            for idx, detail in enumerate(generated, start=1):
                detail_obj = {
                    **detail,
                    "id": unique_detail_id(base_id, taken_ids, idx),
                }
                materialized.append(detail_obj)

            kp["details"] = materialized
            details_added += len(materialized)
            points_with_details += 1
            changed_this_card = True

        if changed_this_card:
            cards_changed += 1

    notes = data.setdefault("meta", {}).setdefault("notes", [])
    notes.append("Added optional key point detail blocks (tables/examples/explanations) for reference usage.")

    CARDS_FILE.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"Updated {CARDS_FILE}: details added={details_added}, points_with_details={points_with_details}, cards_changed={cards_changed}."
    )


if __name__ == "__main__":
    main()
