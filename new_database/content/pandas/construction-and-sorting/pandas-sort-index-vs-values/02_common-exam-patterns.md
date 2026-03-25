```python
df1.loc[df1['Language'] != 'Dutch'].sort_values('Height', ascending=False)
```
sorts by the **values in column `Height`**.

```python
df1.sort_index(ascending=False).loc[:, ['A', 'C', 'D']]
```
sorts rows by index labels, then keeps selected columns.
