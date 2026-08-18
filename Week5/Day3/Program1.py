import asyncio
import time


async def get_user():
    print("Fetching user...")
    await asyncio.sleep(2)
    return {
        "id": 1,
        "name": "User1"
    }


async def get_orders():
    print("Fetching orders...")
    await asyncio.sleep(3)
    return [
        {"id": 101, "amount": 500}
    ]


async def get_payment():
    print("Fetching payment...")
    await asyncio.sleep(2)
    return {
        "status": "paid"
    }


async def main():

    start = time.time()

    user, orders, payment = await asyncio.gather(
        get_user(),
        get_orders(),
        get_payment()
    )

    result = {
        "user": user,
        "orders": orders,
        "payment": payment
    }

    print(result)

    print("Time:", time.time() - start)


asyncio.run(main())