"""
Assume that you already have a variable called 'x', which is a list 
containing integer values. Furthermore, you have 4 variables called
'a', 'b', 'c', 'd'. All of them contain an integer.

Print a list containing strings that describe the elements of 'x' as follows:
If the element is greater than the value of 'a', use "cat1".
If the element is less than the value of 'b', use "cat2".
If the element is greater than or equal to the value of 'c', use "cat3".
If the element is less than or equal to the value of 'd', use "cat4". 

If the element fits into more than one category, use the highest category. 
So, for example, if both "cat3" and "cat4" apply, use "cat4". 

If the integer doesn't fall into any of the 4 categories, use "catunknown". 

For example:
If x = [5, 10, 15, 20], a = 4, b = 9, c = 13, and d = 15
then your program should print:
['cat4', 'cat4', 'cat4', 'cat3']
"""

# Hint 1: This exercise seems complex, but isn't really. Let's take it slow,
# and create an empty list first. We can call it 'cats'.

# Hint 2: We clearly have to loop through 'x' and examine each of its elements.
# So let's create a loop for that.

# Hint 3: Higher-numbered categories dominate lower numbered ones when both
# apply, so let's check higher-numbered categories first, and then work our way 
# down with a bunch of 'if - elif - else' statements. The 'else' part is for 
# the unknown category, of course. 

# Hint 4: Add the category names to 'cats' (while still inside the loop), 
# and print the resulting list at the very end.
