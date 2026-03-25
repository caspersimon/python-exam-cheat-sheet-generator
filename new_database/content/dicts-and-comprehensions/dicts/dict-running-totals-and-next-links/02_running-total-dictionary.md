```python
def main(d):
    result = {}
    for output_key in d:
        result[output_key] = sum(v for k, v in d.items() if k <= output_key)
    return result
```
This preserves the original keys while computing “sum of values whose keys are <= current key”.
