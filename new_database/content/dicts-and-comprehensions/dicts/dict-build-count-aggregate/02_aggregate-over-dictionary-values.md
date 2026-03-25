```python
average_score = sum(math_scores.values()) / len(math_scores)
for student in math_scores:
    if math_scores[student] > average_score:
        print(student)
```

```python
max_rating = max(employee_ratings.values())
for employee, rating in employee_ratings.items():
    if rating == max_rating:
        print(employee)
```
