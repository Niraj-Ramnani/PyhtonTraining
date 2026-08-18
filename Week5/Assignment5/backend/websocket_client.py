import asyncio
import json
import logging
import websockets
from websockets.exceptions import ConnectionClosed

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class OrderWebSocketClient:
    def __init__(self, uri: str = "ws://127.0.0.1:8765", customer_id: int = 1, name: str = "Customer"):
        self.uri = uri
        self.customer_id = customer_id
        self.name = name
        self.websocket = None
        self.received_updates: list[dict] = []
        self._listener_task = None
        self.is_connected = False

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.uri)
            self.is_connected = True
            logging.info(f"[{self.name}] Connected to WebSocket server at {self.uri}")

            await self.send({
                "action": "identify",
                "customer_id": self.customer_id,
                "name": self.name,
            })

            ident_response = await self.recv()
            logging.info(f"[{self.name}] Auth Response: {ident_response.get('message')}")
            return True
        except Exception as e:
            logging.error(f"[{self.name}] Failed to connect: {e}")
            self.is_connected = False
            return False

    async def send(self, data: dict):
        if not self.websocket or not self.is_connected:
            raise RuntimeError("Client is not connected to WebSocket server")
        await self.websocket.send(json.dumps(data))

    async def recv(self) -> dict:
        if not self.websocket or not self.is_connected:
            raise RuntimeError("Client is not connected to WebSocket server")
        raw = await self.websocket.recv()
        return json.loads(raw)

    async def get_order_status(self, order_id: int) -> dict:
        logging.info(f"[{self.name}] Requesting status for Order #{order_id} via WebSocket (No HTTP)...")
        await self.send({
            "action": "get_order_status",
            "order_id": order_id,
        })
        response = await self.recv()
        return response

    async def subscribe_order(self, order_id: int) -> dict:
        logging.info(f"[{self.name}] Subscribing to real-time events for Order #{order_id}...")
        await self.send({
            "action": "subscribe_order",
            "order_id": order_id,
        })
        response = await self.recv()
        return response

    async def start_listening(self):
        async def _listen_loop():
            try:
                async for message_str in self.websocket:
                    msg = json.loads(message_str)
                    if msg.get("type") == "ORDER_STATUS_UPDATE":
                        logging.info(
                            f"[{self.name}] REAL-TIME BROADCAST: Order #{msg['order_id']} ({msg['restaurant']}) status changed to -> {msg['status']}"
                        )
                        self.received_updates.append(msg)
                    else:
                        logging.info(f"[{self.name}] Message received: {msg}")
            except ConnectionClosed:
                logging.info(f"[{self.name}] Server connection closed.")
            except Exception as e:
                logging.error(f"[{self.name}] Listener error: {e}")
            finally:
                self.is_connected = False

        self._listener_task = asyncio.create_task(_listen_loop())

    async def close(self):
        logging.info(f"[{self.name}] Disconnecting gracefully...")
        self.is_connected = False
        if self._listener_task:
            self._listener_task.cancel()
        if self.websocket:
            await self.websocket.close()
            logging.info(f"[{self.name}] Disconnected.")
