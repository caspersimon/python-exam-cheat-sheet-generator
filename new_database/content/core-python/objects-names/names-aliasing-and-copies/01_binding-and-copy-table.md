| Pattern | What it means |
|---|---|
| `b = a` | `b` is another name for the **same** object |
| `b = a[:]` | for a list, `b` is a **new outer list** with the same elements |
| `b = list(a)` | another common shallow-copy pattern for a list |
| `a = a + [4]` | builds a **new** list and rebinds `a` |
| `a.append(4)` | mutates the existing list in place |
