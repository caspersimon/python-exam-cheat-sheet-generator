```python
# build from two lists
d = {name: age for name, age in zip(names, ages)}

# count frequencies
counts = {}
for grade in grades:
    if grade not in counts:
        counts[grade] = 0
    counts[grade] += 1
```
