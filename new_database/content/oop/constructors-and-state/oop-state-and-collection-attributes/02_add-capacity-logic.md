```python
def add_car(self, car):
    if len(self.cars) < self.capacity:
        self.cars.append(car)
    else:
        return "Capacity reached."
```

```python
def add_review(self, score):
    self.review_scores.append(score)
```
