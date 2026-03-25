| Goal | Pattern |
|---|---|
| shift by N days | `dt + timedelta(days=N)` |
| shift by N weeks | `dt + timedelta(weeks=N)` |
| whole-day difference | `(dt2 - dt1).days` |
| day of year | `(dt - datetime(dt.year, 1, 1)).days + 1` |
