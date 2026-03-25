```python
def add_review(self, score):
    self.review_scores.append(score)

def show_rating(self):
    if self.review_scores:
        return round(sum(self.review_scores) / len(self.review_scores), 1)
```
This is the recurring “store scores, then return the rounded average” pattern.
