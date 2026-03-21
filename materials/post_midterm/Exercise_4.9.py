"""
Create a 'Student' class that has three string attributes: 'name', 'department', 
and 'university'.

'name' and 'department' must be passed to the 'Student' class at object 
construction (in this order). 

'university' is an optional argument in the constructor, which takes the value 
Utrecht University by default.

Finally, add a method called 'info' to the class, which returns the following 
string:
"[NAME] studies at the [DEPT] Department of [UNI]."
where: 
- [NAME] should be replaced with the student's name, 
- [DEPT] should be replaced with the student's department, and
- [UNI] should be replaced with the student's university.

Use the (incomplete) code segment at the bottom of this question to start with, 
and modify it as needed.

For example: 
If we create an object from your class as:
student_1 = Student('Jan', 'Economics')
then the method call student_1.info() should return the string: 
'Jan studies at the Economics Department of Utrecht University.'
"""

class Student:
    def __init__(self):
        self.name = 'name'

    def info(self):
        'some info'