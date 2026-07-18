#1. Implement a recursive function to calculate the factorial of a given number.
def fact(n):
    if n <=1:
        return 1
    return fact(n-1) * n

num = int(input("Enter a number : "))
print("Factorial of the number ",fact(num))