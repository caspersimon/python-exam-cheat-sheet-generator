```python
s1 = pd.Series([10, 20], index=['A', 'B'])
s2 = pd.Series([1, 2], index=['B', 'C'])

s1 + s2
# A    NaN
# B   21.0
# C    NaN
```

Pandas aligns by **index label**, not by row position.
