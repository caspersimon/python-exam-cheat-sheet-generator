`replace(old, new, 1)` changes only the **first** match from left to right.

To target the second occurrence, either:
- find the first one, then search again from `index + 1`, or
- do a careful two-step replacement if the order is safe.
