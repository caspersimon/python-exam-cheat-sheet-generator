| Form | Meaning |
|---|---|
| `x[a:b]` | start at `a`, stop **before** `b` |
| `x[a:b:c]` | same, but jump by `c` each time |
| `x[::-1]` | reversed copy |
| `x[-1::-2]` | start at last item, move left by 2 |
| `x[1:len(x):3]` | indices `1, 4, 7, ...` |
