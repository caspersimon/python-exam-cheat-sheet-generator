```python
{key_expr: value_expr for item in source}
```
Examples:
```python
{item: len(item) for item in list_1}
{vowel: ord(vowel) for vowel in 'aeiou'}
{num: roman for num, roman in zip(range(1, 6), ['I','II','III','IV','V'])}
```
