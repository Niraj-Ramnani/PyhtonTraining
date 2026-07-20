#Polymorphism
class A:
    def func(self):
        print("Function of class A")

class B:
    def func(self):
        print("Function of class B")

objs = [A(),B()]

for obj in objs:
    obj.func()