# 2. Build an inventory backup system to compare shallow and deep copy behavior.

import copy

# Original 
inventory = {
    "Laptop": {
        "quantity": 10,
        "price": 50000
    },
    "Mouse": {
        "quantity": 25,
        "price": 500
    }
}

# Create Backups using shallow and deep copy 
shallow_backup = copy.copy(inventory)
deep_backup = copy.deepcopy(inventory)

print("Original Inventory:")
print(inventory)

# Modify Original Inventory
inventory["Laptop"]["quantity"] = 5

print("\nAfter Modifying Original ")

print("\nOriginal Inventory:")
print(inventory)

print("\nShallow Backup:")
print(shallow_backup)

print("\nDeep Backup:")
print(deep_backup)