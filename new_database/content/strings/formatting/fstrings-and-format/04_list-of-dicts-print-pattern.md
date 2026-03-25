```python
students = [{"Name": "Adam", "Grade": 7.5}, {"Name": "Bernard", "Grade": 8.0}]

for student in students:
    print(f"{student['Name']} has received a grade of {student['Grade']:.1f}.")
```
If `students` is a **list**, do not call `.items()` on it. Iterate through the list first, then index each dictionary.
