```python
it = iter([10, 20])

print(next(it))   # 10
print(next(it))   # 20
# next(it)        # StopIteration: no values left
```

An iterator remembers where it is. `next(it)` does **not** restart from the beginning.
