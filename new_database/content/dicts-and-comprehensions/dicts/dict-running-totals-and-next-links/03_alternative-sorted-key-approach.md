A sorted-key running total also works **if** the required output is just the cumulative value per key:
```python
running_total = 0
for key in sorted(d):
    running_total += d[key]
    out[key] = running_total
```
