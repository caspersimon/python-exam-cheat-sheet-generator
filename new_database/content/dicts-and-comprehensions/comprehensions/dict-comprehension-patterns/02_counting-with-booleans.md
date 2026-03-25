```python
grade_curve = {
    grade: sum(v == grade for v in grades.values())
    for grade in dutch_grades
}
```
Because `True` acts like `1` and `False` like `0`, `sum(...)` counts matches.
