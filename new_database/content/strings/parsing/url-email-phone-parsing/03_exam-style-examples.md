```python
url = "https://www.uva.nl/en/education/bachelors.html"
url.split("//")[1].split("/")[0].split(".")[-1]   # 'nl'

email = "student@uva.nl"
email.split("@")[0]   # 'student'
email.split("@")[1]   # 'uva.nl'
```
