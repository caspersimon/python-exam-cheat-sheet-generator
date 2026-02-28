from __future__ import annotations

from typing import Any

from .models import example_detail, explanation_detail, table_detail


def match_details_part3(*, topic_lower: str, lower: str, text: str) -> list[dict[str, Any]] | None:
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

    return None
