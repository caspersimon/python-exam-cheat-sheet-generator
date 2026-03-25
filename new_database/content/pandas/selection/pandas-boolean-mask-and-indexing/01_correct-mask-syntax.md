```python
df[(df['Age'] > 30) & (df['Gender'] == 'Male')]
df.loc[df['Height'] > 170, ['Player', 'Age']]
```
Use `&` / `|` with **parentheses around each condition**.
