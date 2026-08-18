import asyncio
import httpx
import time


async def fetch_data(client, url):
    response = await client.get(url)
    return response.json()


async def main():
    start = time.perf_counter()

    async with httpx.AsyncClient() as client:
        users, posts, comments = await asyncio.gather(
            fetch_data(
                client,
                "https://jsonplaceholder.typicode.com/users"
            ),
            fetch_data(
                client,
                "https://jsonplaceholder.typicode.com/posts"
            ),
            fetch_data(
                client,
                "https://jsonplaceholder.typicode.com/comments"
            )
        )

    print("Users:", len(users))
    print("Posts:", len(posts))
    print("Comments:", len(comments))

    print(f"Time: {time.perf_counter() - start:.2f} seconds")


asyncio.run(main())