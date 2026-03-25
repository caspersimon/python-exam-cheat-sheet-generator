```python
self.date = datetime.strptime(date, '%d-%m-%Y')
hour, minute = start.split(':')
self.start = datetime(
    self.date.year, self.date.month, self.date.day,
    int(hour), int(minute)
)
```
