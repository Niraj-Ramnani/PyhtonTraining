import asyncio
import websockets


async def connect():
    async with websockets.connect("ws://localhost:8765") as websocket:

        while True:
            message = input("Enter message: ")

            await websocket.send(message)

            response = await websocket.recv()

            print("Server:", response)


asyncio.run(connect())