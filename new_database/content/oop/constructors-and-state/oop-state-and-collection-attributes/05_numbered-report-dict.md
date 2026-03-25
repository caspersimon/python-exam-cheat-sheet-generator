```python
def check_garage(self):
    return {
        i: car.get_description()
        for i, car in enumerate(self.cars, start=1)
    }
```
Use `enumerate(..., start=1)` when the output dictionary must start its keys at `1`.
