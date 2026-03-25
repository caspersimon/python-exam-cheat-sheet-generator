```python
s1 = s1.replace('y', 'x', 1).replace('x', 'y', 1)
```
Why this order? Because `y -> x` first, then the **first** `x` from the left is the old `x`, which becomes `y`.
