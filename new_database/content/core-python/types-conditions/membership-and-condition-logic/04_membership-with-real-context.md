```python
allowed_countries = {"Belgium", "France", "Germany"}
destination = "France"

destination in allowed_countries     # True
destination in {"Spain", "Italy"}    # False
```
This is the pattern behind many “is this value allowed / included?” answers.
