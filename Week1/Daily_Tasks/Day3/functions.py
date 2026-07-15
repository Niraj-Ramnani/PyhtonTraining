# Noramal function with parameters
def greet(name):
    print(f"hello , {name}")

greet(input("Enter your name : "))

# Functions with return value

def add(a,b):
    return a + b

a, b = map(int,input("enter two values : ").split())
print("Sum is : ",add(a,b))

"""
diffrent way of puting arguments in a function
1 positional  arguments
2 keyword arguments
3 default arguments
4 variable length arguments
5 keyword varaible length arguments
"""


# positonal 

def introduce(name , age):
    print(f"name is {name} and age is {age}")

introduce("abc",22)

#keyword

introduce(age = 22 , name = "abc")

#default

def greeting(name = "Guest"):
    print(f"Hello , {name}")

greeting("xyx")
greeting()

#Variable (any number of possitional arguments )

def total(*args):
    print(args)
    print(sum(args))

nums = list(map(int,input("enter values to add : ").split()))
#value store in list are usded to unpack the value in the form of list 
total(*nums)

#keyword variable
#keyword are store in form of dictinory
def details(**kwargs):
    print(kwargs)

name,age = input("enter name and age ").split()
details(name = name , age = int(age))


#nested functions

def outer():
    print("Outer ")
    def inner():
        print("Inner")
    inner()

outer()


# combination of postional and keyword
# before / are possitional and after * are of keyword
def func(a,b,/,*,c,d):
    return a + b + c +d
print(func(5,10,c = 15,d=20))


#Scope
"""
variable inside the function is of local scope 
and created in main body or created using global keyword

"""

def func():
    global y
    y = 100
func()
print(y)


#LEBG rule(local,enclosing,builtin,global)

x = "Global"
def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print("local scope : ", x)
    inner()
    print("enclosing scope : ",x)
outer()
print("global scope : ",x)