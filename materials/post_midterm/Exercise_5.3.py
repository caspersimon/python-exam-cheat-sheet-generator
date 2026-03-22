"""
Write a function called 'main' that accepts a pandas DataFrame as an input 
argument.

The input DataFrame has several columns and rows. One column is called 'A', 
another one is called 'B', and there might be others as well. The values in 
the DataFrame are all integers.

Your function should return another DataFrame that only contains those rows
of the input argument for which the value in the 'A' column is 
smaller than, or equal to, the value in the 'B' column. 

The columns in the output should be the same as in the input.

For example:
If we are calling your function as:
main(df)
where 'df' is the DataFrame:
   B  A  C
0  1  3  1
1  4  4  5
2  3  3  2
3  4  5  5
4  3  2  2

then your function should return the DataFrame:
   B  A  C
1  4  4  5
2  3  3  2
4  3  2  2

"""
# You may want to uncomment this:
# import pandas as pd
# df = pd.DataFrame({'B':[1,4,3,4,3],'A':[3,4,3,5,2],'C':[1,5,2,5,2]})

# Hint 1: DataFrame columns are pandas Series objects.

# Hint 2: Comparing two Series objects yields another Series with True and False 
# values, corresponding to the item-by-item comparison.

# Hint 3: You can do boolean indexing (i.e. indexing with a Series that only 
# has True and False values) on a DataFrame.
