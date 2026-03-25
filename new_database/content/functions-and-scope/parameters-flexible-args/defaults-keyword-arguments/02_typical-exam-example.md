```python
def main(x, y=11):
    table = []
    i = 1
    while i < y:
        table.append(f'{x} * {i} = {x*i}')
        i += 1
    return table

main(1)    # valid, because y has a default
```
