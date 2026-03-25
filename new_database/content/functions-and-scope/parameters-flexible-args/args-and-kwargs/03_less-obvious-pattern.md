```python
def glue(**kwargs):
    result = ''
    for key in kwargs.keys():
        result = key + result
    return result

glue(a='e', b='d')   # 'ba'
```
The values `'e'` and `'d'` do not matter there; only the **keyword names** matter.
