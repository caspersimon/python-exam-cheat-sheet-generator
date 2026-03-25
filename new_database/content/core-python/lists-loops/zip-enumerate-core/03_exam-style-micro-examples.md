```python
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
[item[0] * item[1] for item in zip(list1, list2)]
# ['a', 'bb', 'ccc']

for i, (g1, g2, g3) in enumerate(zip(player1, player2, player3), start=1):
    match_goals[i] = (g1, g2, g3)
```
