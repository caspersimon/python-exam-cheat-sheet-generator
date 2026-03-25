```python
list1 = [1, 2, 3]
list2 = ['a', 'b', 'c']
[item[0] * item[1] for item in zip(list1, list2)]
# ['a', 'bb', 'ccc']
```

```python
player1 = [1, 0, 2]
player2 = [0, 1, 1]
player3 = [2, 2, 0]
match_goals = {}

for i, (g1, g2, g3) in enumerate(zip(player1, player2, player3), start=1):
    match_goals[i] = (g1, g2, g3)

# match_goals == {1: (1, 0, 2), 2: (0, 1, 2), 3: (2, 1, 0)}
```
