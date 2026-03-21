"""
Modify the Calculator class below to include an integer attribute called 
'base_number'. The value of this attribute should be passed to the class at the 
time of object construction.

In addition, add four methods to your class as follows: 
1. The 'add' method returns the sum of 'base_number' and 18. 
2. The 'sub' method returns the difference between 'base_number' and 28. 
3. The 'mul' method returns the multiplicative product of 'base_number' and 38.
4. The 'intdiv' method returns the result of the integer division of 
   'base_number' by 48.

Each method above should return an integer.

For example:
If we create an object from your class as:
my_calculator = Calculator(180)
then the method call my_calculator.intdiv() should return the integer: 
3
"""

class Calculator:
    def __init__(self):
        pass

    def add(self):
        pass

    def sub(self):
        pass

# Hint 1: The __init__ constructor method should take an additional positional 
# argument, which will be assigned as the value of the 'base_number' attribute.
# You need to do this assignment inside the __init__ method.

# Hint 2: The four methods are very simple. None of them take any (explicit) 
# arguments, they all have to refer to the 'base_number' attribute of the
# object, and they all return an integer. The first two methods are already 
# half-defined for you.

# Hint 3: Don't forget to erase all the pass statements at the end. Not that it
# matters, of course.
