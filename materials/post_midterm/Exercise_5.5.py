"""
Write a function called 'main' that accepts a pandas DataFrame as an input 
argument.

Each row of the input DataFrame contains data about babies. The DataFrame has
a column called 'Weight' that contains a baby's weight in kilograms 
as a floating point number.

Create a new column called 'Weight (formatted)' that stores each baby's 
weight in grams as a formatted string. During the formatting,
use only the integer part of the weight in grams and attach the 
characters ' g' to the end of each weight measure.

Return the input DataFrame with the new column at the end.

For example:
If we are calling your function as:
main(df)
where 'df' is the DataFrame:
   Height  Weight
0    0.53    3.40
1    0.48    3.50
2    0.50    3.67
then your function should return the DataFrame:
   Height  Weight Weight (formatted)
0    0.53    3.40             3400 g
1    0.48    3.50             3500 g
2    0.50    3.67             3670 g
"""
# You may want to uncomment this:
# import pandas as pd
# df = pd.DataFrame({'Height':[0.53,0.48,0.50],'Weight':[3.40,3.50,3.67]})

# Hint 1: This is a good opportunity to use the 'map' method on a pandas Series 
# object (meaning the 'Weight' column of the DataFrame).

# Hint 2: To hit two birds with one stone, we might as well practice the use of 
# lambda functions as an argument to the 'map' method.

# Hint 3: The lambda function should turn a float that represents weight in 
# kilograms into an integer that represents weight in grams, then 
# turn the integer into a string, and attach the characters ' g' to the end.

# Hint 4: If, instead of explicitly converting data types, you can smuggle an 
# f-string inside the lambda function, you can be extra proud of your code! 
