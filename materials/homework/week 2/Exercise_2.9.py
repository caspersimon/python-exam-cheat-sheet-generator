"""
Assume that there are 2 dictionaries, called 'buyers' and 'sellers'. Both have 
4 key-value pairs. Each value is a list with 5 integers.

The values in the 'buyers' dictionary are the prices that each of the 4 buyers 
is willing to pay for the first, second, ... unit of a product in a market. 

The values in the 'sellers' dictionary are the prices for which each of the 
4 sellers is willing to sell the first, second, ... unit of the product in the 
market.

The product is homogeneous. If a seller's asking price is the same as a buyer's
offer price, the buyer buys the item.

Print the integer value that indicates the number of items traded once all 
(welfare-increasing) transactions have taken place. (That is: how many items
would be sold in an efficiently operating marketplace?)

For example:
If buyers = {'buyer1': [24, 16, 13, 6, 5], 'buyer2': [23, 21, 19, 10, 7], 'buyer3': [21, 20, 15, 13, 10], 'buyer4': [20, 17, 9, 6, 5]},
and sellers = {'seller1': [8, 10, 14, 19, 21], 'seller2': [6, 13, 16, 21, 23], 'seller3': [8, 12, 13, 22, 23], 'seller4': [8, 9, 13, 21, 24]}, 
your program should print: 
10
"""

# WARNING: THIS EXERCISE MAY BE CHALLENGING, BUT IS ULTIMATELY WORTH IT!

# Hint 1: This sounds like a standard microeconomics question, maybe from an 
# exam you've once taken. We have individual demand and supply functions and 
# want to find the equilibrium quantity in the market. How do we do that? 
# Well, as in basic micro: create aggregate demand and supply functions, and 
# find where they intersect!

# Hint 2: Let's get all the buyer prices from the 'buyers' dictionary into a 
# single list (let's call it 'demand'), which we then sort from high to low.

# Hint 3: Let's get all the seller prices from the 'sellers' dictionary into a 
# single list (let's call it 'supply'), which we then sort from low to high.

# Hint 4: Let us now loop through 'demand' (and its index) and count how many
# times the buyer price is at least as large as the corresponding seller 
# price in the 'supply' list. You can, for example, set an integer variable
# called 'quantity_sold' to 0 before the looping, and then just increment it 
# by 1 whenever the buyer "buys" the item from the corresponding seller.

# Hint 5: Don't forget to print the result.
