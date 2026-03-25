```python
s1 = "x and y"
s1 = s1.replace('y', 'x', 1).replace('x', 'y', 1)
# 'y and x'
```
This works because after `y -> x`, the **first** `x` from the left is still the original `x`, which then becomes `y`.
