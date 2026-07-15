#Decorators take function as parameter and returns same function with a modification

# decorator for function without an argument

def changecase(func):
    def wrap():
        return func().upper()
    return wrap
@changecase
def func():
    return "characters"

print(func())

# decorators for the function with arguments

def greater(divide):
    def wrap(a,b):
        if a<b:
            a,b = b,a
        return divide(a,b)
    return wrap

@greater
def divide(a,b):
    print("division of the number is : " , a//b)


a,b = map(int,input("enter two values : ").split())
divide(a,b)


# Decorator with arguments


def repeat(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for i in range(times):
                print(f"Execution {i + 1}")
                func(*args, **kwargs)
        return wrapper
    return decorator


@repeat(3)
def greet():
    print("Hello!")


greet()