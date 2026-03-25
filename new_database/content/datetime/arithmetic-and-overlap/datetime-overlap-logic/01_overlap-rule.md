Two intervals overlap iff:
```python
start1 < end2 and end1 > start2
```
Equivalent idea: overlap is the opposite of
```python
end1 <= start2 or start1 >= end2
```
