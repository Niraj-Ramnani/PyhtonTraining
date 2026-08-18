import asyncio
import json
import logging
import websockets
from websockets.exceptions import ConnectionClosed

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


class OrderWebSocketServer:
    def __init__(self, host: str = "127.0.0.1", port: int = 8765):
        self.host = host
        self.port = port
        self.clients: dict[websockets.WebSocketServerProtocol, dict] = {}
        self.orders: dict[int, dict] = {
            101: {
                "order_id": 101,
                "customer_id": 1,
                "restaurant": "Spice Villa",
                "status": "PLACED",
                "items": ["Paneer Tikka x2", "Butter Chicken x1"],
                "total_amount": 780.0,
            },
            102: {
                "order_id": 102,
                "customer_id": 2,
                "restaurant": "Pizza Point",
                "status": "PLACED",
                "items": ["Cheese Pizza x1", "Cold Coffee x2"],
                "total_amount": 420.0,
            },
            103: {
                "order_id": 103,
                "customer_id": 3,
                "restaurant": "Burger Barn",
                "status": "PLACED",
                "items": ["Cheese Burger x2", "French Fries x1"],
                "total_amount": 350.0,
            },
        }

    async def register(self, websocket):
        self.clients[websocket] = {
            "customer_id": None,
            "name": "Anonymous",
            "subscribed_orders": set(),
        }
        logging.info(f"Client connected: {websocket.remote_address}. Total active clients: {len(self.clients)}")

    async def unregister(self, websocket):
        client_info = self.clients.pop(websocket, None)
        if client_info:
            name = client_info.get("name", "Anonymous")
            logging.info(f"Client disconnected gracefully: {name}. Total active clients: {len(self.clients)}")

    async def broadcast_order_update(self, order_id: int, new_status: str):
        if order_id not in self.orders:
            logging.warning(f"Cannot broadcast: Order {order_id} not found.")
            return

        self.orders[order_id]["status"] = new_status
        payload = json.dumps({
            "type": "ORDER_STATUS_UPDATE",
            "order_id": order_id,
            "status": new_status,
            "customer_id": self.orders[order_id]["customer_id"],
            "restaurant": self.orders[order_id]["restaurant"],
            "timestamp": asyncio.get_event_loop().time(),
        })

        target_clients = []
        for ws, info in list(self.clients.items()):
            if order_id in info["subscribed_orders"] or info["customer_id"] == self.orders[order_id]["customer_id"]:
                target_clients.append(ws)

        logging.info(f"Broadcasting Order #{order_id} -> {new_status} to {len(target_clients)} client(s)...")

        for ws in target_clients:
            try:
                await ws.send(payload)
            except ConnectionClosed:
                await self.unregister(ws)
            except Exception as e:
                logging.error(f"Error sending broadcast to client: {e}")

    async def handle_message(self, websocket, message_str: str):
        try:
            msg = json.loads(message_str)
        except json.JSONDecodeError:
            await websocket.send(json.dumps({
                "type": "ERROR",
                "message": "Invalid JSON format",
            }))
            return

        action = msg.get("action")
        client_info = self.clients.get(websocket)

        if action == "identify":
            customer_id = msg.get("customer_id")
            name = msg.get("name", f"Customer_{customer_id}")
            if not customer_id:
                await websocket.send(json.dumps({"type": "ERROR", "message": "customer_id is required for identify action"}))
                return
            client_info["customer_id"] = int(customer_id)
            client_info["name"] = str(name)
            logging.info(f"Client identified as {name} (Customer ID: {customer_id})")
            await websocket.send(json.dumps({
                "type": "IDENTIFIED",
                "customer_id": customer_id,
                "name": name,
                "message": f"Successfully authenticated as {name}",
            }))

        elif action == "subscribe_order":
            order_id = msg.get("order_id")
            if not order_id or int(order_id) not in self.orders:
                await websocket.send(json.dumps({
                    "type": "ERROR",
                    "message": f"Order {order_id} does not exist",
                }))
                return

            order_id = int(order_id)
            client_info["subscribed_orders"].add(order_id)
            logging.info(f"{client_info['name']} subscribed to Order #{order_id}")
            await websocket.send(json.dumps({
                "type": "SUBSCRIBED",
                "order_id": order_id,
                "current_status": self.orders[order_id]["status"],
                "message": f"Subscribed to real-time updates for Order #{order_id}",
            }))

        elif action == "get_order_status":
            order_id = msg.get("order_id")
            if not order_id or int(order_id) not in self.orders:
                await websocket.send(json.dumps({
                    "type": "ERROR",
                    "message": f"Order {order_id} not found",
                }))
                return

            order = self.orders[int(order_id)]
            await websocket.send(json.dumps({
                "type": "ORDER_STATUS_RESPONSE",
                "order_id": order["order_id"],
                "status": order["status"],
                "restaurant": order["restaurant"],
                "items": order["items"],
                "total_amount": order["total_amount"],
            }))

        elif action == "update_order_status":
            order_id = msg.get("order_id")
            new_status = msg.get("status")
            valid_statuses = ["CONFIRMED", "PREPARING", "READY", "DELIVERED", "CANCELLED"]

            if not order_id or int(order_id) not in self.orders:
                await websocket.send(json.dumps({"type": "ERROR", "message": f"Order {order_id} not found"}))
                return

            if new_status not in valid_statuses:
                await websocket.send(json.dumps({"type": "ERROR", "message": f"Status must be one of {valid_statuses}"}))
                return

            order_id = int(order_id)
            await self.broadcast_order_update(order_id, new_status)
            await websocket.send(json.dumps({
                "type": "UPDATE_SUCCESS",
                "order_id": order_id,
                "status": new_status,
            }))

        else:
            await websocket.send(json.dumps({
                "type": "ERROR",
                "message": f"Unknown action: '{action}'",
            }))

    async def handler(self, websocket):
        await self.register(websocket)
        try:
            async for message in websocket:
                await self.handle_message(websocket, message)
        except ConnectionClosed:
            pass
        finally:
            await self.unregister(websocket)

    async def run(self):
        logging.info(f"Starting Order WebSocket Server on ws://{self.host}:{self.port} ...")
        async with websockets.serve(self.handler, self.host, self.port):
            await asyncio.Future()


if __name__ == "__main__":
    server = OrderWebSocketServer()
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logging.info("WebSocket Server stopped gracefully.")
