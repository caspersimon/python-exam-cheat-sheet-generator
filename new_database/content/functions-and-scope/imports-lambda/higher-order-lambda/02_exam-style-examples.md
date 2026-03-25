```python
funcs = [lambda a, b: a + b, lambda a, b: a * b]
funcs[0](1, 2) ** funcs[1](1, 2)   # 3 ** 2 = 9
```

```python
def calculation(func, *args):
    return sum(func(el) for el in args)

calculation(lambda x: x + 5, 1, 2, 3, 4)  # 30
```
