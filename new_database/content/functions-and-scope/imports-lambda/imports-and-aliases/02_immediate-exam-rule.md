If you alias a module, you **must** use the alias:
```python
import math as constants
print(constants.pi * r**2)   # correct
print(math.pi * r**2)        # wrong here
```
