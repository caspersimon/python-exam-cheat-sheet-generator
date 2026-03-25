```python
sums = [sum(sub) for sub in x]
y = x[sums.index(max(sums))]
```

Do **not** use `max(x)` unless the question wants lexicographic list order.
