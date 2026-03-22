"""
Assume that you already have a variable called 'x', which contains an integer.

Create a new dictionary and call it 'y'. Its keys should be integers indicating 
angles, measured in degrees, from 0 to 45 with a step size of 'x'. 

The values should equal the tangent of the corresponding keys, rounded to 4 
decimal digits.

Import the math package to calculate the tangent of a number.

For example:
If x = 5, then the value of y should be equal to:
{0: 0.0, 5: 0.0875, 10: 0.1763, 15: 0.2679, 20: 0.364, 25: 0.4663, 30: 0.5774, 35: 0.7002, 40: 0.8391, 45: 1.0}
"""

# Hint 1: I think we should start by importing the math package. Seems doable.

# Hint 2: Next step: create an empty dictionary called 'y'. Still doable.

# Hint 3: How about a variable for the angles? Let's call it something and 
# give it a value of 0 to start with.

# Hint 4: Angles going "from 0 to 45 with a step size of 'x'", where 'x' is 
# some other variable whose value we don't know??? This calls for a loop! It 
# is probably a good idea to try a while loop here. (And someone please remind 
# me to make it not infinite!)

# Hint 5: Hmm, tangent, tangent, ..., isn't there a function for that in the 
# math package? Where else would it be? Let's google "python math package"!

# Hint 6: But wait, the function we've found takes angles in radians, while we 
# have them in degrees. I bet there must be a function in that package that 
# turns degrees into radians!

# Hint 7: Are we done? Can we now append the key-value pair to 'y'? No? 
# Oh, yeah, the rounding! At least that one is doable...
