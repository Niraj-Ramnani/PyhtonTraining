# 4. Given a tuple representing the dimensions (length, width, height) of a rectangle, write a program to unpack the tuple and print the dimensions separately.
try:
    dimensions = (5,10,15)
    l,w,h = dimensions
    print("Lengt : ",l)
    print("Width : ",w)
    print("Height : ",h)

except Exception as e:
    print("Error : ",e)