# Question Digest


## 2025 Sample Final Plus Answers (`sample-final-plus-answers`)

### sample-final-plus-answers-q01 — vehicle class defaults

You'd like to define a class called Vehicle. It should have two attributes: name and mode, which you want to be initialized during object creation.
The name attribute can be any string, and it must be passed to the object during creation. The mode attribute is also a string, but it doesn't necessarily need to be passed to the object constructor. If it isn't specified at object construction, then the mode attribute should be equal to the string "land".
For example, if we create a Vehicle object as:
my_car = Vehicle("Mazda")
then the following two conditions should both be true:
my_car.name == "Mazda"
my_car.mode == "land"
Which of the following code segments achieves what you want?

- **A**
```python
class Vehicle:
    def __init__(self, vehicle_name, vehicle_mode="land"):
        self.name = vehicle_name
        self.mode = vehicle_mode
```

- **B**
```python
class Vehicle:
    def __init__(self, vehicle_name, vehicle_mode):
        self.name = vehicle_name
        self.mode = vehicle_mode
```

- **C**
```python
class Vehicle:
    def __init__(self, vehicle_name, vehicle_mode="land"):
        return name, mode
```

- **D**
```python
class Vehicle:
    def __init__(vehicle_name, vehicle_mode):
        name = vehicle_name
        mode = vehicle_mode
```

Correct: **A**

---

### sample-final-plus-answers-q02 — book rating output

Take a look at the following class definition.

Suppose that we create a Book object and call its add_review method three times, like this:
book_1 = Book("The Lightning Thief", "Rick Riordan")
book_1.add_review(5)
book_1.add_review(3)
book_1.add_review(3)

What will then the following command print to the screen?
print(book_1.show_rating())

- **A** `3.7`

- **B** `4`

- **C** `None`

- **D** `3.67`

Correct: **A**

---

### sample-final-plus-answers-q03 — student grade formatting

Imagine that you have a list called students, which is populated by a number of dictionaries.
Each dictionary in the students list has two keys: "Name" and "Grade". The corresponding values are student names (as strings) and course grades (as floats).
For each student, you'd like to print the following text to the screen:
[NAME] has received a grade of [GRADE].
where [NAME] is substituted by the name of the student and [GRADE] is substituted by the actual course grade. The course grade should be displayed to one decimal place after the decimal point.
For example, if
students = [{"Name": "Adam", "Grade": 75}, {"Name": "Bernard", "Grade": 80}]
then you'd like to see the following two lines printed to the screen:
Adam has received a grade of 75.
Bernard has received a grade of 80.
Which of the following code segments will achieve what you want?

- **A**
```python
for student in students:
    print(f"{student['Name']} has received a grade of {student['Grade']}. ")
```

- **B**
```python
for student, grade in students.items():
    print(f"{student} has received a grade of {student['Grade']}. ")
```

- **C**
```python
for student in students:
    print(f"{student['Name']} has received a grade of " + str(student["Grade"]))
```

- **D**
```python
for student, grade in students.items():
    print(f'{student} has received a grade of {grade}.')
```

Correct: **A**

---

### sample-final-plus-answers-q04 — phone number formatting

You need to write a function called format_phone_number that formats phone numbers.
The output of the function should be a string that represents a 10-digit number. The input argument is also a string with 10 digits, but the digits may be separated by dashes (the "-" character) at various places.
For example, the following function calls:
format_phone_number("020-525-1400")
format_phone_number("020-5251400")
format_phone_number("020-525-14-00")
should all return the string:
"0205251400"
Which of the following code segments does not achieve what you want?

- **A**
```python
def format_phone_number(number):
    number.replace("-", "")
    return number
```

- **B**
```python
def format_phone_number(number):
    return number.replace("-", "")
```

- **C**
```python
def format_phone_number(number):
    digits = []
    for char in number:
        if char in "0123456789":
            digits.append(char)
    return "".join(digits)
```

- **D**
```python
def format_phone_number(number):
    return "".join(number.split("-"))
```

Correct: **A**

---

### sample-final-plus-answers-q05 — pandas even-row selection

You have a pandas DataFrame called df that looks like this, when printed:

      A    B    C    D
1   9.1  9.5  9.0  6.9
2   6.4  8.2  7.5  1.7
3   2.5  5.3  8.8  3.0
4   6.7  3.6  7.2  6.9
5   8.4  1.9  8.2  3.3
6   8.1  8.4  9.9  2.2

Suppose that you'd like to create a new DataFrame that looks like this, when printed:

      B
2   8.2
4   3.6
6   8.4

Which of the following code lines will achieve what you want?

- **A** `df.loc[df.index % 2 == 0, ["B"]]`

- **B** `df[2, 4, 6, "B"]`

- **C** `df.iloc[[2, 4, 6], 2]`

- **D** `df.loc[2::2, "B"]`

Correct: **A**

---

### sample-final-plus-answers-q06 — pandas df2 derivation

There are two pandas DataFrames: df1 and df2. They look like this, when printed:
print(df1)

     A    B    C    D
1  5.0  8.2  9.5  4.4
2  6.0  2.4  9.1  3.3
3  3.2  5.2  8.9  3.6
4  7.8  8.7  7.9  8.0
5  1.2  9.7  2.9  3.0

print(df2)

     A    C    D
4  7.8  7.9  8.0
3  3.2  8.9  3.6
2  6.0  9.1  3.3

Which of the following code lines could not have created df2 from df1?

- **A** `df2 = df1.sort_index(ascending=False).loc[:, ["A", "C", "D"]]`

- **B** `df2 = df1.iloc[[3, 2, 1], [0, 2, 3]]`

- **C** `df2 = df1.loc[2:4, ["A", "C", "D"]].sort_values("D", ascending=False)`

- **D** `df2 = df1.loc[2:4, ["A", "C", "D"]].sort_values("C")`

Correct: **A**

---

### sample-final-plus-answers-q07 — datetime month parser

Take a look at the following code segment.

from datetime import datetime

def get_months(date_strings):
    dates = []
    for date_str in date_strings:
        if "-" in date_str:
            dates.append(datetime.strptime(date_str, "%d-%m-%Y"))
        elif "/" in date_str:
            dates.append(datetime.strptime(date_str, "%m/%d/%Y"))
        else:
            dates.append(None)
    return [date.month if date is not None else None for date in dates]

Suppose that you call the function like this:
get_months(["03/02/2013", "03.02.2013", "03-02-2013"])
What does the function call return?

- **A** `[3, None, 2]`

- **B** `[2, None, 3]`

- **C** `[3, 2]`

- **D** `[2, 3]`

Correct: **A**

---

### sample-final-plus-answers-q08 — dictionary comprehension lengths

You have a list of strings called list_1, in which every element is unique.
Which of the following code lines will create a dictionary, in which the keys are the elements of list_1 and the values are the number of characters in the corresponding key?

- **A** `{item: len(item) for item in list_1}`

- **B** `[len(item) for item in list_1]`

- **C** `{item for item in list_1 if len(item) > 0}`

- **D** `{len(item): item for item in list_1}`

Correct: **A**

---

### sample-final-plus-answers-q09 — Datetime parsing

Take a look at the following code segment.

Suppose that you call the function like this:
get_months(["03/02/2013", "03.02.2013", "03-02-2013"])

What does the function call return?

- **A** `[3, None, 2]`

- **B** `[2, None, 3]`

- **C** `[3, 2]`

- **D** `[2, 3]`

Correct: **A**

---

### sample-final-plus-answers-q10 — Datetime day-of-year

Suppose that you want to write a function called day_of_year that takes a datetime value and returns the number of the day that the datetime value represents within the year. The return value is therefore always an integer between 1 and 366.

For example, the function call:
day_of_year(datetime(2022, 2, 1))
should return the integer:
32

Which of the following code segments will achieve what you want? (You can assume that the datetime and timedelta classes are already imported from the datetime module.)

- **A**
```python
def day_of_year(dt):
    return (dt - datetime(dt.year, 1, 1)).days + 1
```

- **B**
```python
def day_of_year(dt):
    return timedelta(dt - datetime(dt.year, 1, 1)) + 1
```

- **C**
```python
def day_of_year(dt):
    return dt - datetime(dt.year, 1, 1) + 1
```

- **D**
```python
def day_of_year(dt):
    return (dt - datetime(dt.year, 1, 0)).days
```

Correct: **A**

---

### sample-final-plus-answers-q11 — Dictionary comprehension

You have a list of strings called list_1, in which every element is unique.
Which of the following code lines will create a dictionary, in which the keys are the elements of list_1 and the values are the number of characters in the corresponding key?

- **A** `{item: len(item) for item in list_1}`

- **B** `[len(item) for item in list_1]`

- **C** `{item for item in list_1 if len(item) > 0}`

- **D** `{len(item): item for item in list_1}`

Correct: **A**

---

### sample-final-plus-answers-q12 — Case swapping

Suppose that you have a list of letters called list_1. Some letters are upper case, others are in lower case.
You'd like to create another list that contains the same letters in the same order, but you want to turn every upper case letter into its lower case version, and every lower case letter into its upper case version.
Which of the following code lines will achieve what you want?

- **A** `[letter.upper() if letter.islower() else letter.lower() for letter in list_1]`

- **B** `[x if x in 'abcdefghijklmnopqrstuvwxyz'.upper() else x.lower() for x in list_1]`

- **C** `Both achieve what you want`

- **D** `None achieves what you want`

Correct: **A**

---

### sample-final-plus-answers-q13 — Comparisons and types

Suppose you have three variables x, y, z, as follows:
x = '3'
y = 3
z = 3.0

What are the outputs of the following lines of code?
print(x == y)
print(y == z)
print(x == z)
print(x == y == z)

- **A**
```python
False
True
False
False
```

- **B**
```python
True
True
True
True
```

- **C**
```python
False
False
False
True
```

- **D**
```python
True
False
False
False
```

Correct: **A**

---

### sample-final-plus-answers-q14 — Loops

You need to write a simple loop that iterates over the integers from 1 to 10, and in each iteration, prints the sum of the current and the previous number. (In the first iteration, just take the previous number to be 0.)
For example:
1 + 0 = 1
2 + 1 = 3
3 + 2 = 5
...
10 + 9 = 19

Choose the program that will print the correct output (i.e.: only the sums).

- **A**
```python
i = 0
while i <= 10:
    print(i + (i-1))
    i += 1
```

- **B**
```python
previous = 0
for i in range(1, 11):
    print(i + previous)
    previous = i
```

- **C** `Both of the above work`

- **D** `Neither of above works`

Correct: **B**

---

### sample-final-plus-answers-q15 — Functions and scope

Executing the following program will produce an error. Why?

- **A** `Result is a local name and cannot be referenced outside of the function.`

- **B** `** is not a valid Python operator.`

- **C** `The syntax of the f-string is incorrect.`

- **D** `You can only use either print or return, but not both.`

Correct: **A**

---

### sample-final-plus-answers-q16 — Lambda functions

You already have a list named list_1 with 2 lambda functions as follows:
list_1 = [lambda a, b: a + b, lambda a, b: a * b]

What would be printed by the following code snippet?
print(list_1[0](1, 2) ** list_1[1](1, 2))

- **A** `6`

- **B** `7`

- **C** `8`

- **D** `9`

Correct: **D**

---

### sample-final-plus-answers-q17 — Empty-sequence equality chain

You have the following function called main:
def main(x):
    y = []
    for i in x:
        if len(i) == 0:
            y.append(True)
        else:
            y.append(False)
    return y[0] == y[1] == y[2]

What will be printed by the following lines:
print(main([{}, {}, {}]))
print(main([[1], [2, 2], [3, 3, 3]]))
print(main([[1], [2], [3]]))

- **A**
```python
True
False
False
```

- **B**
```python
False
False
True
```

- **C**
```python
True
False
True
```

- **D**
```python
True
True
True
```

Correct: **D**

---

### sample-final-plus-answers-q18 — List chunking into sublists

How do you break a list into a list of lists, where each sublist contains 3 elements?
For example:
If you have the original list x as:
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
How do you create:
y = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]

- **A** `y = [x[i:(i + 3)] for i in range(0, 7, 3)]`

- **B** `y = [x[i[0]::3] for i in enumerate(x)]`

- **C** `Both of the above work`

- **D** `Neither of above works`

Correct: **A**

---

### sample-final-plus-answers-q19 — Dictionary running totals

You have to write a function called main that accepts a dictionary as an input argument.
Both the keys and the values of the input are integers.
Return another dictionary that has the same keys as the input argument. For each output key, the corresponding value should be calculated as the sum of those values from the input dictionary whose keys are smaller than or equal to the output key in question.
For example:
main({5: 1, 2: 5, 4: 2})
should return a dictionary that is equal to:
{5: 8, 2: 5, 4: 7}
Which of the following programs works as intended?

- **A**
```python
def main(d):
    result = {}
    for output_key in d.keys():
        result[output_key] = sum([v for k, v in d.items() if k <= output_key])
    return result
```

- **B**
```python
def main(d1):
    running_total = 0
    d2 = {}
    for key in sorted(d1.keys()):
        running_total += d1[key]
        d2[key] = running_total
    return d2
```

- **C** `Both of the above work as intended`

- **D** `None of the above works as intended`

Correct: **C**

---

### sample-final-plus-answers-q20 — Dictionary equality with zip and enumerate

What is the result of the following program?

l1 = [1, 2, 3, 4]
l2 = [2, 3, 4, 5]

d1 = {}
for key, value in zip(l1, l2):
    d1[key] = value

d2 = {}
for key, value in enumerate(l2, 1):
    d2[key] = value

print(d1 == d2)

- **A** `True`

- **B** `False`

- **C** `An error message.`

- **D** `None of the above`

Correct: **A**

---

### sample-final-plus-answers-q21 — Dictionary iteration semantics

d1 = {1: 10, 2: 20, 3: 30, 4: 40}
The following codes all print the same value, except one. Which one?

- **A**
```python
result = 0
for key, value in d1:
    result += value
print(result)
```

- **B**
```python
result = 0
for key in d1.keys():
    result += d1[key]
print(result)
```

- **C**
```python
result = 0
for value in d1.values():
    result += value
print(result)
```

- **D**
```python
result = sum(d1.values())
print(result)
```

Correct: **A**

---

### sample-final-plus-answers-q22 — String count method

You have the following string
x = 'Amsterdam'
Which script, using the count string method, would print the following value:
1

- **A** `print(count(x, 'a'))`

- **B** `print(x.count('a'))`

- **C** `Both scripts would deliver that result`

- **D** `Neither script would deliver that result`

Correct: **B**

---

### sample-final-plus-answers-q23 — Higher-order function returning 30

Take a look at the following function definition.

def calculation(func, *args):
    result = 0
    for el in args:
        result += func(el)
    return result

Which of the following function calls would return the number 30 as a result?

- **A** `calculation(lambda x: x + 5, 1, 2, 3, 4)`

- **B** `calculation(lambda x: x**2, 1, 2, 3, 4)`

- **C** `Both function calls would lead to that result`

- **D** `Neither function call would lead to that result`

Correct: **C**

---

### sample-final-plus-answers-q24 — Circle area imports and aliases

If you know the radius r of a circle and you want to calculate its area, you need the value of pi from the math package and apply the formula:
πr²
Suppose that the variable r already contains the radius of the circle. Which script does not print the correct answer for the area?

- **A**
```python
import math
print(math.pi * r ** 2)
```

- **B**
```python
from math import pi
print(pi * r ** 2)
```

- **C**
```python
import math as constants
print(math.pi * r ** 2)
```

- **D**
```python
from math import pi as constant
print(constant * r ** 2)
```

Correct: **C**

---


## 2022 Final Exam (`final-exam-solutions-for-python-programming-62oop21`)

### final-exam-solutions-for-python-programming-62oop21-q01 — OOP Fundamentals

Take a look at the following class definition.

class Flight:
    def __init__(self, airline, origin, destination, capacity=300):
        self.airline = airline
        self.origin = origin
        self.destination = destination
        self.capacity = capacity

    def set_date(self, date):
        self.date = date

Given the class definition above, trying to execute the following two code lines will result in a Python error.
my_flight = Flight("KLM", "Amsterdam", "Paris")   # Code line 1
my_flight.set_date(my_flight, "29-02-2022")         # Code line 2
Why?

- **A** `The first argument (my_flight) should not have been passed to the set_date method in Code line 2.`

- **B** `The capacity of the flight is not specified as an argument in Code line 1.`

- **C** `The argument self is missing in Code line 1.`

