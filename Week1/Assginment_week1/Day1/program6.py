# 6. Run simple code snippets to observe how Python handles variables and memory.
a = 100
b = a

print("Before changing:")
print("a =", a, "ID:", id(a))
print("b =", b, "ID:", id(b))

a = 200

print("\nAfter changing a:")
print("a =", a, "ID:", id(a))
print("b =", b, "ID:", id(b))

'''
If two variables refer to the same object, they have the same id().
Assigning a new value to an immutable object (such as an integer or string) creates a new object

'''