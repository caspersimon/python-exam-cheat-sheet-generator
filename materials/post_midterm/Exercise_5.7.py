"""
Write a function called 'main' that accepts a pandas Series as an input 
argument. The Series contains first names. Some are spelled correctly, some are
completely in uppercase, and some are completely in lowercase.

Your function should return another Series that only contains those elements
of the input Series that end with a vowel.

The spelling of the names should be corrected to start with a capital letter
and otherwise only contain lowercase letters.

Do not alter the original order of the elements.

For example:
If we are calling your function as:
main(s)
where 's' is the Series:
0     anne
1      BOB
2    cecil
3     Dave
dtype: object

then your function should return the Series:
0    Anne
3    Dave
dtype: object

"""
# You may want to uncomment this:
# import pandas as pd
# s = pd.Series(['anne','BOB','cecil','Dave'],dtype=object)

# Hint 1. Pandas Series have vectorized string methods ('str') that operate on 
# the string elements of the Series one-by-one. You can even do string indexing 
# with them.

# Hint 2. Pandas Series also have an 'isin' method that is excellent for 
# checking whether a Series item is contained in a collection or not.

# Hint 3. You can do boolean indexing on a Series.

# Hint 4. Strings have a 'capitalize' method that you can also use as a 
# vectorized string method to set name spellings into a proper case.