- **D** `The date string passed as an argument in Code line 2 represents an invalid date.`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q02 — OOP Fundamentals

You have the following definition for a Book class.

class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.review_scores = []

    def add_review(self, score):
        self.review_scores.append(score)

    def num_reviews(self):
        return len(self.review_scores)

    def average_score(self):
        if self.num_reviews() > 0:
            return sum(self.review_scores) / len(self.review_scores)

Suppose that you also want to write a method called compare that compares the book to another book and gives a recommendation for which one to read. A book is better than another book if its average review score is higher than the second book's and it has at least as many reviews as the second book. The compare method should return the title of the better book. If neither book is better than the other, then it should return None.

For simplicity, you can assume that both books have at least one review already.

Which method definition achieves what you want?

- **A**
```python
def compare(self, other):
    avg_better = self.average_score() > other.average_score()
    no_fewer_reviews = self.num_reviews() >= other.num_reviews()
    if avg_better and no_fewer_reviews:
        return self.title
    elif not avg_better:
        return other.title
    else:
        return None
```

- **B**
```python
def compare(self, other):
    for first, second in [(self, other), (other, self)]:
        avg_better = first.average_score() > second.average_score()
        no_fewer_reviews = first.num_reviews() >= second.num_reviews()
        if avg_better and no_fewer_reviews:
            return first.title
    return None
```

- **C** `Both methods above compare the book objects as intended.`

- **D** `Neither of the two methods above compare the book objects as intended.`

Correct: **B**

---

### final-exam-solutions-for-python-programming-62oop21-q03 — Strings

You would like to write a function called get_tld that extracts the top-level domain from the URL of a website. The function takes the URL as the input string in the following format:
"https://www.[SECOND-LEVEL DOMAIN].[TOP-LEVEL DOMAIN]/[FOLDER 1]/[...]/[FOLDER N]/[PAGE NAME].html"
and returns the top-level domain as a string.

For example, the function call:
get_tld("https://www.uva.nl/en/education/bachelor-s/bachelors.html")
should return the string:
"nl"

Which of the following code segments would not achieve what you want?

- **A**
```python
def get_tld(url):
    url_1 = url.split(".")[-1]
    return url_1.split("/")[0]
```

- **B**
```python
def get_tld(url):
    url_1 = url.split("//")[1]
    url_2 = url_1.split("/")[0]
    return url_2.split(".")[-1]
```

- **C**
```python
def get_tld(url):
    return url.split("//")[1].split("/")[0].split(".")[-1]
```

- **D**
```python
def get_tld(url):
    url_1 = url[url.find("www") + 2:]
    url_2 = url_1.split("/")[0]
    return url_2.split(".")[-1]
```

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q04 — Strings

You're trying to write a function called is_anagram, which takes two strings as inputs and checks whether they are anagrams of each other. That is: whether one of them can be written by rearranging the letters of the other. Upper case and lower case versions of a letter count as the same letter, and whitespace characters don't count at all.

For example, the following function calls should all return the boolean value True:
is_anagram("Old West Action", "Clint Eastwood")
is_anagram("eleven plus two", "twelve plus one")
is_anagram("I am a weakish speller", "William Shakespeare")

while the following function call should return the boolean value False:
is_anagram("one plus two", "three")

Which of the following code segments achieves what you want?

- **A**
```python
def is_anagram(word_1, word_2):
    return sorted(list(word_1.replace(" ", "").lower())) == sorted(list(word_2.replace(" ", "").lower()))
```

- **B**
```python
def is_anagram(word_1, word_2):
    return word_1.replace(" ", "").lower().sort() == word_2.replace(" ", "").lower().sort()
```

- **C**
```python
def is_anagram(word_1, word_2):
    return list(word_1.replace(" ", "").lower()).sort() == list(word_2.replace(" ", "").lower())
```

- **D**
```python
def is_anagram(word_1, word_2):
    return sorted(list(word_1)).replace(" ", "").lower() == sorted(list(word_2)).replace(" ", "").lower()
```

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q05 — Pandas

You have a pandas Series called s, which contains floats. You'd like to create a new Series, in which each element is equal to the square of the difference between the corresponding element in s and the mean of the elements in s.

For example, if s is the Series:
0    2.0
1    2.0
2    3.0
3    5.0
dtype: float64

then you want the new Series to be:
0    1.0
1    1.0
2    0.0
3    4.0
dtype: float64

Which of the following code segments does not achieve what you want?

- **A** `s.map((s - s.mean())**2)`

- **B** `(s - s.mean())**2`

- **C** `s.map(lambda x: (x - s.mean())**2)`

- **D** `(s - s.mean()).map(lambda x: x**2)`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q06 — 7-pandas-2

You have a pandas DataFrame called df. It has a column called "A" and a column called "B". Both contain numbers.

You'd like to create a column called "C", which contains the difference of the numbers in columns "A" and "B". Which of the following code lines will achieve what you want?

- **A** `df["C"] = df["A"] - df["B"]`

- **B** `df["C"] = df["A"].map(lambda x: x - df["B"])`

- **C** `df["C"] = df.columns["A"] - df.columns["B"]`

- **D** `df["C"] = df.apply(df["A"] - df["B"])`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q07 — 7-pandas-3

You have a pandas DataFrame called df that looks like this, when printed:

      A    B    C    D
1   8.7  4.6  9.5  7.0
2   7.3  1.5  6.3  7.1
3   4.3  9.0  2.9  3.3
4   4.8  2.5  5.1  3.0
5   1.6  1.4  6.7  3.5
6   2.4  3.7  7.6  1.3

Suppose that you'd like to create a new Series that only contains those elements of column "D" of df that are smaller than 5.0. So the Series should look like this, when printed:

3    3.3
4    3.0
5    3.5
6    1.3
Name: D, dtype: float64

Which of the following code lines will not achieve what you want?

- **A** `df.loc[2:6, df.columns[-1]]`

- **B** `df.loc[df["D"] < 5, "D"]`

- **C** `df.loc[3:6, "D"]`

- **D** `df.iloc[2:6, 3]`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q08 — 7-pandas-4

You have two DataFrames: df1 and df2. They look like this when printed:

print(df1)

   Age  Height  Female        City Language
0   23     167    True      Berlin   German
1   36     175    True   Frankfurt   German
2   17     182   False   Antwerpen    Dutch
3   25     177    True    Eindhoven    Dutch
4   36     178   False        Lyon   French
5   52     185   False       Basel   German
6   46     168    True   Innsbruck   German

print(df2)

   Age  Height  Female        City Language
5   52     185   False       Basel   German
4   36     178   False        Lyon   French
1   36     175    True   Frankfurt   German
6   46     168    True   Innsbruck   German
0   23     167    True      Berlin   German

Which of the following code segments could have created df2 from df1?

- **A** `df1.loc[df1["Language"].isin(["French", "German"])].sort_values("Height", ascending=False)`

- **B** `df1.loc[df1["Language"] != "Dutch"].sort_values("Age", ascending=False)`

- **C** `df1.loc[~df1["Language"].isin(["Dutch"]), ["Age", "Height", "City", "Language"]].sort_index(ascending=False)`

- **D** `df1.loc[df1["Language"] != "Dutch"].sort_index(axis=1)`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q09 — 8-comprehensions-1

You have a list of mountain peaks and their heights in meters, all formatted as "[PEAK NAME]: [HEIGHT]m". For example, a few elements of the list are:
"Denali: 6,190m", "Aconcagua: 6,961m", "Kilimanjaro: 5,895m", ...

As you can see, the comma (",") is used as a thousand separator in the height. The list is called mountains.

You'd like to create a dictionary called peaks from the mountains list. The peak names would be the keys, and the corresponding integer values. Continuing the example above, a few key-value pairs of the peaks dictionary should be:
"Denali": 6190, "Aconcagua": 6961, "Kilimanjaro": 5895, ...

Which of the following two code segments achieves what you want?

- **A** `peaks = {peak.split(":")[0]: int(peak.split(": ")[1][:-1].replace(",", "")) for peak in mountains}`

- **B**
```python
names = [peak.split(":")[0] for peak in mountains]
heights = [int(peak.split(": ")[1].replace(",", "").replace("m", "")) for peak in mountains]
peaks = dict(zip(names, heights))
```

- **C** `Both code segments above achieve the intended outcome.`

- **D** `Neither of the two code segments above achieves the intended outcome.`

Correct: **C**

---

### final-exam-solutions-for-python-programming-62oop21-q10 — 8-comprehensions-2

You have a dictionary called grades, in which the keys are unique student ID's (as strings) and the corresponding values are each student's Python course grades (as floats).

You'd like to create another dictionary called grade_curve, in which the keys are the 18 possible Dutch course grades (1.0, 1.5, 2.0, ..., 10) as floats, and the corresponding (integer) values are the number of students in grades who have that particular grade.

Take a look at the following code segment to create the grade_curve dictionary.

dutch_grades = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0,
                6.0, 6.5, 7.0, 7.5, 8.0, 8.5, 9.0, 9.5, 10.0]
grade_curve = {grade: sum([v == grade for v in grades.values()]) for grade in dutch_grades}

Do you think this code segment will always work as intended? If not, then why not?

- **A** `Yes, the code will always work as intended.`

- **B** `The code will not work as intended if there are certain grades that no student has received. That will lead to an error in constructing the dictionary comprehension.`

- **C** `The code will not work as intended, because the keys of the grades dictionary are not used in the list comprehension inside the sum function.`

- **D** `The code will not work as intended, because including a list comprehension inside a dictionary comprehension will lead to a Python syntax error.`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q11 — 8-datetime-1

What does the following code segment print to the screen?

from datetime import datetime, timedelta

date = datetime.strptime("04.05.2020", "%m.%d.%Y")
print((date + timedelta(days=-10)).strftime("%d-%m-%Y"))

- **A** `26-03-2020`

- **B** `04-24-2020`

- **C** `15-04-2020`

- **D** `05-14-2020`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q12 — 8-datetime-2

Suppose you have the following definition for a Meeting class, which records basic information about meetings in a calendar application.

You would like to add a method called lunch_meeting to this class, which returns a boolean value indicating whether there is any overlap between the official lunchtime (12:30 - 13:00) and the time of the meeting.

For example, if you construct a Meeting object as:
my_meeting = Meeting('Ask for salary raise', "25-05-2022", start_time='12:00', length=45)
then the method call:
my_meeting.lunch_meeting()
should return the boolean value True.

Which of the following code segments will achieve what you want?

- **A**
```python
def lunch_meeting(self):
    lunch_start = datetime(self.date.year, self.date.month, self.date.day, 12, 30)
    lunch_end = lunch_start + timedelta(minutes=30)
    return self.start < lunch_end and self.end > lunch_start
```

- **B**
```python
def lunch_meeting(self):
    return self.start < "13:00" and self.end > "12:30"
```

- **C**
```python
def lunch_meeting(self):
    return start_time <= "13:00" and start_time + length > "12:30"
```

- **D**
```python
def lunch_meeting(self):
    lunch_start = datetime(self.date.year, self.date.month, self.date.day, 12, 30)
    lunch_end = datetime(self.date.year, self.date.month, self.date.day, 13, 0)
    return self.start >= lunch_end or self.end <= lunch_start
```

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q13 — Basic logic 2

Suppose you have a variable x which contains a list of tuples, as follows:

x = [(1, 2), (3, 4), (5, 6), (7, 8)]

Choose the correct output for the following line of code.

(x[0][1] * x[-3][0]) == (x[-1][1] - x[-4][1])

- **A** `True`

- **B** `False`

- **C** `NameError`

- **D** `SyntaxError`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q14 — Basic loop 2

Which of the following code segments will print every even number between 0 and 20 (including 0 and 20) to the screen?

- **A**
```python
for i in range(0, 20):
    if i % 2 == 0:
        print(i)
```

- **B**
```python
i = 0
while i <= 20:
    if i % 2 == 0:
        print(i)
    i += 1
```

- **C**
```python
for i in list(range(0, 20)):
    print(i if i % 2 == 0 else None)
```

- **D**
```python
i = 0
while i < 21:
    print(i)
    i += 1
```

Correct: **B**

---

### final-exam-solutions-for-python-programming-62oop21-q15 — Basic scope 2

Choose the correct statement about the program below:

- **A** `a is a global variable. b, c, d are local variables.`

- **B** `a, b are global variables. c, d are local variables.`

- **C** `a, b, c, d are global variables.`

- **D** `a, c, d are global variables. b is a local variable.`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q16 — final-dictionary-1

You have to write a function called main, which takes a list of unique integers as an argument and returns a dictionary.

The output dictionary should consist of all key-value pairs for which the key is an element of the input list and the value is the next element of the input list. When there is no "next element" any more, leave the key-value pair out of the dictionary.

For example, if your function is called as:
main([1, 3, 2, 4])
then it should return the dictionary:
{1: 3, 3: 2, 2: 4}

Which of the following programs work(s) according to the requirements?

- **A**
```python
def main(l1):
    result = {}
    index = 0
    while True:
        index = index + 1
        if index >= len(l1):
            break
        else:
            result[l1[index]] = l1[index + 1]
    return result
```

- **B**
```python
def main(l1):
    result = {}
    for index, value in zip(l1[:-1], l1[1:]):
        result[index] = value
    return result
```

- **C** `Both programs work as required`

- **D** `Neither of the two programs works as required`

Correct: **B**

---

### final-exam-solutions-for-python-programming-62oop21-q17 — final-dictionary-2

What will be printed by the following program?

- **A** `True`

- **B** `False`

- **C** `An error message`

- **D** `None`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q18 — final-dictionary-3

d1 = {1: 2, 2: 1}

The following code segments all print exactly the same output, except for one. Which one?

- **A**
```python
result = 1
for x in d1.values():
    result *= x
print(result)
```

- **B**
```python
result = -1
for x in d1.keys():
    result += d1[x]
print(result)
```

- **C**
```python
result = 4
for x in d1.items():
    result = result // x[1]
print(result)
```

- **D**
```python
result = -4
for x in d1:
    result /= d1[x]
print(result)
```

Correct: **D**

---

### final-exam-solutions-for-python-programming-62oop21-q19 — final-functions-1

Suppose that you have a string called s1, which contains several letters. The letter "x" and the letter "y" occur exactly once in the string, and "x" always precedes "y".

You'd like to print out a string that looks just like s1, except that the letters "x" and "y" should be swapped.

For example, if:
s1 = "axbyc"
then you'd like to print:
aybxc

Reminder: The replace string method has a third argument, which allows you to specify the maximum number of replacements you want to make, counting from left to right.

- **A**
```python
s1 = s1.replace('x', 'y', 1).replace('y', 'x', 1)
print(s1)
```

- **B**
```python
s1 = s1.replace('y', 'x', 1).replace('x', 'y', 1)
print(s1)
```

- **C**
```python
s1.replace('x', 'y', 1).replace('y', 'x', 1)
print(s1)
```

- **D**
```python
s1.replace('y', 'x', 1).replace('x', 'y', 1)
print(s1)
```

Correct: **B**

---

### final-exam-solutions-for-python-programming-62oop21-q20 — final-functions-2

Take a look at the following function definition.

What will be returned by the following function call:
glue(a='e', b='d')

- **A** `ab`

- **B** `cd`

- **C** `ba`

- **D** `dc`

Correct: **C**

---

### final-exam-solutions-for-python-programming-62oop21-q21 — final-functions-3

Take a look at the following function definition.

What will be printed to the screen by the following code?
print(tester())

- **A** `1`

- **B** `-1`

- **C** `0`

- **D** `None`

Correct: **A**

---

### final-exam-solutions-for-python-programming-62oop21-q22 — List lambda 2

Assume that you have a variable called x, which contains a list of integers.

Which of the following code segments will create another list that has every element of x multiplied by 2?

For example, if
x = [1, 2, 3, 4, 5]
then which of the following code segments will result in the list:
[2, 4, 6, 8, 10]

- **A** `list(map(lambda i : i * 2, x))`

- **B** `[(lambda i : i * 2)(item) for item in x]`

- **C**
```python
y = lambda i : i * 2
[y(i) for i in x]
```

- **D** `All three code segments would work as intended`

Correct: **D**

---

### final-exam-solutions-for-python-programming-62oop21-q23 — List logic 2

Which of the following programs creates a new list y, in which the elements are those elements of list x that are equal to their indices?
You can assume x consists of unique integers.

For example, if:
x = [0, 2, 4, 3, 5, 9, 6, 7, 8, 1, 10]
then the program should create a new list y such that:
y = [0, 3, 6, 7, 8, 10]

- **A**
```python
y = []
for i, j in enumerate(x):
    if i == j:
        y.append(i)
```

