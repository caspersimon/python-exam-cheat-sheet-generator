```python
def main(string):
    date = datetime.strptime(string, '%d-%m-%Y')
    out = [date]
    for _ in range(1, 10):
        out.append(out[-1] + timedelta(weeks=1))
    return [dt.strftime('%d-%m-%Y') for dt in out]
```
Example: `main('01-01-2023')[:3]` starts as `['01-01-2023', '08-01-2023', '15-01-2023']`.
