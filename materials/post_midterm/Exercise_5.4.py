"""
Write a function called 'main' that accepts a pandas DataFrame as an input 
argument.

The input DataFrame has at least 4 columns, and the column names are single 
letters. The values in the DataFrame are all integers.

Your function should return another DataFrame in which the rows are sorted 
by the values in the fourth column in decreasing order.

For example:
If we are calling your function as:
main(df)
where 'df' is the DataFrame:
    g   w   a   e
0  96  53  21  77
1  23  10  50  98
2  38  84  80  93

then your function should return the DataFrame:
    g   w   a   e
1  23  10  50  98
2  38  84  80  93
0  96  53  21  77

"""
# You may want to uncomment this:
import pandas as pd
df = pd.DataFrame({'g':[96,23,38],'w':[53,10,84],'a':[21,50,80],'e':[77,98,93]})

# Hint 1: DataFrames have a 'sort_values' method.
