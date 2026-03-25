```python
s = "020-525"
s.replace("-", "")   # returns '020525'
s                    # still '020-525' unless reassigned

df["B"]              # Series
df[["B"]]            # DataFrame

for k, v in d:       # error: iterating dict yields keys, not pairs
    ...

print(result)        # NameError if result only existed inside a function
```
