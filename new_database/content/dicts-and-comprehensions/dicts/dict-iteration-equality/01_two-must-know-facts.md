| Fact | Consequence |
|---|---|
| `for x in d:` iterates over keys | `for key, value in d:` fails unless you iterate over `d.items()` |
| `d1 == d2` compares key-value content | insertion order does **not** matter |
