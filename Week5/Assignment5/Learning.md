Build a performance comparison program for the Online Food Ordering System. Create a synchronous version that retrieves menus, customer order history, and payment information one after another, and an asynchronous version using async/await and an event loop. Run both versions with the same test data, measure execution time, and explain the difference between blocking and non-blocking I/O

```
import time
import asyncio
from db import get_db

LATENCY = 0.5


def get_menu_db(restaurant_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT food_item_id, name, price FROM Food_Items WHERE restaurant_id = %s",
            (restaurant_id,),
        )
        items = [dict(r) for r in cur.fetchall()]
    conn.close()
    return items


def get_order_history_db(customer_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            "SELECT order_id, order_status, total_amount, created_at FROM Orders WHERE user_id = %s",
            (customer_id,),
        )
        orders = [dict(r) for r in cur.fetchall()]
    conn.close()
    return orders


def get_payment_info_db(customer_id):
    conn = get_db()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT p.payment_id, p.order_id, p.amount, p.payment_method, p.payment_status
            FROM Payments p
            JOIN Orders o ON o.order_id = p.order_id
            WHERE o.user_id = %s
            """,
            (customer_id,),
        )
        payments = [dict(r) for r in cur.fetchall()]
    conn.close()
    return payments


def fetch_menu_sync(restaurant_id):
    time.sleep(LATENCY)
    return get_menu_db(restaurant_id)


def fetch_order_history_sync(customer_id):
    time.sleep(LATENCY)
    return get_order_history_db(customer_id)


def fetch_payment_info_sync(customer_id):
    time.sleep(LATENCY)
    return get_payment_info_db(customer_id)


def run_synchronous(customer_id, restaurant_id):
    start = time.perf_counter()
    menu = fetch_menu_sync(restaurant_id)
    orders = fetch_order_history_sync(customer_id)
    payments = fetch_payment_info_sync(customer_id)
    duration = time.perf_counter() - start
    return {"menu": menu, "orders": orders, "payments": payments}, duration


async def fetch_menu_async(restaurant_id):
    await asyncio.sleep(LATENCY)
    return await asyncio.to_thread(get_menu_db, restaurant_id)


async def fetch_order_history_async(customer_id):
    await asyncio.sleep(LATENCY)
    return await asyncio.to_thread(get_order_history_db, customer_id)


async def fetch_payment_info_async(customer_id):
    await asyncio.sleep(LATENCY)
    return await asyncio.to_thread(get_payment_info_db, customer_id)


async def run_asynchronous_tasks(customer_id, restaurant_id):
    start = time.perf_counter()
    menu, orders, payments = await asyncio.gather(
        fetch_menu_async(restaurant_id),
        fetch_order_history_async(customer_id),
        fetch_payment_info_async(customer_id),
    )
    duration = time.perf_counter() - start
    return {"menu": menu, "orders": orders, "payments": payments}, duration


def run_asynchronous(customer_id, restaurant_id):
    return asyncio.run(run_asynchronous_tasks(customer_id, restaurant_id))


def main():
    customer_id = 1
    restaurant_id = 1

    print("=" * 65)
    print("Online Food Ordering System - Performance Comparison")
    print(f"Test Data -> Customer ID: {customer_id}, Restaurant ID: {restaurant_id}")
    print("=" * 65)

    print("\n[1] Running Synchronous Version (Sequential / Blocking)...")
    sync_data, sync_time = run_synchronous(customer_id, restaurant_id)
    print(f"    Fetched {len(sync_data['menu'])} menu items, {len(sync_data['orders'])} orders, {len(sync_data['payments'])} payments.")
    print(f"    Execution Time: {sync_time:.4f} seconds")

    print("\n[2] Running Asynchronous Version (Concurrent / Non-Blocking)...")
    async_data, async_time = run_asynchronous(customer_id, restaurant_id)
    print(f"    Fetched {len(async_data['menu'])} menu items, {len(async_data['orders'])} orders, {len(async_data['payments'])} payments.")
    print(f"    Execution Time: {async_time:.4f} seconds")

    speedup = sync_time / async_time if async_time > 0 else 0
    print("\n" + "=" * 65)
    print("RESULTS & COMPARISON")
    print("=" * 65)
    print(f"Synchronous Total Time : {sync_time:.4f} s (Tasks executed sequentially)")
    print(f"Asynchronous Total Time: {async_time:.4f} s (Tasks executed concurrently)")
    print(f"Speedup Factor         : {speedup:.2f}x faster")
    print("=" * 65)

    print("\nBLOCKING vs NON-BLOCKING I/O EXPLANATION:")
    print("-" * 65)
    print("1. Blocking I/O (Synchronous):")
    print("   - The execution thread halts at each I/O request (DB query/network call).")
    print("   - Task 2 cannot start until Task 1 completely finishes.")
    print("   - Total Time = Time(Menu) + Time(Orders) + Time(Payments)")
    print("\n2. Non-Blocking I/O (Asynchronous):")
    print("   - Uses async/await with an event loop.")
    print("   - While one task is waiting on I/O, the event loop switches to execute other tasks.")
    print("   - Total Time = max(Time(Menu), Time(Orders), Time(Payments))")
    print("=" * 65)


if __name__ == "__main__":
    main()
```

```python
import asyncio
import httpx

TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}
TRANSIENT_EXCEPTIONS = (
    httpx.TimeoutException,
    httpx.ConnectError,
    httpx.ConnectTimeout,
    httpx.ReadTimeout,
    httpx.WriteTimeout,
    httpx.NetworkError,
)

async def fetch_with_retry(
    client: httpx.AsyncClient,
    url: str,
    max_retries: int = 3,
    backoff_factor: float = 0.5,
    timeout: float = 5.0,
):
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            response = await client.get(url, timeout=timeout)
            if response.status_code in TRANSIENT_STATUS_CODES:
                last_error = f"HTTP {response.status_code}: {response.text or 'Transient server error'}"
                if attempt < max_retries:
                    await asyncio.sleep(backoff_factor * (2 ** (attempt - 1)))
                    continue
                break
            
            response.raise_for_status()
            return {"success": True, "url": url, "data": response.json(), "attempts": attempt}

        except TRANSIENT_EXCEPTIONS as e:
            last_error = f"Network/Timeout error: {str(e) or type(e).__name__}"
            if attempt < max_retries:
                await asyncio.sleep(backoff_factor * (2 ** (attempt - 1)))
                continue
            break
        except httpx.HTTPStatusError as e:
            # Non-transient error (e.g. 400, 401, 403, 404) -> do not retry
            return {
                "success": False,
                "url": url,
                "error": f"Non-transient HTTP error {e.response.status_code}: {e.response.text}",
                "attempts": attempt,
                "is_transient": False,
            }
        except Exception as e:
            return {
                "success": False,
                "url": url,
                "error": f"Unexpected error: {str(e)}",
                "attempts": attempt,
                "is_transient": False,
            }

    return {
        "success": False,
        "url": url,
        "error": f"Request failed after {max_retries} attempts. Last error: {last_error}",
        "attempts": max_retries,
        "is_transient": True,
    }
```