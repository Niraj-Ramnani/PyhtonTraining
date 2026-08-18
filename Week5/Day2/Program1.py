# concurent execution 
import asyncio
import time


async def task1():
    print("Task 1 started")
    await asyncio.sleep(3)
    print("Task 1 finished")


async def task2():
    print("Task 2 started")
    await asyncio.sleep(2)
    print("Task 2 finished")


async def main():
    start = time.time()
    t1 = asyncio.create_task(task1())
    t2 = asyncio.create_task(task2())

    await t1
    await t2

    print("Time:", time.time() - start)


asyncio.run(main())