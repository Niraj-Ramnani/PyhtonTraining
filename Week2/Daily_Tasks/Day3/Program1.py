# Shallow and Deep Copy
import copy

# Original list
original = [
    [1, 2, 3],
    [4, 5, 6]
]

# Shallow copy
shallow = copy.copy(original)

# Deep copy
deep = copy.deepcopy(original)


print("Original :", original)
print("Shallow  :", shallow)
print("Deep     :", deep)

# Modifying
original[0][1] = 99


print("Original :", original)
print("Shallow  :", shallow)
print("Deep     :", deep)


original.append([7, 8, 9])

print("\nAfter appending a new list to original")
print("Original :", original)
print("Shallow  :", shallow)
print("Deep     :", deep)