| Feature | Asyncio | Threading | Multiprocessing |
| --- | --- | --- | --- |
| Concurrency | Yes | Yes | Yes |
| Parallel CPU execution | No, typically single event-loop thread | Limited by GIL for Python bytecode | Yes |
| Best for | I/O-bound async work | I/O-bound blocking work | CPU-bound work |
| Memory | Shared process memory | Shared process memory | Separate process memory |
| Overhead | Low | Moderate | Higher |
| Communication | Coroutines/tasks | Shared memory/synchronization | IPC/pipes/queues/etc. |
| Typical use | APIs, WebSockets | Blocking libraries | CPU-heavy processing |

## Async HTTP Call

To make asynchronous HTTP calls in Python, standard libraries like `requests` will not work because they are **synchronous/blocking** (they halt the entire event loop). Instead, use dedicated async HTTP clients like `httpx`

- `httpx.AsyncClient()`**:** Manages connection pooling and keeps TCP connections alive for reuse across requests.
- `await client.get(url)`**:** When the network request is fired, execution pauses on that specific coroutine without blocking the thread. The single-threaded **Event Loop** immediately switches to fire off the next requests.

## Timeout :

A timeout is the maximum amount of time we allow an operation to take before treating it as failed.

```
import asyncio
import httpx


async def fetch_data():
    timeout = httpx.Timeout(5.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(
            "https://jsonplaceholder.typicode.com/users"
        )

        response.raise_for_status()

        return response.json()


asyncio.run(fetch_data())
```

## Retries

A retry is an additional attempt to perform an operation after a failure, subject to defined limits and rules.

# Exponential Backoff

A common retry strategy is **exponential backoff**.

Instead of:

we increase the waiting time:

```
Attempt 1 fails -> wait 1 sec
```

Attempt 2 fails -&gt; wait 2 sec

Attempt 3 fails -&gt; wait 4 sec

Attempt 4 fails -&gt; wait 8 sec

Simple implementation:

```
delay = 2 ** attempt
await asyncio.sleep(delay)
```

## asyncio.wait()

```
task1 = asyncio.create_task(get_user())
task2 = asyncio.create_task(get_orders())

done, pending = await asyncio.wait(
    [task1, task2]
)
```