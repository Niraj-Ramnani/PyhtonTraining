import asyncio
import json
import logging
import websockets
from websocket_server import OrderWebSocketServer
from websocket_client import OrderWebSocketClient

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def run_multi_client_demo():
    print("=" * 80)
    print("ONLINE FOOD ORDERING SYSTEM - WEBSOCKET SERVER & MULTI-CLIENT DEMO")
    print("=" * 80)

    server = OrderWebSocketServer(host="127.0.0.1", port=8765)
    server_task = await websockets.serve(server.handler, server.host, server.port)
    print(f"\n[1] WebSocket Server started on ws://{server.host}:{server.port}")

    client1 = OrderWebSocketClient(customer_id=1, name="Client_1_Aarav")
    client2 = OrderWebSocketClient(customer_id=2, name="Client_2_Diya")
    client3 = OrderWebSocketClient(customer_id=3, name="Client_3_Vihaan")

    print("\n[2] Connecting and Authenticating 3 Simultaneous Clients...")
    await client1.connect()
    await client2.connect()
    await client3.connect()

    print(f"-> Active clients in server registry: {len(server.clients)}")

    print("\n[3] Direct Order Status Retrieval over WebSocket (Without HTTP Request):")
    status_101 = await client1.get_order_status(101)
    print(f"    Client 1 queried Order #101 -> Status: {status_101.get('status')}, Restaurant: {status_101.get('restaurant')}, Items: {status_101.get('items')}")

    status_102 = await client2.get_order_status(102)
    print(f"    Client 2 queried Order #102 -> Status: {status_102.get('status')}, Restaurant: {status_102.get('restaurant')}, Items: {status_102.get('items')}")

    status_103 = await client3.get_order_status(103)
    print(f"    Client 3 queried Order #103 -> Status: {status_103.get('status')}, Restaurant: {status_103.get('restaurant')}, Items: {status_103.get('items')}")

    print("\n[4] Subscribing Clients to Live Order Feeds & Starting Background Listeners...")
    await client1.subscribe_order(101)
    await client2.subscribe_order(102)
    await client3.subscribe_order(101)
    await client3.subscribe_order(103)

    await client1.start_listening()
    await client2.start_listening()
    await client3.start_listening()

    print("\n[5] Broadcasting Order Status Transitions: CONFIRMED -> PREPARING -> READY -> DELIVERED")
    print("-" * 80)

    transitions = [
        (101, "CONFIRMED"),
        (102, "CONFIRMED"),
        (101, "PREPARING"),
        (103, "CONFIRMED"),
        (101, "READY"),
        (102, "PREPARING"),
        (101, "DELIVERED"),
    ]

    for order_id, new_status in transitions:
        await asyncio.sleep(0.3)
        await server.broadcast_order_update(order_id, new_status)

    await asyncio.sleep(0.5)

    print("\n[6] Demonstrating Graceful Disconnection & Connection Registry Cleanup...")
    print(f"-> Before disconnect: {len(server.clients)} active clients")
    await client2.close()
    await asyncio.sleep(0.2)
    print(f"-> After Client 2 (Diya) disconnect: {len(server.clients)} active clients in server registry")

    print("\n[7] Broadcasting Post-Disconnection Update (Order #103 -> PREPARING & READY)...")
    await server.broadcast_order_update(103, "PREPARING")
    await asyncio.sleep(0.2)
    await server.broadcast_order_update(103, "READY")
    await asyncio.sleep(0.3)

    print("\n[8] Demonstrating Error Handling:")
    try:
        ws_test = await websockets.connect("ws://127.0.0.1:8765")
        await ws_test.send("not-valid-json")
        err_res1 = json.loads(await ws_test.recv())
        print(f"    Malformed JSON Payload Error: {err_res1}")

        await ws_test.send(json.dumps({"action": "get_order_status", "order_id": 99999}))
        err_res2 = json.loads(await ws_test.recv())
        print(f"    Non-Existent Order Query Error: {err_res2}")

        await ws_test.send(json.dumps({"action": "unknown_action"}))
        err_res3 = json.loads(await ws_test.recv())
        print(f"    Unknown Action Error: {err_res3}")

        await ws_test.close()
    except Exception as e:
        print(f"Error test exception: {e}")

    print("\n[9] Summary of Updates Received by Connected Clients:")
    print(f"    Client 1 (Aarav) received {len(client1.received_updates)} live status updates for Order #101.")
    print(f"    Client 2 (Diya) received {len(client2.received_updates)} live status updates before disconnecting.")
    print(f"    Client 3 (Vihaan) received {len(client3.received_updates)} live status updates across Orders #101 and #103.")

    await client1.close()
    await client3.close()
    server_task.close()
    await server_task.wait_closed()

    print("\n" + "=" * 80)
    print("ALL WEBSOCKET TESTS & DEMONSTRATIONS COMPLETED SUCCESSFULLY")
    print("=" * 80)


if __name__ == "__main__":
    asyncio.run(run_multi_client_demo())
