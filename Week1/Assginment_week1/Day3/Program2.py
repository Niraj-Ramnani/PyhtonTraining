# 2. Enhance the previous program to include try-except blocks for file-handling errors.
def fact(n):
    if n <=1:
        return 1
    return fact(n-1) * n

try:
    file = open("file.txt","r")
    num = int(file.read())
    print("Factorial of the numeber : ",fact(num))
    file.close()

except FileNotFoundError:
    print("Error : File not Found")

except ValueError:
    print("Error : Not a valid intiger ")

