def right_triangle(num):
    for i in range( 1, num + 1):
        for j in range(i):
            print("*", end="")
        print()

def inverted_triangle(num):
    for i in range (num , 0 , -1):
        for j in range(i):
            print("*", end="")
        print()

def full_pyramid(num):
    for i in range (1,num+1):
        for j in range(num - i):
            print(" ",end="")
        for k in range (2 *i -1):
            print("*",end ="")
        print()


num = int(input("Enter a number: "))
print("pattern 1")
right_triangle(num)
print("pattern 2")
inverted_triangle(num)
print("pattern 3")
full_pyramid(num)