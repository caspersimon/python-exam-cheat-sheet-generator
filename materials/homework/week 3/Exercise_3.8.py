"""
Write a function called 'main' that accepts two lists of integers as positional 
arguments. You can assume that the lists are equally long.

The function should return another list that has the same number of elements as
either of the two input lists. In each position, the returned list should 
contain the smaller of the corresponding elements in the input lists.

If the corresponding input list elements happen to be equal, the returned list
should contain the null value None in that position.

Consider using the 'zip' function for looping through the lists.

For example:
If we are calling your function as: 
main(([3, 9, 7, 0], [3, 5, 9, 8]))
then the function should return:
[None, 5, 7, 0]
"""

# Hint 1: Let us write the function definition line first. We can call the two
# positional arguments 'list_1' and 'list_2'.

# Hint 2: Since the return value is a list, we might as well create an empty 
# one in the first line inside the function. 

# Hint 3: Here comes the interesting part. We want to iterate through the two 
# lists in parallel. Let's use the 'zip' function to create an iterable 
# collection of pairs of list elements, and unpack the pairs in the for loop
# into two variables.

# Hint 4: In each iteration, append the smaller variable value to the result
# list. Unless they are equal, of course, in which case you should append the 
# None value. Pay attention: the null value None is not the same as the 
# string 'None'!

# Hint 5: Don't forget to return the result list.
