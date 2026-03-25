| Expression | Returns | Original object changed? | Exam trap |
|---|---|---:|---|
| `s.replace(old, new)` | new string | No | reassign or lose change |
| `s.split(sep)` | list | No | returns list, not string |
| `sep.join(parts)` | string | No | `join` is called on separator |
| `lst.append(x)` | `None` | Yes | `return lst.append(x)` returns `None` |
| `lst.sort()` | `None` | Yes | use `sorted(lst)` when you need a value |
| `random.shuffle(lst)` | `None` | Yes | shuffles list in place |
| `df.sort_values(...)` | new DataFrame | No | reassign if you want sorted result stored |