- **B**
```python
y = []
for i, j in enumerate(x):
    if i == j:
        y.append(j)
```

- **C** `y = [i for i in x if i == x.index(i)]`

- **D** `All three programs would work as intended`

Correct: **D**

---

### final-exam-solutions-for-python-programming-62oop21-q24 — List loop 2

Assume that you have a list called x, which is a list of multiple sub-lists containing integers.

Which of the following programs will create a new list y that is equal to the sub-list of x whose sum of elements is the highest?

You can assume that the sum of elements in each sub-list is a different number, so that there is only one that is the highest.

For example, if:
x = [[8, 20, 300], [7, 8, 9], [10, 11, 12], [40, 5, 6]]
then y should be:
y = [8, 20, 300]

- **A** `y = max(x)`

- **B**
```python
z = []
for i in x:
    z.append(sum(i))
y = x[z.index(max(z))]
```

- **C**
```python
x.sort()
y = x[-1]
```

- **D** `y = [i for i in x if sum(i) == max(x)]`

Correct: **B**

---


## 2023 Trial Final Study Guide (`final-exam-study-guide-trial-python-basics-2023`)

### final-exam-study-guide-trial-python-basics-2023-q01 — 1_Basics_Logic_2

Suppose you already have: (i) a list of strings called europe which contain the names of all European countries, and (ii) a string variable called destination.

You want to write a program to advice Dutch residents on the documents they need to prepare before traveling:
- If they travel within Europe, your program should print "No passport needed. Bring your ID card."
- If they travel outside of Europe, the program should print "Please bring your passport."

Which of the following code segment will achieve what you need?

- **A**
```python
if destination in europe:
    print('No passport needed. Bring your ID card.')
else:
    print('Please bring your passport.')
```

- **B**
```python
if destination in europe:
    return 'No passport needed. Bring your ID card.'
elif destination not in europe:
    return 'Please bring your passport.'
```

- **C**
```python
for country in europe:
    if destination = country:
        print('No passport needed. Bring your ID card.')
    else:
        print('Please bring your passport.')
```

- **D**
```python
for country in europe:
    if destination != country:
        return 'Please bring your passport.'
    else:
        return 'No passport needed. Bring your ID card.'
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q02 — 1_Basics_Scope_3

Calling the function func_10 will produce an error. Which line of the following code segment produces the error?

- **A**
```python
'var_2 = var_1 * var'
This line produces the error because func_2() was not called and assigning the value to var_1, thus var_1 was referenced before being defined.
```

- **B**
```python
'var_1 = var * 2'
This line produces the error because Python is confused about which value var should have.
```

- **C**
```python
'def func_2(var):'
This line produces the error because the name var is already used for the argument of func_1() and cannot be used again as the name of the argument for func_2().
```

- **D**
```python
'return var_2'
This line produces the error because one function cannot return two outputs.
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q03 — 1_Basics_Variables_1

What is the output of the following code segment?

- **A** `[str, int, NoneType, bool, float, str, dict]`

- **B** `[str, int, NoneType, bool, float, bool, dict]`

- **C** `[str, int, NoneType, bool, float, str, list]`

- **D** `[str, float, NoneType, bool, int, str, dict]`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q04 — 2-dictionaries - comprehension - 1

You have to create a dictionary called vowels_ASCII where the keys are the lowercase vowels (a, e, i, o, u) and the values are their corresponding ASCII values.

The ASCII (American Standard Code for Information Interchange) is a character encoding standard that assigns unique numerical values to characters.

That is, if we execute the following command:
print(vowels_ASCII)

the output should be:
{'a': 97, 'e': 101, 'i': 105, 'o': 111, 'u': 117}

Which of the code segments work(s) as intended?

Hint: the ord() function returns a unique numerical value to a character. The function takes a unit-length text as an argument and returns the assigned unique numerical value.

For example:
ord('a')

returns:
97

- **A** `vowels_ASCII = {vowel: ord(vowel) for vowel in 'aeiou'}`

- **B** `vowels_ASCII = {vowel: ord(vowel) for vowel in 'aeiou' if vowel in 'aeiou'}`

- **C** `Both of the code segments work correctly.`

- **D** `Neither of the code segments work correctly.`

Correct: **C**

---

### final-exam-study-guide-trial-python-basics-2023-q05 — 2-dictionaries - manipulation - 1

Suppose you have three variables called player1_goals, player2_goals, and player3_goals. Each of the variables contains a list of integers that represents the number of goals scored by the football players in five different matches:

player1_goals = [2, 1, 3, 2, 1]
player2_goals = [0, 1, 1, 3, 2]
player3_goals = [1, 0, 2, 1, 3]

You want to create a dictionary called match_goals where the keys are the match numbers (starting from 1) and the values are a tuple containing the total goals scored by each player in that match.

So, if we execute the following command:
print(match_goals)

the output should be:
{1: (2, 0, 1), 2: (1, 1, 0), 3: (3, 1, 2), 4: (2, 3, 1), 5: (1, 2, 3)}

Which of the following code segments works as intended?

- **A**
```python
match_goals = {}
for i, (goals1, goals2, goals3) in enumerate(zip(player1_goals, player2_goals, player3_goals), start=1):
    match_goals[i] = (goals1, goals2, goals3)
```

- **B**
```python
match_goals = {}
for i, (goals1, goals2, goals3) in enumerate(zip(player1_goals, player2_goals, player3_goals), start=1):
    match_goals[i] = [goals1 + goals2 + goals3]
```

- **C**
```python
match_goals = {}
for i, (goals1, goals2, goals3) in enumerate(zip(player1_goals, player2_goals, player3_goals)):
    match_goals[i] = [goals1, goals2, goals3]
```

- **D**
```python
match_goals = {}
for i, (goals1, goals2, goals3) in enumerate(zip(player1_goals, player2_goals, player3_goals)):
    match_goals[i] = (goals1, goals2, goals3)
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q06 — 2-dictionaries - slicing - 1

You have the following dictionary that represents the monthly sales of a store:
monthly_sales = {'January': 1500, 'February': 2200, 'March': 1800, 'April': 2400, 'May': 2000, 'June': 2800}

You need to calculate the average sales for the first three months (January, February, and March). Which of the following code segments works as intended?

- **A**
```python
sales_subset = [monthly_sales[key] for key in list(monthly_sales.keys())[:3]]
average_sales = sum(sales_subset) / len(sales_subset)
print(average_sales)
```

- **B**
```python
sales_subset = monthly_sales[:3]
average_sales = sum(sales_subset) / len(sales_subset)
print(average_sales)
```

- **C**
```python
sales_subset = list(monthly_sales.items())[:3]
average_sales = sum(sales_subset) / len(sales_subset)
print(average_sales)
```

- **D**
```python
sales_subset = monthly_sales['January':'March']
average_sales = sum(sales_subset.values()) / len(sales_subset)
print(average_sales)
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q07 — 2-list - comprehension - 2

What is the output of the following code segment?

- **A** `[1, 4, 3, 8, 5]`

- **B** `[2, 4, 6, 8, 10]`

- **C** `[1, 2, 3, 4, 5]`

- **D** `[2, 2, 6, 4, 10]`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q08 — 2-list - manipulation - 2

What is the output of the following code segment?

- **A** `['10a', '30c']`

- **B** `[10, 20, 30, 40]`

- **C** `['a', 'b', 'c', 'd']`

- **D** `['10a', '20b', '30c', '40d']`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q09 — 2-list - slicing - 2

Suppose you have a list called mylist. You want to extract every third element starting from index 1 (inclusive) to the last index (inclusive) from that list using the following line of code:
subset = mylist[___:___:___]

For example, if you have:
mylist = [10, 15, 20, 25, 30, 35, 40, 45]

then executing the following command:
print(subset)

should return:
[15, 30, 45]

What should the blanks be filled with?

- **A** `1:len(mylist):3`

- **B** `0:len(mylist):3`

- **C** `1:len(mylist)-1:3`

- **D** `0:len(mylist)-1:3`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q10 — 3_Function_Argument_1

Suppose you have the following function:

What will be printed by the following line of code?
print(main())

- **A** `True`

- **B** `False`

- **C** `0`

- **D** `None`

Correct: **D**

---

### final-exam-study-guide-trial-python-basics-2023-q11 — 3_Function_Built-in_3

Suppose you have a variable called x which contains a list of integers as follows:
x = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

Which of the following lines will produce an output that is different from the rest?

- **A** `print(len(x))`

- **B** `print(sorted(x, reverse=True)[0])`

- **C** `print(x.index(9))`

- **D** `print(sum(x[4:6]))`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q12 — 3_Function_Flexible-Argument_1

You want to write a function called main which accepts a flexible number of integers as arguments.

The function should return a dictionary with the following key-value pairs:
- key 'sum' has a value which is the sum of all the integers passed as arguments
- key 'pro' has a value which is the multiplicative product of all the integers passed as arguments
- key 'pow' has a value which is a list of all the squares of the integers passed as arguments

Which of the following lines of code will complete the function to give what you need?

- **A**
```python
x['sum'] = sum(args)
x['pro'] = 1
x['pow'] = []
for i in args:
    x['pro'] *= i
    x['pow'].append(i**2)
```

- **B**
```python
x['sum'] = sum(args)
x['pro'] = i for i in args
x['pow'] = [i**2 for i in args]
```

- **C**
```python
for i in args:
    x['sum'] = sum(args)
    x['pro'] *= i
    x['pow'] = [i**2 for i in args]
```

- **D** `None of the given options.`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q13 — 6-string - fstring - 2

You have the following objects loaded in Python:
item = "laptop"
price = 1299.99

You need to print the following sentence:
The laptop is priced at $1299.99.

Which of the following lines of code works as intended?

- **A**
```python
message = "The {0} is priced at ${1}.".format(item, price)
print(message)
```

- **B**
```python
message = "The {0} is priced at ${1}.".format(item, price)
print(mesage)
```

- **C**
```python
message = "The {item} costs ${price}.".format(price, item)
print(message)
```

- **D**
```python
message = "The {item} costs ${price}.".format(price, item)
print(message)
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q14 — 7-pandas - easy - 1

Suppose you have run the following block of code:

import pandas as pd
data = {'A': [1, 2, 3],
        'B': [4, 5, 6],
        'C': [7, 8, 9]}
df = pd.DataFrame(data)

Which of the following lines of code give(s) the following output?
1    4
2    5
3    6
Name: B, dtype: int64

- **A** `df.loc[:, 'B']`

- **B** `df['B'].loc[:]`

- **C** `df['B']`

- **D** `All of the given lines.`

Correct: **D**

---

### final-exam-study-guide-trial-python-basics-2023-q15 — 8_Datetime_Easy_1

Which code segment gives the same output as the following?

date = datetime.strptime("05.12.2023", "%m.%d.%Y")
print((date + timedelta(days=-10)).strftime("%d-%m-%Y"))

You may assume that datetime and timedelta classess are already imported from the datetime module.

- **A** `print(datetime.strptime('22-05-2023', '%d.%m.%Y'))`

- **B** `print('02-05-2023')`

- **C** `print(datetime.strptime('05.22.2023', '%d-%m-%Y'))`

- **D**
```python
date = datetime.strptime('10/05/2023', '%d/%m/%Y')
print((date + timedelta(days=5)).strftime('%m-%d-%Y'))
```

Correct: **B**

---

### final-exam-study-guide-trial-python-basics-2023-q16 — 9_OOP_Easy_3

You have the following definition for a class called Shape:

What would be the output if we execute the following commands?

print(Shape(5, 3).area == Shape(1, 15).length)

- **A** `True`

- **B** `False`

- **C** `An error`

- **D** `None of the given options.`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q17 — 6-string - operations - 2

Write a function called shuffle_sentence that takes a string as an argument and returns a new string where the words are shuffled randomly.

For example, if your function is called as:
shuffle_sentence("Hello, how are you today?")
then it could return a shuffled string like:
'how today? you Hello, are'

Which of the following programs work(s) according to the requirements?

Hints:
The shuffle() function is a method from the random module. The shuffle() method takes a sequence, like a list, and reorganizes the order of the items. This method changes the original list; it does not return a new list.
The reversed() function computes the reverse of a given sequence object and returns it in the form of a list.

- **A**
```python
def shuffle_sentence(sentence):
    words = sentence.split()
    return ' '.join(reversed(words))
```

- **B**
```python
import random

def shuffle_sentence(sentence):
    words = sentence.split()
    random.shuffle(words)
    return ' '.join(words)
```

- **C** `Both of the programs work.`

- **D** `Neither of the programs work.`

Correct: **B**

---

### final-exam-study-guide-trial-python-basics-2023-q18 — 6-strings - find & replace - 1

Consider the following line of code:

text = "The demand for oil has been increasing. Natural gas is a crucial commodity in many industries. The price of oil has also been rising."

You want to create a new string called new_text where all occurances of "oil" are replaced by "natural gas".

So:
print(new_text)
should return:
"The demand for natural gas has been increasing. Natural gas is a crucial commodity in many industries. The price of natural gas has also been rising."

Which of the following code segments achieve(s) what you want?

- **A** `new_text = ' '.join([word if word != 'oil' else 'natural gas' for word in text.split()])`

- **B** `new_text = text.replace("oil", "natural gas")`

- **C**
```python
new_text = text.split()
for index, word in enumerate(new_text):
    if word == 'oil':
        new_text[index] = 'natural gas'
new_text = ' '.join(new_text)
```

- **D** `All of the given options works as intended.`

Correct: **D**

---

### final-exam-study-guide-trial-python-basics-2023-q19 — 7-pandas - hard - 1

Consider the following pandas DataFrame called df:

   Name  Age  Gender  Salary
0  John   25    Male   50000
1  Jane   30  Female   65000
2  Alex   35    Male   80000
3  Lisa   40  Female   70000
4  Mark   28    Male   55000

You need to perform a series of operations on this DataFrame.
- Operation 1: Select all rows where the age is greater than 30 and the gender is "Male".
- Operation 2: Create a new column called Sex_abbr of which the values should be "F" if gender is "Female" and "M" if gender is "Male".
- Operation 3: Calculate the average salary of all employees.

Which of the following blocks of code performs these operations as intended?

- **A**
```python
df_operation1 = df[(df['Age'] > 30) & (df['Gender'] == 'Male')]
df['Sex_abbr'] = ['M' if x == 'Male' else 'F' for x in df['Gender']]
df_operation3 = df['Salary'].mean()
```

- **B**
```python
df_operation1 = df.loc(df['Age'] > 30) & df.loc(df['Gender'] == 'Male')
df['Sex_abbr'] = ['M' if x == 'Male' else 'F' for x in df['Gender']]
df_operation3 = df['Salary'].mean()
```

- **C**
```python
df_operation1 = df.loc(df['Age'] > 30) & df.loc(df['Gender'] == 'Male')
df['Sex_abbr'] = df['Gender'].map(lambda x: 'M' if x == 'Male' else 'F')
df_operation3 = df['Salary'].sum()/len(df)
```

- **D**
```python
df_operation1 = df[df['Age'] > 30 & df['Gender'] == 'Male']
df['Sex_abbr'].map(lambda x: 'M' if x == 'Male' else 'F' for x in df['Gender'])
df_operation3 = df['Salary'].sum()/len(df)
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q20 — 7-pandas - lambda - 1

Consider the following pandas DataFrame called df:

   Name  Performance_review  Salary
0  John                    2   50000
1  Jane                    4   65000
2  Alex                    3   80000
3  Lisa                    2   70000
4  Mark                    1   55000

You want to create a new column called Bonus that compute each employee's bonus based on their salary and performance review using the following formula:
- if the performance review is less than 4, the bonus is 0.
- if the performance review is 4 or 5, the bonus is 5% of the salary.

Which of the following code snippets works as intended?

- **A** `df['Bonus'] = df.apply(lambda row: row['Salary']*0.05 if row['Performance_review']>=4 else 0, axis=1)`

- **B** `df['Bonus'] = df['Salary'].apply(lambda x: x*0.05 if df['Performance_review']>=4 else 0)`

- **C** `df['Bonus'] = map(df['Salary'].apply(lambda x: x*0.05 if df['Performance_review']>4 else 0))`

- **D** `df['Bonus'] = df['Salary'].map(lambda row: row*0.05 if df['Performance_review']>=4 else 0)`

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q21 — 8_Datetime_Function_3

You want to create a function called main which take an integer and a flexible number of strings as arguments. The strings represent dates in the format of DD MM YYYY. The day, month and year can be separated by different characters.

