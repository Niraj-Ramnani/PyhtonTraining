def add(a,b):
    return a + b

def substract(a,b):
    return a - b

def multiply(a,b):
    return a * b

def divide(a,b):
    if b == 0:
        print("Can not divide ")
    else:
        return a/b
    

if __name__ == "__main__":
    print("Testing add function : ",add(5,5))