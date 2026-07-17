import module
from module import add
from module import multiply

a,b = map(int,input("Enter two values : ").split())

print("Addition is : ",add(a,b))
print("Multiplication is : ",multiply(a,b))