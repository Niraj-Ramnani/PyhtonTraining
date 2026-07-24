class Rectangle:

    def __init__(self, l, w):
        self.length = l
        self.width = w

    @property
    def perimeter(self):
        return 2 * (self.length + self.width)

r = Rectangle(10, 5)

print(r.perimeter)