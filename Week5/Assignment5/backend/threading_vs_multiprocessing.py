import time
import os
import math
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor


def io_bound_task(order_id: int) -> dict:
    time.sleep(0.1)
    return {"order_id": order_id, "status": "invoice_generated", "receipt_size_kb": 128}


def cpu_bound_task(batch_id: int, iterations: int = 4_000_000) -> dict:
    total = 0.0
    for i in range(1, iterations + 1):
        total += math.sqrt(i) * math.sin(i)
    return {"batch_id": batch_id, "result": round(total, 4)}


def run_io_sequential(order_ids: list[int]):
    start = time.perf_counter()
    results = [io_bound_task(oid) for oid in order_ids]
    return results, time.perf_counter() - start


def run_io_threading(order_ids: list[int], max_workers: int = 8):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(io_bound_task, order_ids))
    return results, time.perf_counter() - start


def run_io_multiprocessing(order_ids: list[int], max_workers: int = 8):
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(io_bound_task, order_ids))
    return results, time.perf_counter() - start


def run_cpu_sequential(batches: list[int]):
    start = time.perf_counter()
    results = [cpu_bound_task(b) for b in batches]
    return results, time.perf_counter() - start


def run_cpu_threading(batches: list[int], max_workers: int = 4):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(cpu_bound_task, batches))
    return results, time.perf_counter() - start


def run_cpu_multiprocessing(batches: list[int], max_workers: int = 4):
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(cpu_bound_task, batches))
    return results, time.perf_counter() - start


def main():
    cpu_cores = os.cpu_count() or 4
    print("=" * 75)
    print("Online Food Ordering System - Concurrency Benchmark")
    print(f"System CPU Cores Detected: {cpu_cores}")
    print("=" * 75)

    order_ids = list(range(1, 21))
    print(f"\n[PART 1] I/O-BOUND WORKLOAD: Exporting Invoices for {len(order_ids)} Orders (0.1s simulated I/O each)")
    print("-" * 75)

    _, io_seq_time = run_io_sequential(order_ids)
    print(f"1. Sequential Execution    : {io_seq_time:.4f} s")

    _, io_thread_time = run_io_threading(order_ids, max_workers=8)
    print(f"2. ThreadPoolExecutor (8)  : {io_thread_time:.4f} s  (Speedup: {io_seq_time / io_thread_time:.2f}x)")

    _, io_proc_time = run_io_multiprocessing(order_ids, max_workers=8)
    print(f"3. ProcessPoolExecutor (8) : {io_proc_time:.4f} s  (Speedup: {io_seq_time / io_proc_time:.2f}x)")

    batches = [1, 2, 3, 4]
    print(f"\n[PART 2] CPU-BOUND WORKLOAD: Large Order Analytics & Sales Forecast ({len(batches)} batches of 4M calculations)")
    print("-" * 75)

    _, cpu_seq_time = run_cpu_sequential(batches)
    print(f"1. Sequential Execution    : {cpu_seq_time:.4f} s")

    _, cpu_thread_time = run_cpu_threading(batches, max_workers=4)
    print(f"2. ThreadPoolExecutor (4)  : {cpu_thread_time:.4f} s  (Speedup: {cpu_seq_time / cpu_thread_time:.2f}x - Limited by GIL)")

    _, cpu_proc_time = run_cpu_multiprocessing(batches, max_workers=4)
    print(f"3. ProcessPoolExecutor (4) : {cpu_proc_time:.4f} s  (Speedup: {cpu_seq_time / cpu_proc_time:.2f}x - True Parallelism)")

    print("\n" + "=" * 75)
    print("SUMMARY & CONCURRENCY MODEL COMPARISON")
    print("=" * 75)
    print(f"{'Workload Type':<16} | {'Sequential':<12} | {'Threading':<12} | {'Multiprocessing':<16} | {'Best Model'}")
    print("-" * 75)
    print(f"{'I/O-Bound':<16} | {io_seq_time:>9.4f} s | {io_thread_time:>9.4f} s | {io_proc_time:>13.4f} s | Threading / Async")
    print(f"{'CPU-Bound':<16} | {cpu_seq_time:>9.4f} s | {cpu_thread_time:>9.4f} s | {cpu_proc_time:>13.4f} s | Multiprocessing")
    print("=" * 75)

    print("\nWHY EACH CONCURRENCY MODEL IS APPROPRIATE FOR ITS WORKLOAD:")
    print("-" * 75)
    print("1. Threading for I/O-Bound Tasks:")
    print("   - When a thread waits for I/O (network, file, database), it releases the GIL.")
    print("   - Other threads can immediately run, overlapping idle wait times.")
    print("   - Threads share memory space and have minimal creation/context-switch overhead.")
    print("\n2. Multiprocessing for CPU-Bound Tasks:")
    print("   - Python's Global Interpreter Lock (GIL) allows only one thread to execute Python bytecode at a time.")
    print("   - Multiprocessing spawns separate Python processes, each with its own interpreter and memory space.")
    print("   - This bypasses the GIL and distributes heavy computation across multiple CPU cores simultaneously.")
    print("=" * 75)


if __name__ == "__main__":
    main()
