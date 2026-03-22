"""
Write a function called 'main' that takes any number of positional arguments
as inputs. In addition, it should also take an optional keyword argument that 
has a default integer value of 16. The keyword argument should be named 
'allowed_value'.

The positional arguments are all dictionaries. The keys and values of these 
dictionaries are all integers. Each dictionary key is unique across all the 
input dictionaries.

Your function should return a single dictionary that has all the key-value 
pairs from every input dictionary, provided that the value 
equals the integer stored in 'allowed_value'.

For example: 
If we call your function as: 
main({88: 1, 83: 19}, {58: 15, 52: 18, 99: 16, 49: 16})
then your function should return: 
{99: 16, 49: 16}
"""

# Hint 1: The function definition line is tricky in this one. We need to accept
# an arbitrary number of positional arguments, and we also have a keyword 
# argument with a very specific name ('allowed_value') and a default value
# of 16.

# Hint 2: The return value is a dictionary, so let's create an empty one in the 
# first line of the function. I'll call it 'x'.

# Hint 3: We have to loop through the positional arguments collection, and then
# we have to loop through the key-value pairs of each argument (since the 
# positional arguments are themselves dictionaries).

# Hint 4: As we are iterating through the key-value pairs, we can examine the 
# relation of the value to the keyword argument 'allowed_value', and decide
# whether to include the key-value pair in 'x', or not.

# Hint 5: Don't forget to return 'x' at the end.
