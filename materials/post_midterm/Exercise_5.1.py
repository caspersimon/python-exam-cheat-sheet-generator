"""
Write a function called 'main' that accepts a pandas DataFrame as an input 
argument.

The column names of the DataFrame are single letters, some of them lowercase, 
some of them uppercase.

Your function should return another DataFrame that contains only the lowercase
columns of the original input without changing their order. 

The DataFrame's index should stay the same regardless of the number of lowercase
columns.

For example:
If we are calling your function as:
main(df)
where 'df' is the DataFrame:
   A  b
0  2  6
1  7  4

then your function should return the DataFrame:
   b
0  6
1  4

"""
# You might want to uncomment this:
# df = pd.DataFrame({'A':[2,7],'b':[6,4]})


# Hint 1: DataFrames have a 'columns' property, which gives you an iterable 
# collection of column names.

# Hint 2: There is a string method for checking whether a string contains only 
# lowercase letters. It is called 'islower'. But you can check whether a 
# string equals its lowercase version directly just as well.
