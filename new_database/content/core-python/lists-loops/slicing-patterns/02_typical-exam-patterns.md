```python
mylist = [10, 15, 20, 25, 30, 35, 40, 45]
mylist[1:len(mylist):3]      # [15, 30, 45]

numbers = [1,2,3,4,5,6,7,8,9,10]
numbers[-1::-2]              # [10, 8, 6, 4, 2]
numbers[::-1][::2]           # [10, 8, 6, 4, 2]
numbers[::-2][::-1]          # [2, 4, 6, 8, 10]  # not the same
```
