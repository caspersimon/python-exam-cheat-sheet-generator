| Wrong code | Why |
|---|---|
| `df[df['Age'] > 30 & df['Gender'] == 'Male']` | missing parentheses |
| `df[1, 'Age']` | DataFrame does not use tuple indexing like that here |
| `df.loc(df['Age'] > 30)` | `loc` is an indexer, not a function call |
