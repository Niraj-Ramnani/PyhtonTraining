# Synchronous API example
import time


def get_user():
    time.sleep(3)
    return "User data"


def get_orders():
    time.sleep(2)
    return "Order data"


start = time.time()

user = get_user()
orders = get_orders()

print(user)
print(orders)

print("Time:", time.time() - start)

# time taken 5 seconds 