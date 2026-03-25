| Call | Output | Note |
|---|---|---|
| `'a-b-c'.split('-')` | `['a','b','c']` | returns list of pieces |
| `'-'.join(['a','b'])` | `'a-b'` | separator calls `.join(...)` |
| `'book-book'.replace('book', 'novel', 1)` | `'novel-book'` | third argument limits replacements |

Docs-style optional-argument reminder: `text.replace(old, new[, count])`.
