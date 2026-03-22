"""
Complete the class definition below such that it initializes a Car object with 
four attributes that take string values (or, in some cases, the value None): 
'color', 'speed', 'brand', and 'worth'.

'color' and 'speed' should be passed to Car during initialization. 'brand' 
and 'worth', on the other hand, are derived attributes.

If 'color' is brown and 'speed' is slow, then the 'brand' attribute
should be Chevrolet. Otherwise, the 'brand' attribute should be None.

If 'brand' is Chevrolet, then 'worth' should be cheap. If 'brand' is 
not Chevrolet, then 'worth' should be expensive.

Modify the code below so that the class definition works as expected.

For example:
If we create an object from your class as:
my_car = Car("blue", "super slow")
then: 
my_car.color should be equal to 'blue'
my_car.speed should be equal to 'super slow'
my_car.brand should be equal to None
my_car.worth should be equal to expensive
"""

class Car:
    def __init__(self):
        pass


# Hint 1: Think of the additional positional arguments that the __init__ 
# constructor method must take.

# Hint 2: What we want inside the __init__ method is to assign values to object 
# attributes. To do that, you need to think about the uses of the 'self' 
# implicit positional argument.

# Hint 3: If you understand the hints above, then you only need to write a few 
# more if statements and you're done.
