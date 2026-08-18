import asyncio


async def fetch_data():

    for attempt in range(1, 4):

        try:
            print(f"Attempt {attempt}")

            await asyncio.sleep(1)

            if attempt < 3:
                raise Exception("Temporary failure")

            return "Data received"

        except Exception as error:
            print(error)

    return None


async def main():
    result = await fetch_data()
    print(result)


asyncio.run(main())