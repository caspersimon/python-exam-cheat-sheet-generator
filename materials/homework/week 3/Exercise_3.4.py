"""
Write a function called 'main' that takes two arguments: 
(1) a list of values that can be integers (int), floats (float), strings 
(str), or booleans (bool),
(2) an optional keyword argument called 'excluded_type' that has a default 
value of int as a Python data type.

Your function should return another list that has all the elements of the input 
list (in the same order), except for those pairs where the type of the element 
equals the Python data type stored in 'excluded_type'.

Warning:
An optional keyword argument doesn't have to be specified during a function 
call, but that doesn't mean that it is never specified! Thus, the keyword 
argument's value as the function is executed may sometimes be different from its 
default value.

For example: 
If we call your function as: 
main([3.5, True, 3.5, 0, 8, 0, 7.0, 'False', True, 3.5])
then your function should return the list: 
[3.5, True, 3.5, 7.0, 'False', True, 3.5]
"""

# Hint 1: What is most interesting in this exercise is that we are dealing with
# Python data types as arguments that are passed around in function calls. So 
# make sure that when you define the 'main' function, you give it a keyword 
# argument called 'excluded_type' that has a default value of int
# (as a Python data type name) and not 'int' as a string!

# Hint 2: Otherwise, the exercise is rather standard: create an empty list, 
# loop through the elements of the first function argument, decide whether 
# a given element should be included in the result list, append it to the result
# list if necessary, and return the list at the end.

# Hint 3: Remember: you can check the type of a value with the built-in 'type' 
# function. Moreover, the 'type' function has a return value that you can 
# directly compare to what is stored inside the 'excluded_type' keyword 
# argument.
