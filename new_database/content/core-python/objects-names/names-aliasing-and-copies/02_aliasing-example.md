```python
l1 = [1, 2, 3]
l2 = l1
l3 = l1[:]

l1[0] = 99

print(l2)   # [99, 2, 3]  -> same list as l1
print(l3)   # [1, 2, 3]   -> separate outer list
```
Use this pattern whenever the exam asks why one variable changed “unexpectedly”.
