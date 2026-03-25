```python
# x has unique integers
y = [value for i, value in enumerate(x) if i == value]
```

Equivalent loop:
```python
y = []
for i, value in enumerate(x):
    if i == value:
        y.append(value)
```
