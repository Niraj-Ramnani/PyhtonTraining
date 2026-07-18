# 4. Write a program that prints the pyramid pattern using nested loops
n = int(input("Enter a value : "))
for i in range (1 , n +1):
    for _ in range (n-i):
        print(" ",end = "")
    for _ in range(2*i-1):
        print("*",end="")
    print()

