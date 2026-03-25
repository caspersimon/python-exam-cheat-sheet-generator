```python
x = ['a','b','c','d','e','f','g','h','i']
chunks = [x[i:i+3] for i in range(0, len(x), 3)]
# [['a','b','c'], ['d','e','f'], ['g','h','i']]
```
