```python
date = datetime.strptime("04.05.2020", "%m.%d.%Y")
(date + timedelta(days=-10)).strftime("%d-%m-%Y")
# '26-03-2020'
```

```python
datetime.strptime("03-02-2013", "%d-%m-%Y").month   # 2
datetime.strptime("03/02/2013", "%m/%d/%Y").month   # 3
```
