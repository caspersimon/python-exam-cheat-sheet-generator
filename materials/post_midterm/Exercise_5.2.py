"""
Write a function called 'main' that accepts a pandas DataFrame as an input 
argument.

The index of the DataFrame is a pandas DatetimeIndex with dates that represent 
unique days. However, the dates are totally unordered.

Your function should return another DataFrame that only contains those rows of
the original input for which the date in the index is in April.

Before returning the output DataFrame, put its rows in increasing chronological 
order.

For example:
If we are calling your function as:
main(df)
where 'df' is the DataFrame:
            A  B
2021-06-16  5  9
2021-07-30  3  2
2021-05-26  2  2
2021-06-11  6  6
2021-05-01  9  5
2021-04-25  5  2
2021-04-14  3  9
2021-07-18  6  6

then your function should return the DataFrame:
            A  B
2021-04-14  3  9
2021-04-25  5  2

"""
# You may want to uncomment this:
# import pandas as pd
# idx = pd.DatetimeIndex(['2021-06-16', '2021-07-30', '2021-05-26', '2021-06-11', '2021-05-01', '2021-04-25', '2021-04-14', '2021-07-18'])
# df = pd.DataFrame({'A':[5,3,2,6,9,5,3,6],'B':[9,2,2,6,5,2,9,6]},index=idx)

# Hint 1: The elements of a pandas DatetimeIndex are objects that have integer 
# attributes like: 'year', 'month', 'day', etc. 

# Hint 2: Combine the 'map' method of the DataFrame index, a lambda function, 
# and the 'month' attribute of an index element to transform the DatetimeIndex 
# into a Series that contains the corresponding month numbers.

# Hint 3: Once you have the month numbers as a Series, you can use them to 
# filter the DataFrame rows via boolean indexing.

# Hint 4: DataFrames have a 'sort_index' method. You will want to use it at
# the very end.
