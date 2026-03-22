"""
Assume that you already have two variables, which are two lists: 
one called 'keys', the other called 'values'. The lists have the 
same length. Both lists consists of integers. The 'keys' list contains
only unique numbers.

Create a dictionary 'x', for which all the keys are taken from the 'keys' list
and all the values from the 'values' list. Pairs are formed from 
elements with the same index in their lists. The only exceptions are  
when the values are divisible by 5, or when the key and the value
are equal to each other. In those cases, the key-value pair is ignored.

For example:
If keys = [3, 2, 1, 4] and values = [3, 37, 60, 79] then the value of x should
be equal to:
{2: 37, 4: 79}
"""

# Hint 1: Why not start by creating an empty dictionary called 'x'?

# Hint 2: There is clearly some looping to be done here. Since we have to work
# with two lists of the same length and corresponding elements, but can only
# loop through one list at a time, it would be handy to have the indices of 
# the elements of the looped list with us, too. That way, we could access the 
# corresponding elements in the other list.

# Hint 3: which of the two lists should we choose for the looping? In the grand
# scheme of things, it doesn't matter, since we can access the elements of both
# with the index. But there is an extra check to be done on the values, so 
# maybe that one is more convenient to use for looping.

# Hint 4: How to check whether a number is divisible by 5? Well, this one
# shouldn't be difficult! And don't forget to check whether the key elements
# are equal to the value elements! And don't forget about the "or" part, either!

# Hint 5: All right, now all that's left is to add the key-value pair to 'x'.
# Given that they satisfy the two conditions above, of course.
