`text.replace(old, new, 1)` changes only the **first** match from left to right.

To target the second occurrence, the usual exam-safe pattern is:
- find the first one
- search again starting at `index + 1`
- rebuild the string around that second index
