"""
Write a function called 'main' that accepts a string consisting of lowercase 
letters as an argument.

Your function should return a string with the same characters as in the
input string. Except, when a character is present in the string: 'dab',
then the second occurence of that character should be capitalized.

You can be sure that all the characters in the input string have two or more 
occurences.  

Try to solve the problem using only the replace method of strings (and some 
creativity).

For example:
If we are calling your function as:
main('eabcceceadfdebccaefa') 
then it should return the string: 
'eabcceceAdfDeBccaefa'
"""

# Hint 1: Let's loop through the list of characters: dab. 
# In each iteration, we want to replace the second occurence of the given 
# character in the input argument with the uppercase version of the same 
# character.

# Hint 2: Clearly, we can use the replace method of strings to keep updating
# the input argument. The replace method has an optional keyword argument called
# count, which allows us to specify the maximum number of allowed replacements.

# Hint 3: By applying replace twice for every letter, we can solve
# the task  

# Hint 3 (instead of Hints 1-2): Alternatively, you could
# loop over the string, do an uppercase conversion 
# when needed, and join the transformed list of characters back into a string 
# at the end.
