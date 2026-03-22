"""
Write a function called 'main' that accepts one list as an argument. The list 
consists of sublists, in which the first element is a string and the other
5 elements are integers. 

Your function should return a dictionary, where the keys are the strings from 
every sublist and the values are sub-dictionaries. 

The values of the sub-dictionaries are the integers of the sublists. 
The keys of the sub-dictionaries are strings from the following list (in this 
order): ['cat 1', 'cat 2', 'cat 3', 'cat 4', 'cat 5']

Hint: Try to solve this problem with a dictionary comprehension inside another 
dictionary comprehension. Alternatively, build the outside dictionary with a
for-loop, and the sub-dictionaries inside with a dict comprehension.

For example:
If we are calling your function as:
main([['Shilpa', 73, 68, 59, 75, 54], ['Chitrashi', 74, 73, 63, 65, 72], ['Arya', 60, 58, 76, 77, 59], ['Vidya', 51, 74, 79, 74, 70]]) 
then it should return the dictionary: 
{'Shilpa': {'cat 1': 73, 'cat 2': 68, 'cat 3': 59, 'cat 4': 75, 'cat 5': 54}, 
 'Chitrashi': {'cat 1': 74, 'cat 2': 73, 'cat 3': 63, 'cat 4': 65, 'cat 5': 72}, 
 'Arya': {'cat 1': 60, 'cat 2': 58, 'cat 3': 76, 'cat 4': 77, 'cat 5': 59}, 
 'Vidya': {'cat 1': 51, 'cat 2': 74, 'cat 3': 79, 'cat 4': 74, 'cat 5': 70}}
"""
