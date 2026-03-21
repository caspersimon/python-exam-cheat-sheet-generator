"""
Write a function called 'main' that takes two arguments: 
(1) a 5-character-long string made up of 3 symbols and 2 spaces in between them, 
    like this: "$ * #"
(2) a one-character optional keyword argument called 'winning_symbol' that 
    has a default string value of '*'.

Your function should return another string, which can take one of two possible
values. 

If all 3 input symbols are equal to the current value of 'winning_symbol', 
then the function should return: 
'[S]-BINGO!!!'
where [S] is replaced by the symbol in 'winning_symbol'  

If the symbols are not equal to 'winning_symbol', then the return value 
should be: '--'

For example: 
If we call your function as: 
main('$ $ $', winning_symbol='$')
then your function should return the string: 
$-BINGO!!!
"""

# Hint 1: Start with the function definition line. Make sure to define the 
# keyword argument with the right name and default value.

# Hint 2: Let's make a string with 3 symbols (and 2 spaces in between) that are
# equal to whatever is contained in the keyword argument 'winning_symbol'.
# This is what we are trying to match the first function argument with.

# Hint 3: Decide if there is a match, and return the appropriate string.
