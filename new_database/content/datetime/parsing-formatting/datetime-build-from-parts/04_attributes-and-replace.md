```python
dt.year
dt.month
dt.day
dt.weekday()
```

```python
new_dt = dt.replace(year=2025, month=1)
```

`replace(...)` returns a **new datetime**; it does not mutate the original one in place.
