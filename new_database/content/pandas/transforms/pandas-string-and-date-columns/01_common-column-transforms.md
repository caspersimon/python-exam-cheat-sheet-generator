```python
df['Sex_abbr'] = df['Gender'].map(lambda x: 'M' if x == 'Male' else 'F')
df['Name_Length'] = df['Name'].map(len)
df['Name_Suffix'] = df['Name'].map(lambda x: x[-2:])
df['Occupation'] = df['Occupation'].map(
    lambda x: 'Software Developer' if x == 'Engineer' else x
)
```
