"""
Write a function called 'main' that accepts a pandas DataFrame as an input 
argument.

Each row of the input DataFrame contains personal data about people under 
the following column names: 'Age', 'Gender', 'Height', and 'Nationality'. 'Age'
and 'Height' are always integers, while 'Gender' and 'Nationality' take string 
values.

Calculate the median height in the dataset by nationality.

The result that your function returns should be a pandas Series object. Its 
index should contain the possible values that nationality takes in the
dataset (in alphabetic order). The corresponding values in the Series should 
show the group medians.

For example:
If we are calling your function as:
main(df)
where 'df' is the DataFrame:
   Age  Gender  Height Nationality
0   50      NA     186      French
1   49      NA     165      French
2   50  Female     189       Dutch
3   42      NA     167      French
4   30      NA     171       Dutch
5   62    Male     194      French
6   57      NA     170     British
7   27    Male     173      French

then your function should return the Series:
British    170
Dutch      180
French     173
dtype: float64

"""

# You may want to uncomment this:
# import pandas as pd
# df = pd.DataFrame({'Age':[50,49,50,42,30,62,57,27],'Gender':['NA','NA','Female','NA','NA','Male','NA','Male'],
#                    'Height':[186,165,189,167,171,194,170,173],'Nationality':['French','French','Dutch','French','Dutch','French','British', 'French']})

# Hint 1. DataFrames have a 'groupby' method for exactly these kind of data 
# operations.

# Hint 2. After specifying the grouping variable, select the variable to be 
# analyzed.

# Hint 3. The 'median' method calculates medians.

# Hint 4. Pandas Series have a 'sort_index' method, although you will not 
# actually need it if you use 'groupby' to solve this problem, because 'groupby' 
# returns sorted groups already. If you use something other than 'groupby', then
# don't forget to sort the Series index at the end.
