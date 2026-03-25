```python
def main(*args):
    local = []
    domain = []
    for email in args:
        local.append(email.split('@')[0])
        domain.append(email.split('@')[1])
    return pd.DataFrame({'local': local, 'domain': domain})
```
