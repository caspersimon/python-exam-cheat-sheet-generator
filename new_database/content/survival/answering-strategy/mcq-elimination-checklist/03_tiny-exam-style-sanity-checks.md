```python
s = "020-525"
s.replace("-", "")        # returns '020525'
s                         # still '020-525' unless reassigned

df["B"]                   # Series
df[["B"]]                 # DataFrame

for key, value in d:      # error: iterating a dict yields keys, not (key, value) pairs
    ...
```
