| Situation | Use |
|---|---|
| transform each element of one Series | `series.map(func)` |
| need multiple columns from same row | `df.apply(func, axis=1)` |
| no custom logic; simple arithmetic | direct vectorized ops |
