```python
def payment_overview(self):
    return (
        f'{self.name} receives ${self.salary} monthly, '
        f'${self.holiday_bonus()} in May and '
        f'${self.year_end_bonus()} in December.'
    )
```
Call helper **methods** if the class defines them.
