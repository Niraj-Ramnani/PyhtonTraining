#Closure is function remembers variable from its enclosing funciton even after function is executed 
def counter():

    count = 0

    def increment():

        nonlocal count
        count += 1
        return count

    return increment


c = counter()

print(c())
print(c())
print(c())