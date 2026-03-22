"""
Assume that you already have a variable called 'x', which contains a list.
The elements of the list are strings consisting of a single letter or a 
single digit. The list may contain duplicate elements.

Create a new variable 'y', which is a dictionary with each of the 
digits as keys and the frequency of each of those digits 
as corresponding values.

For example:
If x = ['1', 'a', 'X', '2', 'b', 'Y', '1', 'a', 'X', '1', 'a', 'X'], 
then the value of y should be equal to:
{'1': 3, '2': 1}
"""

# Hint 1: Let's just create an empty dictionary first, we'll fill it up later.
# Don't forget that it has to be named 'y'.

# Hint 2: It seems like a good idea to examine the elements of the list 
# one-by-one!

# Hint 3: But how do we decide if a one-character string is one of the many 
# possible digits? This one is tricky!

# Hint 4: How do we count how many times an element occurs in a list? There 
# must be a list method for this somewhere...

# Hint 5: Okay, now all that is left is to add the requested key-value pair 
# to the 'y' dictionary. It doesn't even matter if we do it several times, 
# since that just updates an already existing key-value pair with the same 
# thing.
