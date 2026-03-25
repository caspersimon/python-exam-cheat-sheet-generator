```python
def is_anagram(word_1, word_2):
    w1 = word_1.replace(" ", "").lower()
    w2 = word_2.replace(" ", "").lower()
    return sorted(w1) == sorted(w2)
```
