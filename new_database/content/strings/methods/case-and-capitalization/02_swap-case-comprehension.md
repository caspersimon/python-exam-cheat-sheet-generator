```python
[letter.upper() if letter.islower() else letter.lower() for letter in list_1]
```

Proper-noun cleanup pattern:
```python
for word in names:
    sentence = sentence.replace(word, word.capitalize())
```
