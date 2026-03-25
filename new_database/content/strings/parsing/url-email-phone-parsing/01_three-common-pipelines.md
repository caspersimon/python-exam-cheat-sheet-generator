| Task | Safe pipeline |
|---|---|
| URL TLD | `url.split('//')[1].split('/')[0].split('.')[-1]` |
| email local/domain | `local, domain = email.split('@')` |
| phone digits only | `''.join(number.split('-'))` or filter digits |
