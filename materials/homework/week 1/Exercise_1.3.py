"""
Imagine that you are writing cashier software for Albert Heijn. The cashiers
scan items one-by-one, and you have to take into account package discounts
automatically (e.g. "Get 4 for the price of 3!")

Assume that you already have a variable called 'package_price', another 
variable called 'individual_price' and a variable called 'package_size'
indicating how many items a package contains.

You can assume that it is always cheaper to buy as many packages as possible 
to fill the order. Also, prices are integers.

Print the total amount to be paid when a customer buys 64 items.

Make sure that the printed total amount is also an integer.

For example:
If package_price is 20, individual_price is 5, and package_size is also 5, 
then your program should print:
260
"""

# Hint 1: how many full packages fit into 64 items if the number of 
# items in a package equals the value of the variable 'package_size'?
# Have a look at the integer division operator!


# Hint 2: how many items are left, once you've fit as many as possible into
# packages?
# Have a look at the division remainder operator!
