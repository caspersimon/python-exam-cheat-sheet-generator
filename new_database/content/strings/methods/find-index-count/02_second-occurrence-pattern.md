```python
index = sentence.find('book')
index = sentence.find('book', index + 1)
new_sentence = sentence[:index] + 'novel' + sentence[index + 4:]
```
This targets the **second** `book` only.