Your function should look for the string inputs which represent dates as DD-MM-YYYY or DD/MM/YYYY and return those strings in the format of DD.MM.YYYY in a list. Furthermore, the dates represented by the strings should be shifted by the amount of days as given by the integer argument.

For example, if we call your function as:
main(3, '25/06/2003', '26.06.2003', '27-06-2003', '28:06:2023', '29-06-2023', '30.06.2023')

the output should be:
['28.06.2003', '30.06.2003', '02.07.2023']

Take a look at the following code segment. Does it do what is intended? If not, then why not?

- **A** `The code segment works as intended.`

- **B** `This code segment does not work because the function will return a list of datetime objects, not a list of strings representing dates.`

- **C** `This code segment does not work because the strftime() method cannot be applied to NoneType object.`

- **D** `This code segment produces an error because you cannot concatenate strings and timedelta.`

Correct: **B**

---

### final-exam-study-guide-trial-python-basics-2023-q22 — 8_Datetime_Hard_2

You want to define a class called Calendar, which has four attributes that are initialized at the time of object construction:
1. The 'event' attribute can be any string,
2. The 'date' attribute is a string representing a date as 'DD-MM-YYYY',
3. The 'start' attribute is a string representing the time as 'HH:MM', and
4. The 'length' attribute is an integer representing the amount of minutes.

The class should also have a method called get_details() that gives a description of Calendar objects.

For example, if we execute the following commands;
event1 = Calendar('Coffee meeting', '01-06-2023', '9:30', 20)
print(event1.get_details())

the output should be:
Coffee meeting: 01-06-2023, 9:30-9:50.

Which of the following code segments gives you what you want?

- **A**
```python
class Calendar():
    def __init__(self, event, date, start, length):
        self.event = event
        self.date = datetime.strptime(date, '%d-%m-%Y')
        self.start = datetime(self.date.year, self.date.month, self.date.day, int(start.split(':')[0]), int(start.split(':')[1]))
        self.end = self.start + timedelta(minutes=length)
    def get_details(self):
        return f'{self.event}: {self.date.strftime("%d-%m-%Y")}, {self.start.hour}:{self.start.minute}-{self.end.hour}:{self.end.minute}.'
```

- **B**
```python
class Calendar():
    def __init__(self, event, date, start, length):
        self.event = event
        self.date = date
        self.start = datetime(self.date, hour=start.split(':')[0], minute=start.split(':')[1])
        self.length = timedelta(minutes=length)
        self.end = self.start + self.length
    def get_details(self):
        return f'{self.event}: {self.date}, {self.start.hour}:{self.start.minute}-{self.end.hour}:{self.end.minute}.'
```

- **C**
```python
class Calendar():
    def __init__(self, event, date, start, length):
        self.event = event
        self.date = date
        self.start = datetime(self.date, hour=start.hour, minute=start.minute)
        self.end = self.self.start + timedelta(minutes=length)
    def get_details(self):
        return f'{self.event}: {self.date}, {self.start.hour}:{self.start.minute}-{self.end.hour}:{self.end.minute}.'
```

- **D**
```python
class Calendar():
    def __init__(self, event, date, start, length):
        self.event = event
        self.date = datetime.strptime(date, '%d-%m-%Y')
        self.start.hour = start.hour
        self.start.minute = start.minute
        self.end = self.start + timedelta(minutes=length)
    def get_details(self):
        return f'{self.event}: {self.date.strftime("%d-%m-%Y")}, {self.start.hour}:{self.start.minute}-{self.end.hour}:{self.end.minute}.'
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q23 — 9_OOP_Function_2

You have the following definition for a class called Employee:

class Employee:
    def __init__(self, name, role, salary):
        self.name = name
        self.role = role
        self.salary = salary
    # ...

You want to add three methods to this class:
1. The holiday_bonus() method which computes and returns the holiday bonus, which is 8.0% of the yearly salary,
2. The year_end_bonus() method which computes and returns the year end bonus, which is 8.3% of the yearly salary
3. The payment_overview() method which returns a payment overview of the employee using the following format:
[Name] receives $[salary] monthly, $[holiday bonus] in May and $[year end bonus] in December.

For example, if we execute the following commands:
employee1 = Employee('John Smith', 'HR representative', 2500)
print(employee1.holiday_bonus())
print(employee1.year_end_bonus())
print(employee1.payment_overview())

the output should be:
2400.0
2490.0
John Smith receives $2500 monthly, $2400.0 in May and $2490.0 in December.

Which of the following code segments should you place on the blank in the class definition to achieve what you want?

- **A**
```python
def holiday_bonus(self):
    return self.salary * 12 * 0.080
def year_end_bonus(self):
    return self.salary * 12 * 0.083
def payment_overview(self):
    return f'{self.name} receives ${self.salary} monthly, ${self.holiday_bonus()} in May and ${self.year_end_bonus()} in December.'
```

- **B**
```python
def payment_overview(self):
    return f'{self.name} receives ${self.salary} monthly, ${self.salary*12*0.08} in May and ${self.salary*12*0.083} in December.'
```

- **C**
```python
def holiday_bonus():
    self.holiday_bonus = self.salary * 12 * 0.080
def year_end_bonus():
    self.year_end_bonus = self.salary * 12 * 0.083
def payment_overview(self):
    return f'{self.name} receives ${self.salary} monthly, ${self.holiday_bonus} in May and ${self.year_end_bonus} in December.'
```

- **D**
```python
def payment_overview(self):
    self.holiday_bonus = self.salary * 12 * 0.080
    self.year_end_bonus = self.salary * 12 * 0.083
    return f'{self.name} receives ${self.salary} monthly, ${self.holiday_bonus} in May and ${self.year_end_bonus} in December.'
```

Correct: **A**

---

### final-exam-study-guide-trial-python-basics-2023-q24 — 9_OOP_Hard_2

You have the following definitions for a class called Car:

class Car:
    def __init__(self, brand, model):
        self.brand = brand
        self.model = model

    def get_description(self):
        return f"{self.brand}, {self.model}"

You want to create another class called Garage, which has two attributes that are initialized during object construction:
- The 'capacity' attribute, which is an integer and must be passed to the object constructor.
- The 'cars' attribute, which is an empty list.

The Garage class should also have two methods:
1. The add_car() method, which adds Car objects to a Garage object. New Car objects can only be added if there is still capacity in the Garage object. If not, the method should return "Capacity reached."
2. The check_garage() method, which reports the Car objects that have been added to the Garage object. The method should return a dictionary in which the keys are the counts of Car objects starting from 1 and the values are the Car objects' descriptions.

For example, if we execute the following commands:
my_garage = Garage(2)
my_garage.add_car(Car("Toyota", "Camry"))
my_garage.add_car(Car("Honda", "Accord"))
print(my_garage.check_garage())

the output should be:
{1: 'Toyota, Camry', 2: 'Honda, Accord'}

Which of the following code segments achieve(s) what you want?

- **A**
```python
class Garage:
    def __init__(self, capacity, cars = []):
        self.capacity = capacity

    def add_car(self, car):
        self.cars += car if len(self.cars) < self.capacity else return 'Capacity reached.'

    def check_garage(self, car):
        return {index: car.get_description() for index, car in enumerate(self.cars, start=1)}
```

- **B**
```python
class Garage:
    def __init__(self, capacity):
        self.capacity = capacity
        self.cars = []

    def add_car(self, car):
        if len(self.cars) < self.capacity:
            self.cars.append(car)
        else:
            return 'Capacity reached.'

    def check_garage(self):
        output = {}
        for index, car in enumerate(self.cars, start=1):
            output[index] = car.get_description()
        return output
```

- **C** `Both of the above will work.`

- **D** `None of the above will work.`

Correct: **B**

---


## 2024 Trial Final (`introduction-to-python-trial-final-exam-solutions-py22`)

### introduction-to-python-trial-final-exam-solutions-py22-q01 — 1_Basics_Logic_3

Suppose you have a variable called x which contains an integer between 0 and 10 (both are inclusive).

Which of the following programs will tell you whether x contains an odd or even number?

- **A**
```python
if x in list(range(11))[::2]:
    print('Even number')
else:
    print('Odd number')
```

- **B**
```python
if x % 2 != 0:
    print('Odd number')
else:
    print('Even number')
```

- **C**
```python
if x in [1, 3, 5, 7, 9]:
    print('Odd number')
else:
    print('Even number')
```

- **D** `All of the programs work as intended.`

Correct: **D**

---

### introduction-to-python-trial-final-exam-solutions-py22-q02 — 1_Basics_Scope_2

Take a look at the following code segment. Will executing this code segment produce an error? If yes, then why?

- **A** `This code will produce an error because a is a global name that is referenced inside the local scope of inner().`

- **B** `This code will not produce any error and will return 30.`

- **C** `This code will produce an error because c is not defined before referencing.`

- **D** `This code will not produce any error and will return 50.`

Correct: **B**

---

### introduction-to-python-trial-final-exam-solutions-py22-q03 — 1_Basics_Variables_2

What will be returned by the following code segment?

- **A** `[0, None, 2, 3, None, 5, 6, 7, 8, None]`

- **B** `[0, 1.0, 2, 3, 3.50, 5, 6, 7, 8, 9]`

- **C** `[None, 1.0, None, None, 3.5, None, None, None, None, '9']`

- **D** `[0, None, 2, 3, None, 5, 6, 7, 8, 9]`

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q04 — 2-dictionaries - comprehension - 2

You have to create a dictionary called roman_nums where the keys are the integers from 1 to 5 (both are inclusive) and the values are their corresponding Roman numeral symbols.

That is, if we execute the following command:
print(roman_nums)
the output should be:
{1: 'I', 2: 'II', 3: 'III', 4: 'IV', 5: 'V'}

Which of the following code segments works as intended?

- **A** `roman_nums = {num: roman for num, roman in zip(range(1, 6), ['I', 'II', 'III', 'IV', 'V'])}`

- **B** `roman_nums = {roman: num for roman, num in zip(['I', 'II', 'III', 'IV', 'V'], range(1, 6))}`

- **C** `roman_nums = {num: ['I', 'II', 'III', 'IV', 'V'][num] for num in range(1, 6)}`

- **D** `roman_nums = {num: roman for num, roman in zip(range(1, 6), 'I II III IV V')}`

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q05 — 2-dictionaries - manipulation - 2

You have two lists representing the names and ages of individuals:
names = ['Alice', 'Bob', 'Charlie', 'David']
ages = [25, 30, 35, 40]

You need to create a dictionary called person_dict where the keys are the names and the values are the ages.
However, you want to only include the names that start with the letter 'A' or with the letter 'C'.

So executing the following command:
print(person_dict)
should give the following output:
{'Alice': 25, 'Charlie': 35}

Which of the following code segments works as intended?

- **A**
```python
person_dict = {}
for name, age in zip(names, ages):
    if name[0] == 'A' or name[0] == 'C':
        person_dict[name] = age
```

- **B**
```python
person_dict = {}
for i, name in enumerate(names):
    if name[0] == 'A' or name[0] == 'C':
        person_dict[i] = ages[i]
```

- **C**
```python
person_dict = {}
for name, age in zip(names, ages):
    if name[0] == 'A' or name[0] == 'C':
        person_dict.append(name:age)
```

- **D**
```python
person_dict = {}
for i, name in enumerate(names):
    for j, letter in enumerate(name):
        if letter == 'A' or letter == 'C':
            person_dict[i] = ages[j]
```

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q06 — 2-dictionaries - slicing - 2

You have the following dictionary that represents the performance ratings of employees in a company:
employee_ratings = {'John': 8, 'Sarah': 9, 'Michael': 7, 'Emma': 9, 'David': 6}

You need to find and print the name of the employee(s) with the highest performance rating.

Which of the following code segments works as intended?

- **A**
```python
max_rating = max(employee_ratings.values())
for employee, rating in employee_ratings.items():
    if rating == max_rating:
        print(employee)
```

- **B**
```python
max_rating_employee = max(employee_ratings.keys())
for employee, rating in employee_ratings.items():
    if employee == max_rating_employee:
        print(employee)
