# Basic class and oject program
class Student:
    branch = "CS"
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def greet(self):
        print("Hello ",self.name)

s1 = Student("aa" , 22)
s1.greet()
print("name : ",s1.name)
print("age : ",s1.age)
print("branch : ",s1.branch)

        