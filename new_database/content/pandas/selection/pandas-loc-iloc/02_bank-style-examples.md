```python
# custom row labels are 1..6
df.loc[2::2, 'B']       # rows with labels 2,4,6
df.iloc[[1,3,5], 1]     # same positions if column B is at position 1
```

```python
df.loc[df.index % 2 == 0, ['B']]   # even labels, one-column DataFrame
```