```

- **C** `Both of the given options are correct.`

- **D** `None of the given options are correct.`

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q07 — 2-list - comprehension - 1

What is the output of the following code segment?

- **A** `[2, 4]`

- **B** `[3, 4, 5]`

- **C** `[4]`

- **D** `[]`

Correct: **C**

---

### introduction-to-python-trial-final-exam-solutions-py22-q08 — 2-list - manipulation - 1

What is the output of the following code segment?

- **A** `['a', 'bb', 'ccc']`

- **B** `[1, 2, 3]`

- **C** `[1, 'b', 3]`

- **D** `['aa', 'bb', 'cc']`

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q09 — 2-list - slicing - 1

Suppose you have a list called mylist. You want to extract every fourth element starting from index 2 (inclusive) to the second-to-last index (inclusive) of that list using the following line of code:
subset = mylist[___:___:___]

For example, if you have:
mylist = [10, 15, 20, 25, 30, 35, 40, 45, 50]

then executing the following command:
print(subset)

should print:
[20, 35]

What should the blanks be filled with?

- **A** `2:-1:3`

- **B** `2:len(mylist)-1:3`

- **C** `Both of the given options are correct.`

- **D** `None of the given options are correct.`

Correct: **C**

---

### introduction-to-python-trial-final-exam-solutions-py22-q10 — 3_Function_Argument_2

Suppose you have the following function, which takes a list of integers as an argument:

What will be returned, if we call the function as follows:
main([0, 1, 2, 23, 24, 25])

- **A** `'abcxyz'`

- **B** `['a', 'b', 'c', 'x', 'y', 'z']`

- **C** `'012232425'`

- **D** `None of the given options.`

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q11 — 3_Function_Built-in_1

Suppose you have a variable called x which contains a string as follows:

x = 'Hello world'

Which of the following lines of code produce(s) 2 as an output?

- **A** `print(x.count('o'))`

- **B** `print(x.split(' ')[0].count('ll'))`

- **C** `print(len(x)//5)`

- **D** `All of the given options.`

Correct: **D**

---

### introduction-to-python-trial-final-exam-solutions-py22-q12 — 3_Function_Flexible-Argument_2

You need to write a function called main which accepts a list of integers as an argument. The function should return a tuple of two integers, in which the first is the sum of the squares of all even numbers, and the second is the sum of the squares of all odd numbers.

For example, calling the function as:
main(1, 2, 3, 4)
should return:
(20, 10)

Which of the following blocks of code fits with the rest of the program and will you give the intended output?

- **A**
```python
for i in args:
    if i % 2 == 0:
        total_even += i**2
    else:
        total_odd += i**2

return (total_even, total_odd)
```

- **B**
```python
for i in args:
    if i % 2 == 1:
        total_even += i
    else:
        total_odd += i

return (total_even**2, total_odd**2)
```

- **C**
```python
for i in args:
    if i % 2 == 0:
        total_even.append(i**2)
    else:
        total_odd.append(i**2)

return (sum(total_even), sum(total_odd))
```

- **D** `All of the given code blocks work as intended.`

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q13 — 6-string - fstring - 1

You have the following objects loaded in Python:
name = "Alice"
age = 25
country = "the USA"

You need to print the following string:
My name is Alice. I am 25 years old, and I am from the USA.

Which of the following lines of code works as intended?

- **A**
```python
message = "My name is {0}. I am {2} years old, and I am from {1}.".format(name, country, age)
print(message)
```

- **B**
```python
message = f"My name is {name}. I am {age} years old, and I am from {country}."
print(message)
```

- **C**
```python
message = 'My name is ' + name + '. I am ' + str(age) + ' years old, and I am from ' + str(country) + '.'
print(message)
```

- **D** `All of the given options are correct.`

Correct: **D**

---

### introduction-to-python-trial-final-exam-solutions-py22-q14 — 7-pandas - easy - 2

Suppose you have the following DataFrame called df, and assume that pandas is already imported:

  Player  Goals  Assists
0 John        5        2
1 Jane        3        6
2 Alex        2        4

All of the following lines of code make the same selection, but one of the results has a different datatype. Which one?

- **A** `df.loc[:, 'Goals']`

- **B** `df['Goals']`

- **C** `df.loc[[0, 1, 2], 'Goals']`

- **D** `df.loc[:, ['Goals']]`

Correct: **D**

---

### introduction-to-python-trial-final-exam-solutions-py22-q15 — 8_Datetime_Easy_3

Which code segment gives the same output as the following:

date1 = datetime(2023, 6, 1).strftime('%d-%m-%Y')
date2 = datetime(2023, 5, 1).strftime('%d-%m-%Y')
print((datetime.strptime(date1, '%d-%m-%Y') - datetime.strptime(date2, '%d-%m-%Y')).days)

You may assume that the datetime and timedelta classes are already imported from the datetime module.

- **A** `print((datetime(2023, 5, 1) - datetime(2023, 6, 1)).days)`

- **B** `print((datetime(2023, 6, 1) - datetime(2023, 1, 5)).days)`

- **C** `print((datetime.strptime('2023-6-1', '%Y-%d-%m') - datetime.strptime('2023-5-1', '%Y-%d-%m')).days)`

- **D** `print((datetime.strptime('2023-06-01', '%Y-%m-%d') - datetime.strptime('2023-05-01', '%Y-%m-%d')).days)`

Correct: **D**

---

### introduction-to-python-trial-final-exam-solutions-py22-q16 — 9_OOP_Easy_2

You have the following definition of a class called Flight. What would be the output if we execute the following statements?

- **A**
```python
'long'
'cheap'
```

- **B**
```python
'short'
'expensive'
```

- **C**
```python
'long'
'expensive'
```

- **D**
```python
'short'
'cheap'
```

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q17 — 6-string - operations - 1

Consider the following code snippet. Which operation in the code snippet contains an error?

- **A** `Operation 1`

- **B** `Operation 2`

- **C** `Operation 3`

- **D** `None of the operations contains an error.`

Correct: **B**

---

### introduction-to-python-trial-final-exam-solutions-py22-q18 — 6-strings - find - 2

Suppose you have the following variables called sentence1 and sentence2 which contain strings. The sentences contain names, but they are not properly capitalized. You want to create a new string object called paragraph, with the proper nouns capitalized in the two sentences and the two sentences connected into one big string.

That is, if we execute the following line of code:
print(paragraph)
the output should be:
"Harry, Ron, and Hermione walked through the halls of Hogwarts; their footsteps echoing off the stone walls.
The Marauder's map in Harry's hands revealed the secret passageways and hidden rooms of the castle."

Which of the following code segments achieves what you want?

- **A**
```python
names = ['harry', 'ron', 'hermione', 'hogwarts', 'marauder']
for name in names:
    sentence1[sentence1.find(name)] = name.capitalize()
    sentence2[sentence2.find(name)] = name.capitalize()
paragraph = sentence1 + " " + sentence2
```

- **B**
```python
names = ['harry', 'ron', 'hermione', 'hogwarts', 'marauder']
for word, name in zip(sentence1, names):
    if word == name:
        sentence1 = sentence1.replace(word, name.capitalize())
for word, name in zip(sentence2, names):
    if word == name:
        sentence2 = sentence2.replace(word, name.capitalize())
paragraph = sentence1 + " " + sentence2
```

- **C**
```python
names = ['harry', 'ron', 'hermione', 'hogwarts', 'marauder']
new1 = ' '.join([word.capitalize() if word in names else word for word in sentence1])
new2 = ' '.join([word.capitalize() if word in names else word for word in sentence2])
paragraph = new1 + " " + new2
```

- **D**
```python
for word in ['harry', 'ron', 'hermione', 'hogwarts', 'marauder']:
    sentence1 = sentence1.replace(word, word.capitalize())
    sentence2 = sentence2.replace(word, word.capitalize())
paragraph = sentence1 + " " + sentence2
```

Correct: **D**

---

### introduction-to-python-trial-final-exam-solutions-py22-q19 — 7-pandas - hard - 2

Consider the following pandas DataFrame called df, and assume that Pandas is already imported.

You need to perform a series of operations on this DataFrame:
- Operation 1: Create a new column called Name_Length that contains the length of each person's name
- Operation 2: Replace all occurrences of the occupation 'Engineer' with 'Software Developer'
- Operation 3: Extract the last two characters of each person's name and store them in a new column called Name_Suffix

Which of the following blocks of code performs these operations as intended?

- **A**
```python
df['Name_Length'] = df['Name'].map(lambda x: len(x))
df['Occupation'] = ['Software Developer' if x == 'Engineer' else x for x in df['Occupation']]
df['Name_Suffix'] = df['Name'].map(lambda x: x[-2:])
```

- **B**
```python
df['Name_Length'] = len(df['Name'])
df['Occupation'] = ['Software Developer' if x == 'Engineer' else x for x in df['Occupation']]
df['Name_Suffix'] = df['Name'].lambda x: x[-2:]
```

- **C**
```python
df['Name_Length'] = len(df['Name'])
df['Occupation'].map(lambda x: 'Software Developer' if x == 'Engineer' else x)
df['Name_Suffix'] = df['Name'].map(lambda x: x[:-2])
```

- **D**
```python
df['Name_Length'] = df['Name'].map(len)
df['Occupation'] = df['Occupation'].map(lambda x: 'Software Developer' if x == 'Engineer' else x)
df['Name_Suffix'] = df['Name'].map(lambda x: x[-2:-1])
```

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q20 — 7-pandas - lambda - 2

What will be printed by the following code?

- **A**
```python
Product  Units  Price
2       C    200     15
0       A    100     10
3       D     72     13
1       B     45     19
```

- **B**
```python
Product  Units  Price
1       B     50     19
0       A    100     10
3       D     80     13
2       C    200     15
```

- **C**
```python
Product  Units  Price
2       C    200     15
0       A    100     10
3       D     80     13
1       B     50     19
```

- **D**
```python
Product  Units  Price
2       C    200     15
3       D     80     13
0       A    100     10
1       B     50     19
```

Correct: **C**

---

### introduction-to-python-trial-final-exam-solutions-py22-q21 — 8_Datetime_Function_2

You have the following definition for a class called Calendar.

The method check_overlap() should return True if there are two overlapping events and False if the two events are not overlapping.

For example, if we have the following Calendar objects:
event1 = Calendar('Coffee meeting', '01-06-2023 9:30', 20)
event2 = Calendar('Writing session', '01-06-2023 10:00', 150)
event3 = Calendar('Lunch meeting', '01-06-2023 12:00', 45)

the following command should return False:
print(event1.check_overlap(event2))

and the following command returns True:
print(event2.check_overlap(event3))

Does the code segment given above do what you want? If not, then why not?

Hint:
The timedelta functions contains the following parameters: days, seconds, microseconds, milliseconds, minutes, hours, and weeks. All the parameters are optional and 0 by default. The timedelta object that is created using this function represents a duration.

- **A** `The code segment works as intended.`

- **B** `This code segment does not work because the condition provided after the return keyword is incorrect.`

- **C** `This code segment does not work because the syntax to parse the input string to create a datetime object is incorrect.`

- **D** `This code segment does not work because the __init__ method needs 4 parameters and only 3 arguments are passed.`

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q22 — 8_Datetime_Hard_1

You want to create a DataFrame called df that has the following format:

         Day  Month  Year
01-01-23    1      1  2023
08-01-23    8      1  2023
15-01-23   15      1  2023
22-01-23   22      1  2023
29-01-23   29      1  2023

Which of the following code segments achieves what you want?

You may assume that the datetime and timedelta classes are already imported from the datetime module, as well as the pandas module (via: import pandas as pd).

Hint:
The timedelta functions contains the following parameters: days, seconds, microseconds, milliseconds, minutes, hours, and weeks. All the parameters are optional and 0 by default. The timedelta object that is created using this function represents a duration.

- **A**
```python
dates = [(datetime(2023, 1, 1) + timedelta(weeks=1*i)) for i in range(5)]
data = {'Day': [date.day for date in dates],
        'Month': [date.month for date in dates],
        'Year': [date.year for date in dates]}
df = pd.DataFrame(data, index=[date.strftime('%d-%m-%y') for date in dates])
```

- **B**
```python
dates = [(datetime(2023, 1, 1) + timedelta(days=7*i)).strftime('%d-%m-%y') for i in range(5)]
data = {'Day': [date.day for date in dates],
        'Month': [date.month for date in dates],
        'Year': [date.year for date in dates]}
df = pd.DataFrame(data, index=dates)
```

- **C**
```python
day = pd.Series([(datetime(2023, 1, 1) + timedelta(weeks=1*i)).day for i in range(5)])
month = pd.Series([(datetime(2023, 1, 1) + timedelta(weeks=1*i)).month for i in range(5)])
year = pd.Series([(datetime(2023, 1, 1) + timedelta(weeks=1*i)).year for i in range(5)])
df = pd.DataFrame(data=[day, month, year])
```

- **D**
```python
df = pd.DataFrame(index=[(datetime(2023, 1, 1) + timedelta(weeks=1*i)) for i in range(5)],
                  {'Day': [date.days for date in index],
                   'Month': [date.months for date in index],
                   'Year': [date.year for date in index]})
```

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q23 — 9_OOP_Function_3

You have the following definition of a class called Pack.

You want to add to this class a method called fitting() that calculates how many times another object of the class Pack would fit inside this object.
The method should return the number of times these other objects would fit completely in this object, and the final value.
The final value is the sum of all values of all objects that fit in it, plus the value of the carrying object self.

For example, if we execute the lines of code:
backpack = Pack(size=15, value=20)
book = Pack(size=4, value=10)
backpack.fitting(book)

the output should be:
Amount: 3. Value: 50.

Which of the following code segments should you place on the missing lines in the class definition to achieve what you want?

- **A**
```python
def fitting(self, other):
    if self.size > other.size:
        self.total = (self.size // other.size) * other.value + self.value
        return f'Amount: {self.size // other.size}. Value: {self.total}.'
    else:
        return f'Amount: 0. Value: {self.value}.'
```

- **B**
```python
def fitting(self, other):
    if self.size > other.size:
        return f'Amount: {self.size // other.size}. Value: {other.value * other.size}.'
    else:
        return f'Amount: 0. Value: {self.value}.'
```

- **C**
```python
def fitting(self, other):
    self.amount = self.size / other.size
    self.total = self.amount * other.value
    return f'Amount: {self.amount}. Value: {self.total}.'
```

- **D**
```python
def fitting(self, other):
    self.amount = self.size / other.size
    self.total = self.amount * other.value
    return 'Amount: {}. Value: {}.'.format(self.amount, self.value if self.size > other.size else self.total)
```

Correct: **A**

---

### introduction-to-python-trial-final-exam-solutions-py22-q24 — 9_OOP_Hard_1

You have the following definition for a class called Piece.

And the creation of three objects with the help of the class definition:
a = Piece(diagonal=True, straight=False, initial_position=(0, 0))
b = Piece(diagonal=False, straight=True, initial_position=(4, 3))
c = Piece(diagonal=True, straight=True, initial_position=(9, 6))

If we run the following statements:
print(a.check_move((4, 4)))
print(b.check_move((5, 5)))
print(c.check_move((6, 6)))

This will print 3 Boolean values. Of these values, how many times will this be True?

- **A** `0`

- **B** `1`

- **C** `2`

- **D** `3`

Correct: **B**

---


## 2023 Resit Exam Guidelines (`resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023`)

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q01 — Multiple choice - Question-ID: 357615

Suppose you have a list called x containing tuples, where
x = [(1, 2), (3, 4), (5, 6), (7, 8)]

Which of the following lines of code will print True?

- **A** `print(x[0][1] * x[-3][0] == x[2][1])`

- **B** `print(x[1][0] + x[-2][0] == x[-1][1])`

- **C** `print(x[-1][0] - x[-2][0] == x[0][1])`

- **D** `All lines of code will print True.`

Correct: **D**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q02 — Multiple choice - Question-ID: 357607

Executing the following program will produce an error. Why?

- **A** `The function called power should not return the string 'The result of {} ** {} is: {}'.format(num, factor, result), but the value of result.`

- **B** `** is not a valid Python operator.`

- **C** `The syntax used in the return statement to format the string is incorrect.`

- **D** `Result is a local name that cannot be referenced outside of the function power.`

Correct: **D**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q03 — Multiple choice - Question-ID: 355235

What will be printed by the following code segment?

- **A** `['a', 'None', '123']`

- **B** `[[]]`

- **C** `[]`

- **D** `[None]`

Correct: **D**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q04 — function defaults and loops

Suppose you have the following function, which takes two integers as arguments:

What will be printed by the following line of code:
print(main(1))

- **A** `This code produces an error as there is a missing argument when calling main.`

- **B**
```python
['1 * 1 = 1',
 '1 * 2 = 2',
 '1 * 3 = 3',
 '1 * 4 = 4',
 '1 * 5 = 5',
 '1 * 6 = 6',
 '1 * 7 = 7',
 '1 * 8 = 8',
 '1 * 9 = 9',
 '1 * 10 = 10']
```

- **C**
```python
The code produces a syntax error because of the line:
    table.append(f'{x} * {i} = {x*i}')
```

- **D**
```python
['1 * 1 = 1',
 '1 * 2 = 2',
 '1 * 3 = 3',
 '1 * 4 = 4',
 '1 * 5 = 5',
 '1 * 6 = 6',
 '1 * 7 = 7',
 '1 * 8 = 8',
 '1 * 9 = 9',
 '1 * 10 = 10',
 '1 * 11 = 11']
```

Correct: **B**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q05 — list slicing and sets

Suppose you have a list called x, where:
x = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

Which of the following code segments will print the following list?
[5, 4, 3, 2, 1]

- **A**
```python
y = list(set(x))
print(sorted(y, reverse = True))
```

- **B** `print(x[::-2])`

- **C** `Both lines of code will print that output.`

- **D** `Neither line of code will print that output.`

Correct: **C**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q06 — keyword arguments

You need to write a function called main which accepts a flexible number of keyword arguments. The function should compute and return the sum of the values of the arguments.

For example, if you call the function as:
main(apple=1.99, banana=0.99, orange=1.49)
it should return:
4.47

Which of the following functions will return the intended value?

- **A**
```python
def main(**kwargs):
    total = 0
    for item, price in kwargs.items():
        total += item
    return total
```

- **B**
```python
def main(**kwargs):
    total = 0
    for price in kwargs.values():
        total += price
    return total
```

- **C**
```python
def main(**kwargs):
    total = 0
    for item, price in kwargs.keys():
        total += price
    return total
```

- **D** `All functions will return the intended value.`

Correct: **B**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q07 — Dictionaries and Mappings

Assume you already have a list of strings called words.

You need to create a dictionary called word_lengths, where the keys are the strings in the list words and the values are their lengths.

Which of the following code segments will work as intended?

- **A** `word_lengths = {length: word for word, length in enumerate(words)}`

- **B** `word_lengths = {len: word for word in words}`

- **C** `word_lengths = {word: len(word) for word in words}`

- **D** `word_lengths = {word: len for word, len in words}`

Correct: **C**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q08 — Dictionaries and Mappings

You are given two lists, called students and grades.

The students list contains strings representing the names of students.
The grades list contains integers representing the students' corresponding grade levels.

You need to create a dictionary called grade_counts that counts the number of students in each grade level. That is, the keys of the dictionary are the grade levels and the values are the number of students in that grade.

For example, if you have:
students = ['A', 'B', 'C', 'D', 'E', 'F']
grades = [9, 10, 9, 11, 10, 9]

then the created dictionary grade_counts should be:
{9: 3, 10: 2, 11: 1}

Which of the following code segments will work as intended?

- **A**
```python
grade_counts = {}
for grade in grades:
    if grade not in grade_counts:
        grade_counts[grade] = 0
    grade_counts[grade] += 1
```

- **B**
```python
grade_counts = {}
for student, grade in zip(students, grades):
    if grade in grade_counts:
        grade_counts[grade].append(student)
    else:
        grade_counts[grade] = [student]
```

- **C** `Both of the given options will work as intended.`

- **D** `None of the given options will work as intended.`

Correct: **A**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q09 — Dictionaries and Mappings

You have a dictionary that represents the scores of students in a math competition:
math_scores = {'John': 85, 'Sarah': 92, 'Michael': 78, 'Emma': 90, 'David': 82}

You want to find and print the names of the students who scored above the average score.

Which of the following code segments will work as intended?

- **A**
```python
average_score = sum(math_scores.values()) / len(math_scores)
for student in math_scores.keys():
    if math_scores[student] > average_score:
        print(student)
```

- **B**
```python
for student in math_scores:
    if math_scores[student] > (sum(math_scores.values()) / len(math_scores)):
        print(student)
```

- **C** `Both code segments will work as intended.`

- **D** `None of the code segments will work as intended.`

Correct: **C**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q10 — String Methods

What is the output of the following code segment?

x = 'Hello, World!'
print([char for char in x if char.islower()])

- **A** `['e', 'l', 'l', 'o', 'o', 'r', 'l', 'd']`

- **B** `['e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd', '!']`

- **C** `['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']`

- **D** `['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']`

Correct: **A**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q11 — Functions and Imports

What will be the output of the following code segment?

list1 = [5, 10, 15, 20]
list2 = [2, 4, 6, 8]
result = []

for a, b in zip(list1, list2):
    result.append(a // b)

print(result)

- **A** `[1, 2, 3, 4]`

- **B** `[2, 2, 2, 2]`

- **C** `[6, 12, 18, 24]`

- **D** `[2.5, 2.5, 2.5, 2.5]`

Correct: **B**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q12 — Sequences and Access

Suppose you have a list called numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].
Which of the following lines of code will not create a list with the name subset and the value [10, 8, 6, 4, 2]?

- **A** `subset = numbers[::-2][::-1]`

- **B** `subset = numbers[-1::-2]`

- **C** `subset = numbers[::-1][::2]`

- **D** `subset = numbers[::-2]`

Correct: **A**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q13 — Multiple choice

You have a string variable called sentence:
sentence = 'I bought a book about programming. The book has a lot of exercises. I enjoy reading a good book.'

You want to replace only the second occurrence of "book" with "novel" in the sentence and save this as new_sentence.

So:
print(new_sentence)
should print:
I bought a book about programming. The novel has a lot of exercises. I enjoy reading a good book.

Which of the following code segments will work as intended?

Hint:
The string find() method takes three arguments: value, start and end. The first argument is required and is the value to search for. The second and third argument are optional, they are indices specifying where to start and end the search, respectively.

- **A**
```python
index = sentence.find('book')
index = sentence.find('book', index + 1)
new_sentence = sentence[:index] + 'novel' + sentence[index + 4:]
```

- **B**
```python
new_sentence = sentence.replace("book", "novel", 2)
new_sentence = new_sentence.replace("novel", "book", 1)
```

- **C** `Both options will work as intended.`

- **D** `None of the given options will work as intended.`

Correct: **C**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q14 — Multiple choice

You have the following objects loaded in Python:
fruits = ["apple", "banana", "orange"]
count = 3

You want to print the following sentence:
I have 3 fruits: apple, banana, and orange.

Which of the following code fragments will achieve the desired output?

- **A**
```python
message = f"I have {count} fruits: {', '.join(fruits)}."
print(message)
```

- **B**
```python
message = f"I have {count} fruits: {fruits[0]}, {fruits[1]}, and {fruits[2]}."
print(message)
```

- **C** `Both code fragments will achieve the desired output.`

- **D** `Neither of the code fragments will achieve the desired output.`

Correct: **B**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q15 — Multiple choice

A company wants to extract the components of email addresses. An email address consists of the local part, which comes before the "@" symbol and a domain name, which comes after the "@" symbol.

You need to create a function called main() which accepts a flexible number of strings representing email addresses and returns a DataFrame. Your DataFrame should have a column called 'local' which contains the local parts and a column called 'domain' which contains the domain names of the email addresses that were passed as arguments.

For example, if you execute the following command:
print(main('example@example.com', 'student@uva.nl', 'email@address.com'))

the output should be:
  local   domain
0 example example.com
1 student uva.nl
2 email   address.com

Which of the following code segments will return this dataframe as intended?

You may assume that pandas is already imported as pd.

- **A**
```python
def main(*args):
    local = []
    domain = []
    for email in args:
        local.append(email.split("@")[0])
        domain.append(email.split("@")[1])
    return pd.DataFrame({local: domain for local, domain in zip(local, domain)})
```

- **B**
```python
def main(*args):
    data = {}
    for email in args:
        data['local'] = email.split("@")[0]
        data['domain'] = email.split("@")[1]
    return pd.DataFrame(data)
```

- **C**
```python
def main(args):
    return pd.DataFrame({
        'local': [email.split("@")[1] for email in args],
        'data': [email.split("@")[0] for email in args]})
```

- **D**
```python
def main(*args):
    data = {}
    data['local'] = pd.Series([email.split("@")[0] for email in args])
    data['domain'] = pd.Series([email.split("@")[1] for email in args])
    return pd.DataFrame(data)
```

Correct: **D**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q16 — Multiple choice

You have the following definition of a class called Employee:

class Employee:
    def __init__(self, name, role, gender = 'not specified'):
        self.name = name
        self.role = role
        self.gender = gender

What will be the output if we execute the following lines of code?

employee1 = Employee('John Smith', 'HR representative')
print(employee1.name == 'John Smith')
print(employee1.gender == 'not specified')

- **A**
```python
True
True
```

- **B**
```python
False
True
```

- **C**
```python
False
False
```

- **D**
```python
True
False
```

Correct: **A**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q17 — Multiple choice

Which other code fragment will print the same output as the following?

from datetime import datetime, timedelta
print((datetime.strptime('2023/1/10', '%Y/%m/%d') - datetime(2023, 1, 1)).days + 1)

- **A**
```python
from datetime import datetime, timedelta
print((datetime(2023, 1, 10) - datetime(2023, 1, 1)).days)
```

- **B**
```python
from datetime import datetime, timedelta
print(timedelta(datetime(2023, 1, 10) - datetime(2023, 1, 1)).days + 1)
```

- **C**
```python
from datetime import datetime, timedelta
print((datetime(2023, 1, 10) - datetime.strptime('2023-1-1', '%Y-%m-%d')).days)
```

- **D**
```python
from datetime import datetime, timedelta
print((datetime(2023, 1, 11) - datetime(2023, 1, 1)).days)
```

Correct: **D**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q18 — Multiple choice

Suppose you have the following DataFrame called df:
  Player  Age  Height
0 John     25     180
1 Jane     30     165
2 Alex     27     175

You may assume that pandas is already imported as pd.

Which of the following lines of code will give an error?

- **A** `print(df[['Player', 'Age']])`

- **B** `print(df.loc[df['Height'] > 170, ['Player', 'Age']])`

- **C** `print(df.loc[:, 'Age'])`

- **D** `print(df[1, 'Age'])`

Correct: **D**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q19 — animals methods

You have the following definition for a class called Animals:

You need to add two methods to the class:
1. The walk() method, which returns the 'sound' attribute an Animal object has if the Animal object has 'legs'. If the Animal object does not, return 'Cannot walk!'.
2. The swim() method, which returns the 'sound' attribute an Animal object has if the Animal object has 'fin'. If the Animal object does not, return 'Cannot swim!'.

For example, if we execute the following commands:
cat = Animals('kitty', legs=True, sound='Meow!')
fish = Animals('nemo', fin=True, sound='Blob!')
print(cat.walk())
print(cat.swim())
print(fish.swim())
print(fish.walk())

the output should be:
Meow!
Cannot swim!
Blob!
Cannot walk!

Which of the following code segments should you place on the missing lines in the class definition to achieve what you want?

- **A**
```python
def walk(self):
    return self.sound if self.legs else 'Cannot walk!'
def swim(self):
    return self.sound if self.fin else 'Cannot swim!'
```

- **B**
```python
def walk(self):
    if self.legs = True:
        return self.sound
    else:
        return 'Cannot walk!'
def swim(self):
    if self.fin = True:
        return self.sound
    else:
        return 'Cannot swim!'
```

- **C**
```python
def walk():
    return sound if legs else 'Cannot walk!'
def swim():
    return sound if fin else 'Cannot swim!'
```

- **D**
```python
def walk():
    if legs == True:
        return sound
    else:
        return 'Cannot walk!'
def swim():
    if fin == True:
        return sound
    else:
        return 'Cannot swim!'
```

Correct: **A**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q20 — movie review methods

You have the following definition for a class named Movie.

You need to add three methods to the class:
1. The add_review() method, which adds review scores to the 'reviews' attribute,
2. The rating() method, which computes and returns the average review score of all scores stored in the 'reviews' attribute. If there are no reviews, the method should return 0.
3. The compare() method, which compares the average review scores of two Movie objects and return the title of the Movie object with the higher average review score, i.e., the name of the movie you should watch. In case both Movie objects have the same average review score, the method should return 'Either'.

For example, if we execute the following commands:
movie1 = Movie('In Bruges', 'Martin McDonagh', [5, 3, 5, 4])
movie2 = Movie('Parasite', 'Bong Joon Ho')
print(movie1.compare(movie2))

the output should be:
In Bruges

Which of the following code segments should you place on the missing lines in the class definition to achieve what you want?

- **A**
```python
def add_review(self, score):
    self.reviews += score
def rating(self):
    return sum(self.reviews)/len(self.reviews) if self.reviews else 0
def compare(self, other):
    for first, second in [(self, other), (other, self)]:
        return first.title if first.rating() > second.rating() else 'Either'
```

- **B**
```python
def add_review(score):
    reviews.append(score)
def rating():
    if reviews:
        return sum(reviews)/len(reviews)
    else:
        return 0
def compare(self, other):
    if self.rating > other.rating:
        return self.title
    elif self.rating < other.rating:
        return other.title
    else:
        return 'Either'
```

- **C** `Both code segments will work as intended.`

- **D** `Neither code segments will work as intended.`

Correct: **D**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q21 — datetime weekly dates list

You need to write a function called main, which accepts a string as an argument. The string represents a date as DD-MM-YYYY.

The function should return a list containing 10 strings representing dates, all in that same format.
The first element of the list should be the original input date.
Each further element of the list should be a string representing the date that is exactly one week after the preceding element of the list.

Take a look at the following code segment:

from datetime import datetime, timedelta

def main(string):
    date = datetime.strptime(string, '%d-%m-%Y')
    str_list = [date]
    for i in range(1, 10):
        str_list.append((str_list[i-1] + timedelta(weeks=1)).strftime('%d-%m-%Y'))
    return str_list

Will this code segment work as intended? If not, then why not?

- **A** `This code will not work as intended, because there will be 11 strings in the list instead of 10.`

- **B** `The code will not work because the two methods strptime() and strftime() are mixed up.`

- **C** `This code will not work because str_list[i-1] is a string. Timedelta objects can only be added to datetime objects, and cannot be added to strings.`

- **D** `This code segment will work as intended.`

Correct: **C**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q22 — pandas date column from day month year

Suppose you have the following DataFrame called df:

   Day  Month  Year
0    1      5  2023
1    8      5  2023
2   15      5  2023
3   22      5  2023
4   29      5  2023

You need to create a new column called Date that contains strings representing the dates as constructed from the Day, Month and Year columns. That is, finally the DataFrame should look like this:

   Day  Month  Year        Date
0    1      5  2023  01-05-2023
1    8      5  2023  08-05-2023
2   15      5  2023  15-05-2023
3   22      5  2023  22-05-2023
4   29      5  2023  29-05-2023

Which of the following code segments will achieve what you want? You may assume that the pandas is already imported as pd.

- **A**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime(y, m, d).strftime('%d-%m-%Y') for d, m, y in zip(df['Day'], df['Month'], df['Year'])])
```

- **B**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime.strptime(d, m, y, '%d-%m-%Y') for d, m, y in zip(df['Day'], df['Month'], df['Year'])])
```

