```python
print(1.1 + 2.2 == 3.3)   # False
print([1, 2] == [2, 1])   # False
print({1, 2} == {2, 1})   # True
```

- exact float equality can fail because decimal fractions are stored approximately
- lists / tuples / strings care about order
- sets do not care about insertion order when testing equality
