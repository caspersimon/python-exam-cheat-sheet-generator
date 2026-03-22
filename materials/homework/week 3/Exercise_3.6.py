"""
Write a function called 'main' that accepts a list of integers. This is a list
with the sales volumes of all the firms in a market.

The function should return the decrease in the Herfindahl-Hirschman Index (HHI) 
as an integer when a firm with a sales volume of 40 enters the 
market, while the sales volumes of the other firms stay the same.

As a reminder, the HHI is a measure of market concentration. It is the sum of 
the squares of the percentage market shares of all firms in the market. 
Percentage market shares are rounded to whole numbers before the HHI 
calculation. The HHI is therefore always an integer between 0 and 10,000.

For example:
If we are calling your function as: 
main([47, 21, 27, 29, 11, 6, 18]) 
then it should return the integer: 
224
"""

# Hint 1: Let's define a function first that takes a list as a positional 
# argument. Calling the argument 'sales_before_entry' is probably helpful.

# Hint 2: It's clear that we will have to calculate the HHI twice. Once with 
# the new entrant's sales volume, and once without. The classy way to write 
# this would be to define an inner function that calculates the HHI for any 
# list of sales volumes, and then call that inner function twice from the outer
# function with different arguments.

# Hint 3: Let's be classy, and define an inner function called 'calculate_hhi' 
# that takes a list as a positional argument.

# Hint 4: The inner function will return an integer as the HHI value. Let's call
# that integer 'hhi' and set it to zero at the start of the inner function.

# Hint 5: We're calculating the sum of squared market shares, right? 
# So we definitely need to know total sales. How do we calculate total sales 
# from a list of sales volumes? There's a handy function just for this purpose!

# Hint 6: OK, so we have total sales! It shouldn't be hard to loop 
# through the sales volumes, calculate the percentage market share of each 
# company, round it to a whole number, square it, and add it to 'hhi'.

# Hint 7: We're still in the inner function! Don't forget to return 'hhi'.

# Hint 8: Now back to the outer function 'main'! Call the inner function once 
# with 'sales_before_entry', and once with 'sales_before_entry' plus 40
# as the last element. Return the difference from 'main' and go get a coffee!
