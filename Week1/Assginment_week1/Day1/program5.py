# 5. Understand the basics of memory management in Python, such as how objects are allocated and deallocated.
a = 10
b = a 
print(f"Value of a : {a} and value of b : {b}")

print(f"id of a {id(a)} and id of b {id(b)}")

'''
Python automatically manages memory using its memory manager.
Variables store references to objects, not the actual objects.

'''