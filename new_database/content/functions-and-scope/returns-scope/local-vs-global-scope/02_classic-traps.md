```python
def power(num, factor):
    result = num ** factor
    return result

print(result)   # NameError: result was local to power
```

```python
a = 10
def f():
    a = a + 1   # local-shadowing problem
```
