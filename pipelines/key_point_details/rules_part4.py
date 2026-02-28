from __future__ import annotations

from typing import Any

from .models import example_detail, explanation_detail, table_detail


def match_details_part4(*, topic_lower: str, lower: str, text: str) -> list[dict[str, Any]] | None:
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
    return None