- **C**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime(d, m, y).strftime('%d-%m-%Y') for d, m, y in zip(df['Day'], df['Month'], df['Year'])])
```

- **D**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime.strptime(date, '%d-%m-%Y') for date in zip(df['Day'], df['Month'], df['Year'])])
```

Correct: **A**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q23 — pandas above average salary

Consider the following pandas DataFrame called df:

   Name  Age  Salary
0  John   25   50000
1  Jane   30   65000
2  Alex   35   80000
3  Lisa   40   70000
4  Mark   28   55000

You need to perform a series of operations on this DataFrame:
- Operation 1: Create a new column called Above_average, which contains True if the employee's salary is above the average salary of all the employees, otherwise False.
- Operation 2: Create a new column called Salary_difference, which represents how much higher an employee's salary is than the average salary.
- Operation 3: Print the segment of the adapted DataFrame that contains all the columns, but only the rows in which the employees earn more than the average salary.

That is, the final result printed should be:
   Name  Age  Salary  Above_average  Salary_difference
1  Jane   30   65000           True               1000
2  Alex   35   80000           True              16000
3  Lisa   40   70000           True               6000

Which of the following blocks of code will perform these operations as intended? You may assume the pandas module is already imported as pd.

- **A**
```python
mean_salary = round(df['Salary'].mean())
df['Above_average'] = pd.Series([True if salary > mean_salary else False for salary in df['Salary']])
df['Salary_difference'] = df['Salary'] - mean_salary
print(df[df['Above_average']==True])
```

- **B** `None of the blocks of code will work as intended.`

- **C** `Both blocks of code will work as intended.`

- **D**
```python
mean_salary = round(df['Salary'].mean())
df['Above_average'] = df['Salary'].map(lambda x: True if x > mean_salary else False)
df['Salary_difference'] = df['Salary'].map(lambda x: x - mean_salary)
print(df[df['Salary_difference']>0])
```

Correct: **A**

---

### resit-exam-guidelines-for-intro-to-python-6013b0470y-july-2023-q24 — pandas lambda output

What will be the output of the following lines of code?

import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df['C'] = df['A'].map(lambda x: x + df['B'].sum())

print(df)

- **A**
```python
A  B   C
0  1  4  18
1  2  5  21
2  3  6  24
```

- **B**
```python
A  B   C
0  1  4  12
1  2  5  15
2  3  6  18
```

- **C**
```python
A  B   C
0  1  4   9
1  2  5  12
2  3  6  15
```

- **D**
```python
A  B   C
0  1  4  16
1  2  5  17
2  3  6  18
```

Correct: **D**

---


## 2023 Resit Solutions (`resit-solutions-for-introduction-to-python-35761538`)

### resit-solutions-for-introduction-to-python-35761538-q01 — 1_Basics_Logic_1

Suppose you have a list called x containing tuples, where
x = [(1, 2), (3, 4), (5, 6), (7, 8)]

Which of the following lines of code will print True?

- **A** `print(x[0][1] * x[-3][0] == x[2][1])`

- **B** `print(x[1][0] + x[-2][0] == x[-1][1])`

- **C** `print(x[-1][0] - x[-2][0] == x[0][1])`

- **D** `All lines of code will print True.`

Correct: **D**

---

### resit-solutions-for-introduction-to-python-35761538-q02 — 1_Basics_Scope_1

Executing the following program will produce an error. Why?

def power(num, factor):
    result = num ** factor
    return 'The result of {} ** {} is: {}.'.format(num, factor, result)
print(result)

- **A** `Result is a local name that cannot be referenced outside of the function power.`

- **B** `** is not a valid Python operator.`

- **C** `The syntax used in the return statement to format the string is incorrect.`

- **D** `The function called power should not return the string 'The result of {} ** {} is: {}.'.format(num, factor, result), but the value of result.`

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q03 — 1_Basics_Variables_3

What will be printed by the following code segment?

def main(x):
    y = list()
    for i in x:
        if type(i) == type(x):
            y.append(i)
    return y

result = main(['a', 'None', [], {}, '123', 0.05, 111])
print(result)

- **A** `['a', 'None', '123']`

- **B** `[[]]`

- **C** `[None]`

- **D** `[]`

Correct: **B**

---

### resit-solutions-for-introduction-to-python-35761538-q04 — 3_Function_Argument_3

Suppose you have the following function, which takes two integers as arguments:

def main(x, y=11):
    table = []
    i = 1
    while i < y:
        table.append(f'{x} * {i} = {x*i}')
        i += 1
    return table

What will be printed by the following line of code:
print(main(1))

- **A** `['1 * 1 = 1', '1 * 2 = 2', '1 * 3 = 3', '1 * 4 = 4', '1 * 5 = 5', '1 * 6 = 6', '1 * 7 = 7', '1 * 8 = 8', '1 * 9 = 9', '1 * 10 = 10']`

- **B** `['1 * 1 = 1', '1 * 2 = 2', '1 * 3 = 3', '1 * 4 = 4', '1 * 5 = 5', '1 * 6 = 6', '1 * 7 = 7', '1 * 8 = 8', '1 * 9 = 9', '1 * 10 = 10', '1 * 11 = 11']`

- **C** `This code produces an error as there is a missing argument when calling main.`

- **D**
```python
The code produces a syntax error because of the line:
            table.append(f'{x} * {i} = {x*i}')
```

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q05 — Functions Built-in

Suppose you have a list called x, where:

x = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5]

Which of the following code segments will print the following list?
[5, 4, 3, 2, 1]

- **A**
```python
y = list(set(x))
print(sorted(y, reverse = True))
```

- **B** `print(x[::-2])`

- **C** `Both lines of code will print that output.`

- **D** `Neither line of code will print that output.`

