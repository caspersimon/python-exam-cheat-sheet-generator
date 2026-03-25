```python
lunch_start = datetime(self.date.year, self.date.month, self.date.day, 12, 30)
lunch_end = lunch_start + timedelta(minutes=30)
return self.start < lunch_end and self.end > lunch_start
```
