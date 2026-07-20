# Inheritance
"""
Single Inheritance
Multiple Inheritane
Multilevel Inheritance
Hierarchical Inheritance
"""
#Single
class A:
    def show(self):
        print("A")

class B(A):
    pass

obj = B()
obj.show()

#Multiple

class Temp1:
    def showtemp1(self):
        print("Temp1")

class Temp2:
    def showtemp2(self):
        print("Temp2")

class Temp3(Temp1,Temp2):
    pass

obj2 = Temp3()
obj2.showtemp1()
obj2.showtemp2()

#Multilevel

class ClassA:
    def funcA(self) : 
        print("Class A")

class ClassB(ClassA):
    def funcB(self):
        print("Class B")

class ClassC(ClassB):
    def funcC(self):
        print("Class C")

obj3 = ClassC()
obj3.funcA()
obj3.funcB()
obj3.funcC()

#Hierarchical
class Parent:
    def Parentfunc(self):
        print("Parent Function")

class Child1(Parent):
    pass

class Child2(Parent):
    pass

Child1().Parentfunc()
Child2().Parentfunc()
