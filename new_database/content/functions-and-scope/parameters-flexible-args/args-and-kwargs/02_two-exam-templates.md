```python
def main(*args):
    return {
        'sum': sum(args),
        'pro': math.prod(args),
        'pow': [i**2 for i in args]
    }
```

```python
def main(**kwargs):
    total = 0
    for value in kwargs.values():
        total += value
    return total
```
