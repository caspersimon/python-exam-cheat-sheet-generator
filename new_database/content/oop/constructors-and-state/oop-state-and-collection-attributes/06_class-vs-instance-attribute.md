```python
class Counter:
    total_created = 0          # class attribute: shared default

    def __init__(self):
        self.count = 0         # instance attribute: one per object
        Counter.total_created += 1
```

- `self.x` belongs to one object
- `ClassName.x` is shared until an instance shadows it with its own `self.x`
