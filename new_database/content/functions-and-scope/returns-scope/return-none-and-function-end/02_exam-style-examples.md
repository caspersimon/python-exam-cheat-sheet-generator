```python
def main(x=0):
    if x > 0:
        return True
    if x < 0:
        return False

print(main())   # None
```

```python
def main(x):
    y = []
    ...
    return [y.append(i)]   # [None], because append returns None
```
