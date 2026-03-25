| Wrong pattern | Why |
|---|---|
| `series.map((series - series.mean())**2)` | `map` expects a function / mapping, not a finished Series expression |
| `df['Salary'].map(lambda x: ... if df['Performance_review'] >= 4 else 0)` | condition uses whole column, not current row |
| `df.apply(df['A'] - df['B'])` | `apply` is being misused |
