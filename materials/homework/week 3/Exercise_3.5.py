"""
Write a function called 'main', that accepts an unlimited number of arguments. 
They are all integers and you can assume they are all different. 

The function should return a dictionary. The keys of the dictionary should be 
the arguments that are passed to the function. The values will be lists of 
those passed arguments that are smaller than the key, and that the key 
can be divided by. The lists must be sorted in decreasing order.

For example:
If we are calling your function as: 
main(1, 10, 5, 17, 12, 19, 18, 16)
then the function should return (remember the order of the keys does not matter):
{12: [1], 18: [1], 17: [1], 16: [1], 10: [5, 1], 5: [1], 1: [], 19: [1]}
"""

        
        










# Hint 1: Let us write the function definition line first. How do we receive 
# an arbitrary number of positional arguments in a function? What kind of data 
# structure will these arguments be stored in?

# Hint 2: We'll populate a dictionary with all kinds of data in this exercise. 
# For now, let's just create an empty one and call it something. I'll call it 
# 'x', because that's short.

# Hint 3: Let's iterate through the collection of arguments that the function 
# has received.

# Hint 4: The function argument in the current iteration will be a key in 'x'. 
# The corresponding value will be a list of some kind. So let's create an empty 
# list as the first action within each round of iteration. I'll call it 'y'. 
# Because that's short, too.

# Hint 5: The value to each key should be a list of those arguments that are 
# (1) smaller than the key and (2) yield a zero remainder when we divide the 
# key with them. So why don't we loop through all the arguments (again), and 
# only append those to 'y' that satisfy these two conditions?

# Hint 6: Once we have the right list elements, let's sort them and append the 
# key-value pair to 'x'. What a long exercise!
