```python
class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name)
        self.breed = breed
```

Use `class Child(Parent):` to inherit.
Use `super().__init__(...)` when the child should keep the parent’s setup logic.
