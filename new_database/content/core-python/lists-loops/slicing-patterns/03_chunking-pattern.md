```python
# break x into chunks of size 3
chunks = [x[i:i+3] for i in range(0, len(x), 3)]
```

For `x = ['a','b','c','d','e','f','g','h','i']` this gives:
```python
[['a','b','c'], ['d','e','f'], ['g','h','i']]
```
