import asyncio
import time


async def get_user():
    await asyncio.sleep(3)
    return "User data"


async def get_orders():
    await asyncio.sleep(2)
    return "Order data"


async def main():

    start = time.time()

    user, orders = await asyncio.gather(
        get_user(),
        get_orders()
    )

    print(user)
    print(orders)

    print("Time:", time.time() - start)


asyncio.run(main())