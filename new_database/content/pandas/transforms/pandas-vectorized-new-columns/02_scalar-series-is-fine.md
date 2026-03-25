These are valid elementwise operations:
```python
df['A'] + 5
df['Salary'] - mean_salary
(df['A'] - df['A'].mean())**2
```
A scalar broadcasts across the whole Series.
