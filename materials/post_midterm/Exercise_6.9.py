"""
Write a function called 'main' that accepts one list consisting of 
one-character strings.

Your function should return a list of two-character strings. 

The first characters in the output list should be the same as the characters in 
the input list at the same positions.

The second characters in the output list should be the same as the characters 
in the input list 3 positions later.
If, for the second character, you have reached the end of the input list, 
start again at the beginning.

Hint: List slicing and concatenation, list comprehensions, and the zip()
function may all come in handy for a concise solution.

For example:
If we are calling your function as:
main(['p', 'o', 'd', 'o', 'f', 'o', 'p', 'm', 't', 'k', 'h', 'o', 'g']) 
then it should return the list: 
['po', 'of', 'do', 'op', 'fm', 'ot', 'pk', 'mh', 'to', 'kg', 'hp', 'oo', 'gd']
"""