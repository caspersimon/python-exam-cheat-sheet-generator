```python
(datetime.strptime('2023/1/10', '%Y/%m/%d') - datetime(2023, 1, 1)).days + 1
# 10
```
Without `+ 1`, the difference from Jan 1 to Jan 10 is `9` whole days.
