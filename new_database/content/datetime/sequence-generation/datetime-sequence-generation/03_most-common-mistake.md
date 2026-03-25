If you store strings too early, the next line `previous_date + timedelta(...)` fails because the previous item is no longer a datetime.
