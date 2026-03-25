| Expression | Result | Why |
|---|---:|---|
| `-5 // 3` | `-2` | `//` floors downward, not toward zero |
| `-5 % 3` | `1` | remainder keeps the divisor’s sign |
| `-5 // 2` | `-3` | still floors downward |
| `-5 % 2` | `1` | paired with the floored quotient |

Useful check: `a == (a // b) * b + (a % b)`.
