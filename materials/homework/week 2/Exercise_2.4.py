"""
Assume that there is already a variable 'x', which refers to a list with at 
least 5, but maybe more, different integers.

Create a dictionary called 'y', in which the keys are the indexes from the list 
and the values are the values from the list, with one exception: for the 
highest value in the dictionary, the key should be "highest".

For example:
If x = [65, 43, 1, 0, 59, 16, 86, 40, 60] then the value of y should be:
{0: 65, 1: 43, 2: 1, 3: 0, 4: 59, 5: 16, 'highest': 86, 7: 40, 8: 60}
"""

# Hint 1: Let's start by creating an empty dictionary called 'y'.

# Hint 2: I think we have to loop through the list elements. But it would also 
# be very handy to have their indices with them in the loop. This sounds so 
# contrived that they must have talked about how to do it in the lecture.

# Hint 3: Okay, I have the index, I have the element, let's just make a 
# key-value pair out of them and add it to 'y'. But wait! I'd better check 
# first whether the element I have is the highest one in the list.

# Hint 4: How do I find the highest number in a list? Could sorting help?

# Hint 5: OK, now I know what to add to 'y'. Let's get it over with!
