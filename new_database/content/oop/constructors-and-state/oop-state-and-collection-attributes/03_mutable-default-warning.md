Avoid `cars=[]` or `review_scores=[]` as a default parameter in `__init__` unless you really want that same list reused across objects.  
Safer general pattern:
```python
def __init__(self, reviews=None):
    self.reviews = [] if reviews is None else list(reviews)
```
