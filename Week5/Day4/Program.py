import asyncio
import websockets


clients = set()


async def broadcast(message):
    if clients:
        await asyncio.gather(
            *(client.send(message) for client in clients)
        )


async def handle_client(websocket):
    clients.add(websocket)

    print("Client connected")
    print("Total clients:", len(clients))

    try:
        async for message in websocket:
            print("Received:", message)

            await broadcast(message)

    except websockets.ConnectionClosed:
        print("Client disconnected")

    finally:
        clients.discard(websocket)

        print("Total clients:", len(clients))


async def main():
    async with websockets.serve(
        handle_client,
        "localhost",
        8765
    ):
        print("Server running on ws://localhost:8765")
        await asyncio.Future()


asyncio.run(main())