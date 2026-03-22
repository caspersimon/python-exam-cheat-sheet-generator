"""
Suppose you are given a list x = ['A','B','A','C','B','A','B']. Write 
a programme that allows the user to find the index of the n-th instance
of 'B' in the list, where 'n' is input by the user of the programme. 
Make sure to tackle the case where the user asks for something that 
doesn't exist. 
"""
x = ['A','B','A','C','B','A','B']
n = input('The index of which iteration of B would you like to find?')
i = -1
try:
    for j in range(int(n)):
        i = x.index('B',i+1)
    print(i)
except ValueError:
    print('There are fewer than ' + n + ' instances of B in the list.') #Either this
    print('There are only ' + str(j) + ' instances of B in the list.')  #or this option is fine for error handling