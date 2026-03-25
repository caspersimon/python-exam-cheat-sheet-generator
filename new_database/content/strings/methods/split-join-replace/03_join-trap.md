`join` is called on the **separator string**, not on the list:
```python
'-'.join(words)    # correct
words.join('-')    # wrong
```
