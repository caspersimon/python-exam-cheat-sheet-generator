If the printed output shows:
```python
1    4
2    5
3    6
Name: B, dtype: int64
```
you want a **Series** selection, such as:
```python
df['B']
df.loc[:, 'B']
```
Not:
```python
df[['B']]
```
