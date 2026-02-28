from __future__ import annotations

from typing import Any

from .models import example_detail, explanation_detail, table_detail


def match_details_part2(*, topic_lower: str, lower: str, text: str) -> list[dict[str, Any]] | None:
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

    return None
