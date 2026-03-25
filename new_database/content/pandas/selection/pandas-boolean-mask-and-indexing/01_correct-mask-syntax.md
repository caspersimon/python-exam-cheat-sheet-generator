```python
df[(df['Age'] > 30) & (df['Gender'] == 'Male')]
df.loc[df['Height'] > 170, ['Player', 'Age']]
```
Correct exam options use `&` / `|` with **parentheses around each condition**.
