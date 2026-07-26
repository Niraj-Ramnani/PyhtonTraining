# 5. Write a higher-order function that returns different mathematical functions based on user choice.
def add(a,b):
    return a + b

def substract(a,b):
    return a - b

def multiply(a,b):
    return a * b

def dvivide(a,b):
    if b == 0:
        raise ValueError("Can not divide by zero ")

    return a / b

def math_function(choice):
    operations = {
        1 : add,
        2 : substract,
        3 : multiply,
        4 : dvivide
    }

    if choice not in operations:
        raise ValueError("Invalid Choice ")

    return operations[choice]

def main():
    while(True):
        try:
            operation = int(input("\n choose one option \n 1 Add \n 2 Substract \n 3 Multiply \n 4 Divide \n 5 Exit \n"))
            if operation == 5:
                print("Program Executed ")
                break
            num1 = int(input("Enter first Number : "))
            num2 = int(input("Enter second Number : "))

            higer_order_function = math_function(operation)
            output = higer_order_function(num1,num2)
            print("Output : ",output)

        except Exception as e:
            print("Error ",e)

if __name__ == "__main__":
    main()

