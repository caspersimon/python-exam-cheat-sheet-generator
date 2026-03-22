"""
Write a function called 'main' that accepts two pandas DataFrames as input 
arguments. 

The first DataFrame (let's call it 'address') has two columns: 'Name' and 
'Town'. 'Name' contains people's first names, and 'Town' contains the name of 
the town where they live. There may be several people in the dataset who live
in the same town.

The second DataFrame (let's call it 'province') also has two columns: 'Town' 
and 'Province'. It shows which Dutch province each town is located in. In this 
DataFrame, the town names are unique. The province names may, of course, be
duplicated.

Create a new column in the 'address' DataFrame and call it 'Province', too. 
For each person, this column should show the name of the province in which 
they live.

If a person's town is not in the 'province' DataFrame, then the 'Province'
column of the 'address' DataFrame should contain the string No province.

Return the extended 'address' DataFrame at the end of your function.

For example:
If we are calling your function as:
main(address, province)
where 'address' is the DataFrame:
      Name    Town
0      Ann   Paris
1  Bridget   Assen
2   Oliver  Dokkum
3   Summer  Dokkum

and 'province' is the DataFrame:
         Town   Province
0   Hoogeveen    Drenthe
1       Assen    Drenthe
2       Emmen    Drenthe
3   Harlingen  Friesland
4      Dokkum  Friesland
5  Leeuwarden  Friesland
6  Middelburg    Zeeland
7        Goes    Zeeland
8  Vlissingen    Zeeland

then your function should return the DataFrame:
      Name    Town     Province
0      Ann   Paris  No province
1  Bridget   Assen      Drenthe
2   Oliver  Dokkum    Friesland
3   Summer  Dokkum    Friesland

"""

# You may want to uncomment this:
# import pandas as pd
# address = pd.DataFrame({'Name':['Ann', 'Bridget', 'Oliver', 'Summer'],'Town':['Paris', 'Assen', 'Dokkum', 'Dokkum']})
# province = pd.DataFrame({'Town':['Hoogeveen', 'Assen', 'Emmen', 'Harlingen', 'Dokkum', 'Leeuwarden', 'Middelburg', 'Goes', 'Vlissingen'],
#                          'Province':['Drenthe', 'Drenthe','Drenthe', 'Friesland', 'Friesland', 'Friesland', 'Zeeland', 'Zeeland', 'Zeeland']})

# Hint 1: What you really want is a simple DataFrame left merge. 
# Check out the 'merge' DataFrame method.

# Hint 2. When pandas finds no match during a merge operation, it enters a 
# missing value in the corresponding DataFrame cell.

# Hint 3. Missing values in a DataFrame can easily be replaced. Take a look at 
# the 'fillna' DataFrame method.
