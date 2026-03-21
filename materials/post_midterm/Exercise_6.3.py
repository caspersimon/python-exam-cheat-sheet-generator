"""
Write a function called 'main' that accepts one dictionary consisting of keys 
and values that are both strings with lower-case letters.

Your function should return a dictionary that is the same as the input except 
for the following cases: 
- the key does not start with a vowel, or
- the value does end with a vowel. 
Vowels include: a, e, i, o, and u.
In the above mentioned cases, the key-value pairs of the input dictionary 
should not be included in the output dictionary.

For example:
If we are calling your function as:
main({'ba': 'efb', 'dg': 'fbcuo', 'ae': 'fe', 'ofcei': 'uedb', 'gbdue': 'ie', 
      'oeci': 'ogbfu', 'bgfoa': 'id', 'ua': 'idg', 'uobf': 'cabf', 
      'bda': 'od', 'od': 'ib', 'aebuc': 'ocueb', 'co': 'edfoi'}) 
then it should return the dictionary: 
{'ofcei': 'uedb', 'ua': 'idg', 'uobf': 'cabf', 'od': 'ib', 'aebuc': 'ocueb'}
"""
