"""
Write a function called 'main', that accepts two integer values, 'minimum' and
'maximum', as arguments. 

The function should return a dictionary. The keys of the dictionary are tuples
for all possible combinations of integers between 'minimum' and 'maximum' 
(endpoints included).

The values of the dictionary are the result of the subtraction of the 
two integers in the corresponding key.

For example:
If we are calling your function as: 
main(2, 4)
then it should return:
{(2, 2): 0, (2, 3): -1, (2, 4): -2, (3, 2): 1, (3, 3): 0, (3, 4): -1, (4, 2): 2, (4, 3): 1, (4, 4): 0}
"""

# Hint 1: Let's define 'main' as a function taking two positional arguments.

# Hint 2: If we're going to populate a dictionary with key-value pairs, we 
# might as well define an empty dictionary in the first line inside the 
# function.

# Hint 3: How do we find all possible combinations of integers between 'minimum'
# and 'maximum'? One way to do it would be by using nested for loops, each 
# having an independent running variable going from 'minimum' to 'maximum'.

# Hint 4: the 'range(x, y)' function call gives you a collection of integers 
# from x to y-1, which you can iterate over in a for loop. Use this function 
# call in each of the loops, but make sure to substitute the correct arguments
# for 'x' and 'y'.

# Hint 5: You can build the requested tuple in the inside loop, use it as a 
# new key in the dictionary we are populating, and calculate the value that 
# corresponds to the new key.

# Hint 6: Don't forget to return the dictionary at the end.
