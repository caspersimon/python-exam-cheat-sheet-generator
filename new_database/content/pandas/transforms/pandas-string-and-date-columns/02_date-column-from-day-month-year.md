```python
df['Date'] = pd.Series([
    datetime(y, m, d).strftime('%d-%m-%Y')
    for d, m, y in zip(df['Day'], df['Month'], df['Year'])
])
```
