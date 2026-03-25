```python
def add_tag(tag, tags=[]):
    tags.append(tag)
    return tags
```

That same list is reused across calls.

Safer pattern:
```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
    tags.append(tag)
    return tags
```
