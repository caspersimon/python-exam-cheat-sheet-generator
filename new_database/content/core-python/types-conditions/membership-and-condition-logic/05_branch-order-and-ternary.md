- In an `if / elif / else` chain, put the most specific or highest-threshold branch first.
- Ternary form is `value_if_true if condition else value_if_false`.
- When filtering a collection, apply the condition to **each element**:
  ```python
  [x for x in nums if x > 0]
  ```
  not `if nums > 0`.
- Convert before comparing mixed types such as `'3'` and `3`.
