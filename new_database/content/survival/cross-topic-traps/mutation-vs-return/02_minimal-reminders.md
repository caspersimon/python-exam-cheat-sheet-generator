```python
# strings: immutable
s = "book-book"
s.replace("book", "novel", 1)
print(s)                     # 'book-book'

# lists: append mutates, returns None
y = []
result = y.append(3)
print(y, result)            # [3] None

# shuffle: in place
words = "hello there you".split()
random.shuffle(words)       # words changed
```
