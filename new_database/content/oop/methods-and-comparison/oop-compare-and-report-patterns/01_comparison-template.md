```python
def compare(self, other):
    for first, second in [(self, other), (other, self)]:
        better_value = first.metric() > second.metric()
        enough_context = first.count() >= second.count()
        if better_value and enough_context:
            return first.title
    return None   # or 'Either', depending on stem
```
