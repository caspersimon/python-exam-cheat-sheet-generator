| Goal | Pattern | Shape preserved? |
|---|---|---:|
| replace missing values | `df.fillna('No value')` | Yes |
| remove incomplete rows | `df.dropna()` | No |
| remove incomplete columns | `df.dropna(axis=1)` | No |
