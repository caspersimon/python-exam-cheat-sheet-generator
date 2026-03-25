| Expression | Result | Why |
|---|---:|---|
| `'3' == 3` | `False` | string vs int |
| `3 == 3.0` | `True` | numeric equality |
| `'3' == 3.0` | `False` | string vs float |
| `[]`, `{}`, `''` in `if` | falsey | empty container/string |
| non-empty list/dict/string | truthy | contains something |
| `True == 1` | `True` | booleans are numeric subclasses |
| `False == 0` | `True` | same idea |