Correct: **C**

---

### resit-solutions-for-introduction-to-python-35761538-q06 — Function Flexible Argument

You need to write a function called main which accepts a flexible number of keyword arguments. The function should compute and return the sum of the values of the arguments.

For example, if you call the function as:
main(apple=1.99, banana=0.99, orange=1.49)
it should return:
4.47

Which of the following functions will return the intended value?

- **A**
```python
def main(**kwargs):
    total = 0
    for item, price in kwargs.items():
        total += item
    return total
```

- **B**
```python
def main(**kwargs):
    total = 0
    for price in kwargs.values():
        total += price
    return total
```

- **C**
```python
def main(**kwargs):
    total = 0
    for item, price in kwargs.keys():
        total += price
    return total
```

- **D** `All functions will return the intended value.`

Correct: **B**

---

### resit-solutions-for-introduction-to-python-35761538-q07 — Dictionaries Comprehension

Assume you already have a list of strings called words.

You need to create a dictionary called word_lengths, where the keys are the strings in the list words and the values are their lengths.

Which of the following code segments will work as intended?

- **A** `word_lengths = {length: word for word, length in enumerate(words)}`

- **B** `word_lengths = {len: word for word in words}`

- **C** `word_lengths = {word: len(word) for word in words}`

- **D** `word_lengths = {len: word for word, len in words}`

Correct: **C**

---

### resit-solutions-for-introduction-to-python-35761538-q08 — Dictionaries and Mappings

You are given two lists, called students and grades:
- The students list contains strings representing the names of students.
- The grades list contains integers representing the students' corresponding grade levels.

You need to create a dictionary called grade_counts that counts the number of students in each grade level. That is, the keys of the dictionary are the grade levels and the values are the number of students in that grade.

For example, if you have:
students = ['A', 'B', 'C', 'D', 'E', 'F']
grades = [9, 10, 9, 11, 10, 9]

then the created dictionary grade_counts should be:
{9: 3, 10: 2, 11: 1}

Which of the following code segments will work as intended?

- **A**
```python
grade_counts = {}
for grade in grades:
    if grade not in grade_counts:
        grade_counts[grade] = 0
    grade_counts[grade] += 1
```

- **B**
```python
grade_counts = {}
for student, grade in zip(students, grades):
    if grade in grade_counts:
        grade_counts[grade].append(student)
    else:
        grade_counts[grade] = [student]
```

- **C** `Both of the given options will work as intended.`

- **D** `None of the given options will work as intended.`

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q09 — Dictionaries and Mappings

You have a dictionary that represents the scores of students in a math competition:
math_scores = {'John': 85, 'Sarah': 92, 'Michael': 78, 'Emma': 90, 'David': 82}

You want to find and print the names of the students who scored above the average score.

Which of the following code segments will work as intended?

- **A**
```python
average_score = sum(math_scores.values()) / len(math_scores)
for student in math_scores.keys():
    if math_scores[student] > average_score:
        print(student)
```

- **B**
```python
for student in math_scores:
    if math_scores[student] > (sum(math_scores.values()) / len(math_scores)):
        print(student)
```

- **C** `Both code segments will work as intended.`

- **D** `None of the code segments will work as intended.`

Correct: **C**

---

### resit-solutions-for-introduction-to-python-35761538-q10 — String Methods

What is the output of the following code segment?

x = 'Hello, World!'
print([char for char in x if char.islower()])

- **A** `['e', 'l', 'l', 'o', 'o', 'r', 'l', 'd']`

- **B** `['e', 'l', 'l', 'o', ',', ' ', 'w', 'o', 'r', 'l', 'd', '!']`

- **C** `['h', 'e', 'l', 'l', 'o', 'w', 'o', 'r', 'l', 'd']`

- **D** `['H', 'e', 'l', 'l', 'o', 'W', 'o', 'r', 'l', 'd']`

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q11 — Functions and Imports

What will be the output of the following code segment?

list1 = [5, 10, 15, 20]
list2 = [2, 4, 6, 8]
result = []

for a, b in zip(list1, list2):
    result.append(a // b)

print(result)

- **A** `[1, 2, 3, 4]`

- **B** `[2, 2, 2, 2]`

- **C** `[6, 12, 18, 24]`

- **D** `[2.5, 2.5, 2.5, 2.5]`

Correct: **B**

---

### resit-solutions-for-introduction-to-python-35761538-q12 — Sequences and Access

Suppose you have a list called numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].
Which of the following lines of code will not create a list with the name subset and the value [10, 8, 6, 4, 2]?

- **A** `subset = numbers[::-2][::-1]`

- **B** `subset = numbers[-1::-2]`

- **C** `subset = numbers[::-1][::2]`

- **D** `subset = numbers[::-2]`

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q13 — string - find - 3

You have a string variable called sentence:
sentence = 'I bought a book about programming. The book has a lot of exercises. I enjoy reading a good book.'

You want to replace only the second occurrence of "book" with "novel" in the sentence and save this as new_sentence.

So:
print(new_sentence)
should print:
I bought a book about programming. The novel has a lot of exercises. I enjoy reading a good book.

Which of the following code segments will work as intended?

Hint:
The string find() method takes three arguments: value, start and end. The first argument is required and is the value to search for. The second and third argument are optional, they are indices specifying where to start and end the search, respectively.

- **A**
```python
index = sentence.find('book')
index = sentence.find('book', index + 1)
new_sentence = sentence[:index] + 'novel' + sentence[index + 4:]
```

- **B**
```python
new_sentence = sentence.replace("book", "novel", 2)
new_sentence = new_sentence.replace("novel", "book", 1)
```

- **C** `Both options will work as intended.`

- **D** `None of the options will work as intended.`

Correct: **C**

---

### resit-solutions-for-introduction-to-python-35761538-q14 — string - fstring - 3

You have the following objects loaded in Python:
fruits = ["apple", "banana", "orange"]
count = 3

You want to print the following sentence:
I have 3 fruits: apple, banana, and orange.

Which of the following code fragments will achieve the desired output?

- **A**
```python
message = f"I have {count} fruits: {', '.join(fruits)}."
print(message)
```

- **B**
```python
message = f"I have {count} fruits: {fruits[0]}, {fruits[1]}, and {fruits[2]}."
print(message)
```

- **C** `Both code fragments will achieve the desired output.`

- **D** `Neither of the code fragments will achieve the desired output.`

Correct: **B**

---

### resit-solutions-for-introduction-to-python-35761538-q15 — string - operations - 3

A company wants to extract the components of email addresses. An email address consists of the local part, which comes before the "@" symbol and a domain name, which comes after the "@" symbol.

You need to create a function called main() which accepts a flexible number of strings representing email addresses and returns a DataFrame. Your DataFrame should have a column called 'local' which contains the local parts and a column called 'domain' which contains the domain names of the email addresses that were passed as arguments.

For example, if you execute the following command:
print(main('example@example.com', 'student@uva.nl', 'email@address.com'))

the output should be:
  local   domain
0 example example.com
1 student uva.nl
2 email   address.com

Which of the following code segments will return this dataframe as intended?

You may assume that pandas is already imported as pd.

- **A**
```python
def main(*args):
    data = {}
    data['local'] = pd.Series([email.split("@")[0] for email in args])
    data['domain'] = pd.Series([email.split("@")[1] for email in args])
    return pd.DataFrame(data)
```

- **B**
```python
def main(args):
    return pd.DataFrame({
        'local': [email.split("@")[1] for email in args],
        'data': [email.split("@")[0] for email in args]})
```

- **C**
```python
def main(*args):
    data = {}
    for email in args:
        data['local'] = email.split("@")[0]
        data['domain'] = email.split("@")[1]
    return pd.DataFrame(data)
```

- **D**
```python
def main(*args):
    local = []
    domain = []
    for email in args:
        local.append(email.split("@")[0])
        domain.append(email.split("@")[1])
    return pd.DataFrame({local: domain for local, domain in zip(local, domain)})
```

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q16 — 6_OOP_Easy_1

You have the following definition of a class called Employee:

class Employee:
    def __init__(self, name, role, gender = 'not specified'):
        self.name = name
        self.role = role
        self.gender = gender

What will be the output if we execute the following lines of code?

employee1 = Employee('John Smith', 'HR representative')
print(employee1.name == 'John Smith')
print(employee1.gender == 'not specified')

- **A**
```python
True
True
```

- **B**
```python
True
False
```

- **C**
```python
False
True
```

- **D**
```python
False
False
```

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q17 — 8_Datetime_Easy_2

Which other code fragment will print the same output as the following?

from datetime import datetime, timedelta
print((datetime.strptime('2023/1/10', '%Y/%m/%d') - datetime(2023, 1, 1)).days + 1)

- **A**
```python
from datetime import datetime, timedelta
print(timedelta(datetime(2023, 1, 10) - datetime(2023, 1, 1)).days)
```

- **B**
```python
from datetime import datetime, timedelta
print(timedelta(datetime(2023, 1, 10) - datetime(2023, 1, 1)).days + 1)
```

- **C**
```python
from datetime import datetime, timedelta
print((datetime(2023, 1, 10) - datetime.strptime('2023-1-1', '%Y-%m-%d')).days)
```

- **D**
```python
from datetime import datetime, timedelta
print((datetime(2023, 1, 11) - datetime(2023, 1, 1)).days)
```

Correct: **D**

---

### resit-solutions-for-introduction-to-python-35761538-q18 — pandas - easy - 3

Suppose you have the following DataFrame called df:
  Player  Age  Height
0 John     25     180
1 Jane     30     165
2 Alex     27     175

You may assume that pandas is already imported as pd.

Which of the following lines of code will give an error?

- **A** `print(df.loc[:, 'Age'])`

- **B** `print(df.loc[df['Height'] > 170, ['Player', 'Age']])`

- **C** `print(df[['Player', 'Age']])`

- **D** `print(df[1, 'Age'])`

Correct: **D**

---

### resit-solutions-for-introduction-to-python-35761538-q19 — 6_OOP_Function_1

You have the following definition for a class called Animals:

class Animals:
    def __init__(self, name, sound, legs=None, fin=None):
        self.name = name
        self.sound = sound
        self.legs = legs
        self.fin = fin

    # missing lines
    # ...

You need to add two methods to the class:
1. The walk() method, which returns the 'sound' attribute an Animal object has if the Animal object has 'legs'. If the Animal object does not, return 'Cannot walk!'.
2. The swim() method, which returns the 'sound' attribute an Animal object has if the Animal object has 'fin'. If the Animal object does not, return 'Cannot swim!'.

For example, if we execute the following commands:
cat = Animals('kitty', legs=True, sound='Meow!')
fish = Animals('nemo', fin=True, sound='Blob!')
print(cat.walk())
print(cat.swim())
print(fish.swim())
print(fish.walk())

the output should be:
Meow!
Cannot swim!
Blob!
Cannot walk!

Which of the following code segments should you place on the missing lines in the class definition to achieve what you want?

- **A**
```python
def walk(self):
    return self.sound if self.legs else 'Cannot walk!'
def swim(self):
    return self.sound if self.fin else 'Cannot swim!'
```

- **B**
```python
def walk(self):
    if self.legs == True:
        return self.sound
    else:
        return 'Cannot walk!'
def swim(self):
    if self.fin == True:
        return self.sound
    else:
        return 'Cannot swim!'
```

- **C** `Both code segments will work as intended.`

- **D** `Neither code segment will work as intended.`

Correct: **C**

---

### resit-solutions-for-introduction-to-python-35761538-q20 — 6_OOP_Hard_3

You have the following definition for a class named Movie.

class Movie:
    def __init__(self, title, director, reviews = None):
        self.title = title
        self.director = director
        self.reviews = reviews if reviews else []

    # missing lines
    # ...

You need to add three methods to the class:
1. The add_review() method, which adds review scores to the 'reviews' attribute.
2. The rating() method, which computes and returns the average review score of all scores stored in the 'reviews' attribute. If there are no reviews, the method should return 0.
3. The compare() method, which compares the average review scores of two Movie objects and returns the title of the Movie object with the higher average review score, i.e., the name of the movie you should watch. In case both Movie objects have the same average review score, the method should return 'Either'.

For example, if we execute the following commands:
movie1 = Movie('In Bruges', 'Martin McDonagh', [5, 3, 5, 4])
movie2 = Movie('Parasite', 'Bong Joon Ho')
print(movie1.compare(movie2))

the output should be:
In Bruges

Which of the following code segments should you place on the missing lines in the class definition to achieve what you want?

- **A**
```python
def add_review(self, score):
    self.reviews += score
def rating(self):
    return sum(self.reviews)/len(self.reviews) if self.reviews else 0
def compare(self, other):
    for first, second in [(self, other), (other, self)]:
        return first.title if first.rating() > second.rating() else 'Either'
```

- **B**
```python
def add_review(score):
    reviews.append(score)
def rating():
    if reviews:
        return sum(reviews)/len(reviews)
    else:
        return 0
def compare(self, other):
    if self.rating > other.rating:
        return self.title
    elif self.rating < other.rating:
        return other.title
    else:
        return 'Either'
```

- **C** `Both code segments will work as intended.`

- **D** `Neither code segment will work as intended.`

Correct: **D**

---

### resit-solutions-for-introduction-to-python-35761538-q21 — 8_Datetime_Function_1

You need to write a function called main, which accepts a string as an argument. The string represents a date as DD-MM-YYYY.

The function should return a list containing 10 strings representing dates, all in that same format.
The first element of the list should be the original input date.
Each further element of the list should be a string representing the date that is exactly one week after the preceding element of the list.

Take a look at the following code segment:

from datetime import datetime, timedelta

def main(string):
    date = datetime.strptime(string, '%d-%m-%Y')
    str_list = [date]
    for i in range(1, 10):
        str_list.append((str_list[i-1] + timedelta(weeks=1)).strftime('%d-%m-%Y'))
    return str_list

Will this code segment work as intended? If not, then why not?

- **A** `The code will not work because the two methods strptime() and strftime() are mixed up.`

- **B** `This code will not work because str_list[i-1] is a string. Timedelta objects can only be added to datetime objects, and cannot be added to strings.`

- **C** `This code will not work as intended, because there will be 11 strings in the list instead of 10.`

- **D** `This code segment will work as intended.`

Correct: **B**

---

### resit-solutions-for-introduction-to-python-35761538-q22 — 8_Datetime_Hard_3

Suppose you have the following DataFrame called df:

   Day  Month  Year
0    1      5  2023
1    8      5  2023
2   15      5  2023
3   22      5  2023
4   29      5  2023

You need to create a new column called Date that contains strings representing the dates as constructed from the Day, Month and Year columns. That is, finally the DataFrame should look like this:

   Day  Month  Year        Date
0    1      5  2023  01-05-2023
1    8      5  2023  08-05-2023
2   15      5  2023  15-05-2023
3   22      5  2023  22-05-2023
4   29      5  2023  29-05-2023

Which of the following code segments will achieve what you want? You may assume that the pandas module is already imported as pd.

- **A**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime(y, m, d).strftime('%d-%m-%Y') for d, m, y in zip(df['Day'], df['Month'], df['Year'])])
```

- **B**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime.strptime(d, m, y, '%d-%m-%Y') for d, m, y in zip(df['Day'], df['Month'], df['Year'])])
```

