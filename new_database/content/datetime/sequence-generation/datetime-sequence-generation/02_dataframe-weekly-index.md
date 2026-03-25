```python
dates = [datetime(2023, 1, 1) + timedelta(weeks=i) for i in range(5)]
df = pd.DataFrame(
    {'Day': [d.day for d in dates],
     'Month': [d.month for d in dates],
     'Year': [d.year for d in dates]},
    index=[d.strftime('%d-%m-%y') for d in dates]
)
```
