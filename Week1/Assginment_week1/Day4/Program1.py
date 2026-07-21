1. # Write a program to add two matrices.
import numpy as np

def getdata():
    matrix = []
    for i in range(rows):
        row = list(map(int,input(f"Enter row {i +1 } ").split()))
        if len(row) != cols:
            raise ValueError(f"row must contain {cols} elements ")
        matrix.append(row)
    return matrix

try:
    rows = int(input("Enter number of rows : "))
    cols = int(input("Enter number of columns : "))
    print("Enter elements for matrix 1 : ")
    matrix1 = getdata()

    print("Enter elements for matrix 2 : ")
    matrix2 = getdata()

    matrix1 = np.array(matrix1)
    matrix2 = np.array(matrix2)

    res = matrix1 + matrix2
    print("matrix 1")
    print(matrix1)
    
    print("matrix 2")
    print(matrix2)

    print("result matrix ")
    print(res)

except Exception as e:
    print("Error Occured " ,e)

    