- **C**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime(d, m, y).strftime('%d-%m-%Y') for d, m, y in zip(df['Day'], df['Month'], df['Year'])])
```

- **D**
```python
from datetime import datetime
df['Date'] = pd.Series([datetime.strptime(date, '%d-%m-%Y') for date in zip(df['Day'], df['Month'], df['Year'])])
```

Correct: **A**

---

### resit-solutions-for-introduction-to-python-35761538-q23 — pandas - hard - 3

Consider the following pandas DataFrame called df:

   Name  Age  Salary
0  John   25   50000
1  Jane   30   65000
2  Alex   35   80000
3  Lisa   40   70000
4  Mark   28   55000

You need to perform a series of operations on this DataFrame.
- Operation 1: Create a new column called Above_average, which contains True if the employee's salary is above the average salary of all the employees, otherwise False.
- Operation 2: Create a new column called Salary_difference, which represents how much higher an employee's salary is than the average salary.
- Operation 3: Print the segment of the adapted DataFrame that contains all the columns, but only the rows in which the employees earn more than the average salary.

That is, the final result printed should be:
   Name  Age  Salary  Above_average  Salary_difference
1  Jane   30   65000           True                100
2  Alex   35   80000           True              16000
3  Lisa   40   70000           True               6000

Which of the following blocks of code will perform these operations as intended? You may assume the pandas module is already imported as pd.

- **A**
```python
mean_salary = round(df['Salary'].mean())
df['Above_average'] = pd.Series([True if salary > mean_salary else False for salary in df['Salary']])
df['Salary_difference'] = df['Salary'] - mean_salary
print(df[df['Above_average']==True])
```

- **B**
```python
mean_salary = round(df['Salary'].mean())
df['Above_average'] = df['Salary'].map(lambda x: True if x > mean_salary else False)
df['Salary_difference'] = df['Salary'].map(lambda x: x - mean_salary)
print(df[df['Salary_difference']>0])
```

- **C** `Both blocks of code will work as intended.`

- **D** `None of the blocks of code will work as intended.`

Correct: **C**

---

### resit-solutions-for-introduction-to-python-35761538-q24 — pandas - lambda - 3

What will be the output of the following lines of code?

import pandas as pd

df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
df['C'] = df['A'].map(lambda x: x + df['B'].sum())

print(df)

- **A**
```python
A  B   C
0  1  4  16
1  2  5  17
2  3  6  18
```

- **B**
```python
A  B   C
0  1  4  18
1  2  5  21
2  3  6  24
```

- **C**
```python
A  B   C
0  1  4  12
1  2  5  15
2  3  6  18
```

- **D**
```python
A  B   C
0  1  4   9
1  2  5  12
2  3  6  15
```

Correct: **A**

---


## Trial Final Later-Course Focus (`trial-final-exam-solutions-introduction-to-python-3077951`)

### trial-final-exam-solutions-introduction-to-python-3077951-q01 — 6-OOP-1

You'd like to define a class called Vehicle. It should have two attributes: "name" and "mode", which you want to be initialized at the time of object construction.

The "name" attribute can be any string, and it must be passed to the object constructor. The "mode" attribute is also a string, but it doesn't necessarily need to be passed to the object constructor, then the "mode" attribute should be equal to "land".

For example, if we create a Vehicle object as:
my_car = Vehicle("Mazda")
then the following two conditions should both be true:
my_car.name == "Mazda"
my_car.mode == "land"

Which of the following code segments achieves what you want?

- **A**
```python
class Vehicle:
    def __init__(self, vehicle_name, vehicle_mode="land"):
        self.name = vehicle_name
        self.mode = vehicle_mode
```

- **B**
```python
class Vehicle:
    def __init__(self, vehicle_name, vehicle_mode):
        self.name = vehicle_name
        self.mode = vehicle_mode
```

- **C**
```python
class Vehicle:
    def __init__(self, vehicle_name, vehicle_mode="land"):
        return name, mode
```

- **D**
```python
class Vehicle:
    def __init__(vehicle_name, vehicle_mode):
        name = vehicle_name
        mode = vehicle_mode
```

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q02 — 6-OOP-2

Take a look at the following class definition.

Suppose that we create a Book object and call its add_review method three times, like this:
book_1 = Book("The Lightning Thief", "Rick Riordan")
book_1.add_review(5)
book_1.add_review(3)
book_1.add_review(3)

What will the following command print to the screen?
print(book_1.show_rating())

- **A** `3.7`

- **B** `4`

- **C** `None`

- **D** `3.67`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q03 — 6-strings-1

Imagine that you have a list called students, which is populated by a number of dictionaries.

Each dictionary in the students list has two keys: "Name" and "Grade". The corresponding values are student names (as strings) and course grades (as floats).

For each student, you'd like to print the following text to the screen:
[NAME] has received a grade of [GRADE].
where [NAME] is substituted by the name of the student and [GRADE] is substituted by the actual course grade. The course grade should be displayed to one decimal place after the decimal point.

For example, if:
students = [{"Name": "Adam", "Grade": 7.5}, {"Name": "Bernard", "Grade": 8.0}]
then you'd like to see the following two lines printed to the screen:
Adam has received a grade of 7.5.
Bernard has received a grade of 8.0.

Which of the following code segments will achieve what you want?

- **A**
```python
for student in students:
    print(f"{student['Name']} has received a grade of {student['Grade']:.1f}.")
```

- **B**
```python
for student, grade in students.items():
    print(f"{student} has received a grade of {grade:.1f}.")
```

- **C**
```python
for student in students:
    print(f"{student[\"Name\"]} has received a grade of {student[\"Grade\"]:.1f}.")
```

- **D**
```python
for student, grade in students:
    print(f"{student} has received a grade of {grade:.1f}.")
```

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q04 — 6-strings-2

You need to write a function called format_phone_number that formats phone numbers. The output of the function should be a string that represents a 10-digit number. The input argument is also a string with 10 digits, but the digits may be separated by dashes (the "-" character, at various places).

For example, the following function calls:
format_phone_number("020-525-1400")
format_phone_number("020-5251400")
format_phone_number("020-525-14-00")
should all return the string:
"0205251400"

Which of the following code segments does not achieve what you want?

- **A**
```python
def format_phone_number(number):
    number.replace("-", "")
    return number
```

- **B**
```python
def format_phone_number(number):
    return number.replace("-", "")
```

- **C**
```python
def format_phone_number(number):
    digits = []
    for char in number:
        if char in "0123456789":
            digits.append(char)
    return "".join(digits)
```

- **D**
```python
def format_phone_number(number):
    return "".join(number.split("-"))
```

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q05 — 7-pandas-new_column-1

You have a pandas DataFrame called df. It has a column called "A" and a column called "B". Both contain numbers.

You'd like to create a column called "C", which contains the sum of the numbers in columns "A" and "B". Which of the following code lines will achieve what you want?

- **A** `df["C"] = df["A"] + df["B"]`

- **B** `df["C"] = df["A"].map(lambda x: x + df["B"])`

- **C** `df["C"] = df.columns["A" + "B"]`

- **D** `df["C"] = df["A" + "B"]`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q06 — 7-pandas-selection-1

You have a pandas DataFrame called df that looks like this, when printed:

     A    B    C    D
1  9.1  9.5  9.0  6.0
2  6.4  8.2  7.5  1.7
3  2.5  5.3  8.8  3.0
4  6.7  3.6  7.2  6.9
5  8.4  1.9  8.2  3.3
6  8.1  8.4  9.9  2.2

Suppose that you'd like to create a new DataFrame that only contains those elements of column "B" in df that have an even-numbered index. Which of the following code lines will achieve what you want?

- **A** `df.loc[df.index % 2 == 0, ["B"]]`

- **B** `df[2, 4, 6, "B"]`

- **C** `df.iloc[[2, 4, 6], 2]`

- **D** `df.loc[2::2, "B"]`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q07 — 7-pandas-sorting-1

There are two pandas DataFrames: df1 and df2. They look like this, when printed:

print(df1)

     A    B    C    D
1  5.0  8.2  9.5  4.4
2  6.0  2.4  9.1  3.3
3  3.2  5.2  8.9  3.6
4  7.8  8.7  7.9  8.0
5  1.2  9.7  2.9  3.0

print(df2)

     A    C    D
4  7.8  7.9  8.0
3  3.2  8.9  3.6
2  6.0  9.1  3.3

Which of the following code lines could not have created df2 from df1?

- **A** `df2 = df1.sort_index(ascending=False)[["A", "C", "D"]]`

- **B** `df2 = df1.iloc[[3, 2, 1], [0, 2, 3]]`

- **C** `df2 = df1.loc[2:4, ["A", "C", "D"]].sort_values("D", ascending=False)`

- **D** `df2 = df1.loc[2:4, ["A", "C", "D"]].sort_values("C")`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q08 — 7-pandas-string-1

There is a pandas Series called s, which contains Dutch municipality and corresponding province names, separated by a semicolon and a whitespace. The following, for example, is an element of this Series: "Amsterdam; Noord-Holland".

You'd like to create a new Series that only contains the municipality names from s in the same order. Which of the following code lines will achieve what you want?

- **A** `s.map(lambda x: x.split("; ")[0])`

- **B** `s.split("; ")[0]`

- **C** `s.lambda(x.split("; "))`

- **D** `s.str[:9]`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q09 — 8-datetime-1

Take a look at the following code segment.

from datetime import datetime

def get_months(date_strings):
    dates = []
    for date_str in date_strings:
        if "-" in date_str:
            dates.append(datetime.strptime(date_str, "%d-%m-%Y"))
        elif "/" in date_str:
            dates.append(datetime.strptime(date_str, "%m/%d/%Y"))
        else:
            dates.append(None)
    return [date.month if date is not None else None for date in dates]

Suppose that you call the function like this:
get_months(["03/02/2013", "03.02.2013", "03-02-2013"])

What does the function call return?

- **A** `[3, None, 2]`

- **B** `[2, None, 3]`

- **C** `[3, 2]`

- **D** `[2, 3]`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q10 — 8-datetime-2

Suppose that you want to write a function called day_of_year that takes a datetime value and returns the number of the day that the datetime value represents within the year. The return value is therefore always an integer between 1 and 366.

For example, the function call:
day_of_year(datetime(2022, 2, 1))
should return the integer:
32

Which of the following code segments will achieve what you want? (You can assume that the datetime and timedelta classes are already imported from the datetime module.)

- **A**
```python
def day_of_year(dt):
    return (dt - datetime(dt.year, 1, 1)).days + 1
```

- **B**
```python
def day_of_year(dt):
    return timedelta(dt - datetime(dt.year, 1, 1)) + 1
```

- **C**
```python
def day_of_year(dt):
    return dt - datetime(dt.year, 1, 1) + 1
```

- **D**
```python
def day_of_year(dt):
    return (dt - datetime(dt.year, 1, 0)).days
```

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q11 — 8-dict_comprehension-1

You have a list of strings called list_1, in which every element is unique.

Which of the following code lines will create a dictionary, in which the keys are the elements of list_1 and the values are the number of characters in the corresponding key?

- **A** `{item: len(item) for item in list_1}`

- **B** `[len(item) for item in list_1]`

- **C** `{item for item in list_1 if len(item) > 0}`

- **D** `{len(item): item for item in list_1}`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q12 — 8-list_comprehension-1

Suppose that you have a list of letters called list_1. Some letters are upper case, others are in lower case.

You'd like to create another list that contains the same letters in the same order, but you want to turn every upper case letter into its lower case version, and every lower case letter into its upper case version.

Which of the following code lines will achieve what you want?

- **A** `[letter.upper() if letter.islower() else letter.lower() for letter in list_1]`

- **B** `[letter.upper() for letter in list_1 if letter.islower() else letter.lower()]`

- **C** `[letter.lower() for letter in list_1 if letter.isupper()] + [letter.upper() for letter in list_1 if letter.islower()]`

- **D** `[letter.capitalize() for letter in list_1 if not letter.iscapitalized()]`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q13 — Basic logic

Suppose you have three variables x, y, z as follows:

x = 'x'
y = 3
z = 3.0

What are the outputs of the following lines of code?
print(x == y)
print(y == z)
print(x == z)
print(x == y == z)

- **A**
```python
False
True
False
False
```

- **B**
```python
True
True
True
True
```

- **C**
```python
False
False
False
True
```

- **D**
```python
True
False
False
False
```

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q14 — Basic loop

You need to write a simple loop that iterates over the integers from 1 to 10, and in each iteration, prints the sum of the current and the previous number. In the first iteration, just take the previous number to be 0.

For example:
1 + 0 = 1
2 + 1 = 3
3 + 2 = 5
...
10 + 9 = 19

Choose the program that will print the correct output (i.e. only the sums).

- **A**
```python
previous = 0
for i in range(1, 11):
    print(i + previous)
    previous = i
```

- **B**
```python
i = 0
while i <= 10:
    print(i + (i - 1))
    i += 1
```

- **C** `Both of the above`

- **D** `Neither of the above`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q15 — Basic scope

Executing the following program will produce an error. Why?

def cube(num):
    result = num ** 3
    return f'The cube of {num} is: {result}.'

print(result)

- **A** `Result is a local variable and cannot be referenced outside of the function`

- **B** `** is not a valid Python operator.`

- **C** `The syntax of the f-string is incorrect.`

- **D** `You can only use either print or return, but not both.`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q16 — List lambda

You already have a list named list_1 with 2 lambda functions as follows:

list_1 = [lambda a, b: a + b, lambda a, b: a * b]

What would be printed by the following code snippet?
print(list_1[0](1, 2) ** list_1[1](1, 2))

- **A** `6`

- **B** `7`

- **C** `8`

- **D** `9`

Correct: **D**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q17 — List logic

You have the following function called main:

def main(x):
    y = []
    for i in x:
        if len(i) == 0:
            y.append(True)
        else:
            y.append(False)
    return y[0] == y[1] == y[2]

What are the outputs of the following lines:
main([[], (), []])
main([[1], [2, 2], [3, 3, 3]])
main([[1], [2], [3]])

- **A**
```python
True
True
True
```

- **B**
```python
True
False
True
```

- **C**
```python
True
False
False
```

- **D**
```python
False
False
True
```

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q18 — List loop

How do you break a list into a list of lists, in which a sub-list consists of 3 values each?

For example, if the original list x is:
x = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']
then how would you create:
y = [['a', 'b', 'c'], ['d', 'e', 'f'], ['g', 'h', 'i']]

- **A** `y = [x[i:i + 3] for i in range(0, 7, 3)]`

- **B** `y = [x[0::3] for i, enumerate(x)]`

- **C** `Both of the above work`

- **D** `Neither of the above works`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q19 — trial-dictionary-1

You have to write a function called main that accepts a dictionary as an input argument. Both the keys and the values of the input are integers.

Return another dictionary that has the same keys as the input argument. For each output key, the corresponding value should be calculated as the sum of those values from the input dictionary, whose keys are smaller than, or equal to, the output key in question.

For example:
main({5: 1, 2: 5, 4: 2})
should return a dictionary that is equal to:
{5: 8, 2: 5, 4: 7}

Which of the following programs works as intended?

- **A**
```python
def main(d1):
    running_total = 0
    d2 = {}
    for key in sorted(d1.keys()):
        running_total += d1[key]
        d2[key] = running_total
    return d2
```

- **B**
```python
def main(d):
    result = {}
    for output_key in d.keys():
        result[output_key] = sum([v for k, v in d.items() if k <= output_key])
    return result
```

- **C** `Both of the above works as intended`

- **D** `None of the above work as intended`

Correct: **C**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q20 — trial-dictionary-2

What is the result of the following program?

l1 = [1, 2, 3, 4]
l2 = [2, 3, 4, 5]

d1 = {}
for key, value in zip(l1, l2):
    d1[key] = value

d2 = {}
for key, value in enumerate(l2, 1):
    d2[key] = value

print(d1 == d2)

- **A** `True`

- **B** `False`

- **C** `An error message.`

- **D** `None of the above`

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q21 — trial-dictionary-3

d1 = {1: 10, 2: 20, 3: 30, 4: 40}

The following codes all print the same value, except one. Which one?

- **A**
```python
result = 0
for key, value in d1:
    result += value
print(result)
```

- **B**
```python
result = 0
for key in d1.keys():
    result += d1[key]
print(result)
```

- **C**
```python
result = 0
for value in d1.values():
    result += value
print(result)
```

- **D**
```python
result = sum(d1.values())
print(result)
```

Correct: **A**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q22 — trial-functions-1

You have the following string
x = 'Amsterdam'

Which script, using the count string method, would print the following value:
1

- **A** `print(count(x, 'a'))`

- **B** `print(x.count('a'))`

- **C** `Both scripts would deliver that result`

- **D** `Neither script would deliver that result`

Correct: **B**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q23 — trial-functions-2

Take a look at the following function definition.

def calculation(func, *args):
    result = 0
    for el in args:
        result += func(el)
    return result

Which of the following function calls would return the number 30 as a result?

- **A** `calculation(lambda x: x + 5, 1, 2, 3, 4)`

- **B** `calculation(lambda x: x**2, 1, 2, 3, 4)`

- **C** `Both function calls would lead to that result`

- **D** `Neither function call would lead to that result`

Correct: **C**

---

### trial-final-exam-solutions-introduction-to-python-3077951-q24 — trial-functions-3

If you know the radius r of a circle and you want to calculate its area, you need the value of pi from the math package and apply the formula:
πr²

Suppose that the variable r already contains the radius of the circle. Which script does not print the correct answer for the area?

- **A**
```python
import math
print(math.pi * r ** 2)
```

- **B**
```python
from math import pi
print(pi * r ** 2)
```

- **C**
```python
import math as constants
print(math.pi * r ** 2)
```

- **D**
```python
from math import pi as constant
print(constant * r ** 2)
```

Correct: **C**

---
