import asyncio
import time
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


class AsyncFoodOrderingClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:5000",
        default_timeout: float = 3.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self.base_url = base_url.rstrip("/")
        self.default_timeout = default_timeout
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor
        self.transport = transport

    async def get_with_retry(
        self,
        client: httpx.AsyncClient,
        endpoint: str,
        timeout: float | None = None,
        max_retries: int | None = None,
    ) -> dict:
        url = endpoint if endpoint.startswith("http") else f"{self.base_url}{endpoint}"
        retries = max_retries if max_retries is not None else self.max_retries
        request_timeout = timeout if timeout is not None else self.default_timeout

        last_error_detail = None

        for attempt in range(1, retries + 1):
            try:
                response = await client.get(url, timeout=request_timeout)

                if response.status_code in TRANSIENT_STATUS_CODES:
                    last_error_detail = f"HTTP {response.status_code} (Transient Server Error)"
                    if attempt < retries:
                        delay = self.backoff_factor * (2 ** (attempt - 1))
                        await asyncio.sleep(delay)
                        continue
                    break

                if 400 <= response.status_code < 500 and response.status_code != 429:
                    return {
                        "endpoint": endpoint,
                        "success": False,
                        "attempts": attempt,
                        "status_code": response.status_code,
                        "error": f"Non-transient client error HTTP {response.status_code} (not retried): {response.text}",
                    }

                response.raise_for_status()
                return {
                    "endpoint": endpoint,
                    "success": True,
                    "attempts": attempt,
                    "status_code": response.status_code,
                    "data": response.json(),
                }

            except TRANSIENT_EXCEPTIONS as exc:
                last_error_detail = f"{type(exc).__name__}: {str(exc) or 'Connection/Timeout issue'}"
                if attempt < retries:
                    delay = self.backoff_factor * (2 ** (attempt - 1))
                    await asyncio.sleep(delay)
                    continue
                break
            except Exception as exc:
                return {
                    "endpoint": endpoint,
                    "success": False,
                    "attempts": attempt,
                    "status_code": None,
                    "error": f"Fatal non-transient exception: {str(exc)}",
                }

        return {
            "endpoint": endpoint,
            "success": False,
            "attempts": retries,
            "status_code": None,
            "error": f"Request failed after {retries} retries. Reason: {last_error_detail}",
        }

    async def fetch_order_dashboard(
        self,
        restaurant_id: int = 1,
        payment_order_id: int = 1,
    ) -> dict:
        endpoints = {
            "restaurant_info": f"/api/restaurants/{restaurant_id}",
            "menu_info": f"/api/food-items?restaurant_id={restaurant_id}",
            "payment_status": f"/api/payments/status/{payment_order_id}",
        }

        async with httpx.AsyncClient(transport=self.transport) as client:
            start_time = time.perf_counter()
            results = await asyncio.gather(
                self.get_with_retry(client, endpoints["restaurant_info"]),
                self.get_with_retry(client, endpoints["menu_info"]),
                self.get_with_retry(client, endpoints["payment_status"]),
                return_exceptions=False,
            )
            elapsed = time.perf_counter() - start_time

        return {
            "total_elapsed_seconds": round(elapsed, 4),
            "restaurant": results[0],
            "menu": results[1],
            "payment": results[2],
        }


def create_mock_transport():
    attempt_tracker = {"retry_endpoint": 0}

    async def mock_handler(request: httpx.Request) -> httpx.Response:
        path = request.url.path

        if "/api/restaurants/" in path:
            await asyncio.sleep(0.1)
            return httpx.Response(200, json={"restaurant_id": 1, "name": "Spice Villa", "address": "MI Road, Jaipur", "rating": 4.5})

        elif "/api/food-items" in path:
            await asyncio.sleep(0.1)
            return httpx.Response(200, json=[
                {"food_item_id": 1, "name": "Paneer Tikka", "price": 220.0},
                {"food_item_id": 2, "name": "Butter Chicken", "price": 340.0},
                {"food_item_id": 3, "name": "Gulab Jamun", "price": 90.0},
            ])

        elif "/api/payments/status/" in path:
            await asyncio.sleep(0.1)
            return httpx.Response(200, json={"payment_id": 1, "order_id": 1, "payment_method": "upi", "payment_status": "completed", "amount": 650.0})

        elif "/api/flaky-service" in path:
            attempt_tracker["retry_endpoint"] += 1
            if attempt_tracker["retry_endpoint"] < 2:
                return httpx.Response(503, text="Service Temporarily Unavailable (Transient)")
            return httpx.Response(200, json={"message": "Recovered successfully after transient failure on attempt 2!"})

        elif "/api/down-service" in path:
            return httpx.Response(504, text="Gateway Timeout (Transient Failure)")

        elif "/api/invalid-resource" in path:
            return httpx.Response(404, json={"error": "Resource Not Found (Non-transient)"})

        return httpx.Response(404, json={"error": "Unknown path"})

    return httpx.MockTransport(mock_handler)


async def run_demonstration():
    mock_transport = create_mock_transport()
    service = AsyncFoodOrderingClient(
        base_url="http://127.0.0.1:5000",
        default_timeout=2.0,
        max_retries=3,
        backoff_factor=0.1,
        transport=mock_transport,
    )

    print("=" * 70)
    print("ASYNCHRONOUS HTTP CLIENT (httpx) WITH CONCURRENCY & RETRIES")
    print("=" * 70)

    print("\n[Scenario 1] Concurrent Retrieval of 3 Endpoints (Restaurant, Menu, Payment):")
    dashboard = await service.fetch_order_dashboard(restaurant_id=1, payment_order_id=1)
    print(f"-> Total concurrent execution time: {dashboard['total_elapsed_seconds']}s")
    for key in ["restaurant", "menu", "payment"]:
        item = dashboard[key]
        print(f"   [{key.upper()}] Endpoint: {item['endpoint']} | Status: {item['status_code']} | Attempts: {item['attempts']}")
        print(f"     Data: {item['data']}")

    print("\n[Scenario 2] Transient Failure (503 Service Unavailable) -> Auto-Retry & Recovery:")
    async with httpx.AsyncClient(transport=mock_transport) as client:
        res = await service.get_with_retry(client, "/api/flaky-service", max_retries=3)
        print(f"   Endpoint: {res['endpoint']} | Success: {res['success']} | Total Attempts: {res['attempts']}")
        print(f"   Result: {res.get('data') or res.get('error')}")

    print("\n[Scenario 3] Persistent Transient Failure (504 Gateway Timeout) -> Stops After Max Retries:")
    async with httpx.AsyncClient(transport=mock_transport) as client:
        res = await service.get_with_retry(client, "/api/down-service", max_retries=3)
        print(f"   Endpoint: {res['endpoint']} | Success: {res['success']} | Total Attempts: {res['attempts']}")
        print(f"   Meaningful Error: {res['error']}")

    print("\n[Scenario 4] Non-Transient Failure (404 Not Found) -> Immediate Stop (Zero Retries):")
    async with httpx.AsyncClient(transport=mock_transport) as client:
        res = await service.get_with_retry(client, "/api/invalid-resource", max_retries=3)
        print(f"   Endpoint: {res['endpoint']} | Success: {res['success']} | Total Attempts: {res['attempts']}")
        print(f"   Error: {res['error']}")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETED SUCCESSFULLY")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(run_demonstration())
