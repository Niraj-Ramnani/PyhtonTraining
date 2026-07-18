#1. Write a program to swap the values of two variables without using a temporary variable.
a,b = map(int,input("Enter two values : ").split())
print(f"Value before swaping a = {a} , b = {b}")
a,b = b,a
print(f"Value after swaping a = {a} , b = {b}")
