"""
Write a function called 'main' that accepts an arbitrary number of keyword 
arguments. You can assume that the value of every keyword argument is an 
integer. 

The function should return a dictionary. The keys of the dictionary should be 
the names of the keyword arguments. The values should be the remainders that 
you get when you divide the keyword argument value by 5.

Make sure that the dictionary values are integers. You may need to convert them.

For example:
If we are calling your function as: 
main(mango=7, apple=9, lime=3)
then the function should return:
{'mango': 2, 'apple': 4, 'lime': 3}
"""

# Hint 1: Let us write the function definition line first. How do we receive 
# an arbitrary number of keyword arguments in a function? What kind of data 
# structure will these arguments be stored in?

# Hint 2: We need to return a dictionary, so we might as well make an empty one
# at the start of the function. Let's call it 'x'.

# Hint 3: 'x' needs to be populated by looping over the data structure that 
# contains the received keyword argument names and values. In each iteration of
# the loop, we'll get the remainder from the division of the keyword argument 
# value and 5, and use that -- along with the keyword argument 
# name -- to create a new key-value pair in 'x'. Use the 'int' function to 
# convert the remainders to integers, just in case they are not.

# Hint 4: Don't forget to return 'x' at the end.
