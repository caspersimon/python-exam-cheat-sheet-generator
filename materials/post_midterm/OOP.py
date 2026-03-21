class Rectangle:
    def __init__(self,length,width):
        self.length = length
        self.width = width
        self.midpoint = f'The midpoint of this rectangle is {length/2 , width/2}'
    def area(self):
        return self.length*self.width
    def hstretch(self,factor):
        self.width = factor * self.width

a_particular_rectangle = Rectangle(2,3)
a_particular_rectangle.hstretch(3)
print(a_particular_rectangle.width)

class Square(Rectangle):
    def __init__(self, side):
        self.side = side
        super().__init__(side, side)

a_particular_square = Square(4)
print(a_particular_square.width == a_particular_square.length)
a_particular_square.hstretch(2)
print(a_particular_square.width == a_particular_square.length)
