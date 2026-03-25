| Wrong pattern | Why it fails |
|---|---|
| `def __init__(name, mode):` | missing `self` |
| `return name, mode` inside `__init__` | constructor should not return tuple |
| `name = vehicle_name` | local name only; attribute never stored |
| missing default | call without second arg fails |
