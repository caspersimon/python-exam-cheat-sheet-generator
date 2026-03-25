```python
df['Bonus'] = df.apply(
    lambda row: row['Salary']*0.05 if row['Performance_review'] >= 4 else 0,
    axis=1
)
```

```python
df['Name_Length'] = df['Name'].map(len)
df['Name_Suffix'] = df['Name'].map(lambda x: x[-2:])
```
