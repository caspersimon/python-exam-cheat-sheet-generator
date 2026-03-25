```python
my_flight = Flight("KLM", "Amsterdam", "Paris")
my_flight.set_date(my_flight, "29-02-2022")   # wrong
```
Why? Python already passes `my_flight` as `self` automatically.  
Correct:
```python
my_flight.set_date("29-02-2022")
```
