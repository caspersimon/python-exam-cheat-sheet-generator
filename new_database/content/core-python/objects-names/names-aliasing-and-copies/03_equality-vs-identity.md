| Expression | Checks | Typical use |
|---|---|---|
| `a == b` | same value/content | normal equality questions |
| `a is b` | same object in memory | identity / singleton checks such as `x is None` |

If the question is not explicitly about object identity, `==` is usually the intended comparison.
