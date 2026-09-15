import asyncio
import threading
import time


def number_generator(limit):
    for value in range(1, limit + 1):
        yield value * 2


def decorator_example(func):
    def wrapper(*args, **kwargs):
        print("before call")
        result = func(*args, **kwargs)
        print("after call")
        return result
    return wrapper


@decorator_example
def greet(name):
    return f"Hello, {name}!"


class FileHandler:
    def __enter__(self):
        self.file = open("sample.txt", "w")
        return self.file

    def __exit__(self, exc_type, exc_value, traceback):
        self.file.close()
        print("file closed")


async def async_task(name):
    await asyncio.sleep(1)
    return f"Task {name} finished"


def thread_worker(name):
    for i in range(3):
        print(f"Thread {name}: {i}")
        time.sleep(0.2)


numbers = list(number_generator(5))
print(numbers)
print(greet("Python"))

with FileHandler() as file:
    file.write("Advanced Python practice")

async def run_async():
    result = await async_task("A")
    print(result)

asyncio.run(run_async())

thread_1 = threading.Thread(target=thread_worker, args=("One",))
thread_2 = threading.Thread(target=thread_worker, args=("Two",))
thread_1.start()
thread_2.start()
thread_1.join()
thread_2.join()

squares = [x ** 2 for x in range(1, 6)]
print(squares)

student_scores = {"A": 90, "B": 85, "C": 95}
filtered = {name: score for name, score in student_scores.items() if score >= 90}
print(filtered)

add = lambda a, b: a + b
print(add(10, 20))

try:
    value = 10 / 0
except ZeroDivisionError:
    print("Cannot divide by zero")
finally:
    print("This always runs")
