```python
# dict from two lists
d = {name: age for name, age in zip(names, ages)}

# count from 1
for i, value in enumerate(items, start=1):
    print(i, value)

# next-link dict
d = {left: right for left, right in zip(l1[:-1], l1[1:])}
```
