from __future__ import annotations

from typing import Any

from .models import example_detail, explanation_detail, table_detail


def match_details_part1(*, topic_lower: str, lower: str, text: str) -> list[dict[str, Any]] | None:
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
    return None
