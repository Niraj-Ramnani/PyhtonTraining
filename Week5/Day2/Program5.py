from multiprocessing import Process
import time

def worker(name):
    print(f"{name} started")
    total = 0
    for i in range(10_000_000):
        total += i
    print(f"{name} finished")

if __name__ == '__main__':
    p1 = Process(target=worker, args=("Process 1",))
    p2 = Process(target=worker, args=("Process 2",))

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("All processes finished")