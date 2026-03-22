"""
Write a function called 'main' that accepts a string as an argument. You can 
expect the string to have an even number of characters that are either lower- 
or uppercase letters. Lowercase letters have an even-numbered index in the 
string and uppercase letters have an odd-numbered index in the string. 
(E.g.: "aBcDeF".)

Your function should return a string consisting of odd-indexed 
characters in the reverse order, concatenated with even-indexed
characters in the same order (relative to the original argument).

For example:
If we are calling your function as:
main('tDmSzAkCgZaThKqZnAhN') 
then it should return the string: 
'NAZKTZCASDtmzkgahqnh'
"""

# Hint 1: Try to solve the exercise by defining a function with only
# a single return line, using string slicing twice and concatenating the two slices.
