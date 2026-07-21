def fibonacci(n):
    a, b = 0, 1
    count = 0

    while count < n:
        yield a
        a, b = b, a + b
        count += 1


n = int(input("Enter number of terms: "))

print("Fibonacci Series:")
for num in fibonacci(n):
    print(num, end=" ")