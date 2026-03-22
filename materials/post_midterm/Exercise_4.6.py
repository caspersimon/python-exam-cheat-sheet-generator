"""
Write a class called 'Main', which accepts a list of index numbers as an 
argument during object construction.

When an object is created from this class, the object should have an
attribute called 'occupied_spaces'. This attribute is a list containing
12 elements. 

The elements of the 'occupied_spaces' list should be either None (if the index
of the element is not in the input argument list) or 'c' (if it is).

For example:
If we create an object from your class as:
my_object = Main([0, 1, 3, 5])
then my_object.occupied_spaces should be equal to the list: 
['c', 'c', None, 'c', None, 'c', None, None, None, None, None, None]
"""






# Hint 1: Let's start with a line that defines a class called 'Main'

# Hint 2: We need to take a few specific steps when an object is created from 
# this class, right? That means, we need to write a __init__ constructor 
# method. So let's define the __init__ method as if it were a function inside
# the class definition.

# Hint 3: Remember: the first positional argument of any method inside a class 
# is always 'self'. But the constructor also accepts an explicit positional 
# argument. Let's call it 'index_list'. Or anything else, really.

# Hint 4: Inside the __init__ method, we need to create a list with 12 elements,
# each of which is either the string 'c' or the null value None, depending
# on whether the index of the element is contained in 'index_list' or not.
# This should be doable.

# Hint 5: Now for the tricky part: the 'occupied_spaces' attribute of the object
# must be set equal to the list we've just created. How do we refer to the 
# object inside a method? And how do we refer to an attribute of an object?
# If you figure these two things out, you're pretty much done with the problem.
