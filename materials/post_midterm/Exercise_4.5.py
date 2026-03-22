"""
Write a function called 'main' that accepts a string consisting of lowercase 
letters as an argument.

Your function should return a list that describes how often the letters in the
list: ['b', 'c', 'd'] occur in the input string. 

If a letter occurs only once, the description should be: 
"The string contains the character 'X' 1 time."
where X should be replaced by the letter in question.

If a letter occurs more than once, or not at all, the description should be: 
"The string contains the character 'X' N times."
where X should be replaced by the letter in question, and N by the number of
occurrences of the letter.

For example:
If we are calling your function as:
main('behhbhfeggfdeggbeg') 
then it should return the list: 
['The string contains the character 'b' 3 times.',
 'The string contains the character 'c' 0 times.',
 'The string contains the character 'd' 1 time.']
"""

# Hint 1: Let's define an empty list called 'result' in the first line inside 
# the 'main' function.

# Hint 2: We probably need to iterate through the letters in ['b', 'c', 'd'].
# So let's do that!

# Hint 3: In each iteration, we need to count how many times a letter occurs 
# in the input string (check out the 'count' string method!) and decide whether 
# to use the word "time" or "times" based on the count. Store these two things
# in two separate variables.

# Hint 4: As a next step, let's append an f-string with the proper sentence to 
# 'result'. Inside the f-string, you'll need to refer to the letter in question,
# to its count in the input string, and to the "time" / "times" word.

# Hint 5: One more thing: there is a pair of quotes inside each f-string. The 
# easiest way to put them there is to write the f-string itself with double-
# quotes.

