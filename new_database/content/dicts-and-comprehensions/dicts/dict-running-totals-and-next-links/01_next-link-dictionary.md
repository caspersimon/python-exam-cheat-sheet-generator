```python
def main(l1):
    return {left: right for left, right in zip(l1[:-1], l1[1:])}
```
Example:
```python
main([1, 3, 2, 4])   # {1: 3, 3: 2, 2: 4}
```
