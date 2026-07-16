# Even numbers generator
def even_numbers(limit):
    for i in range(2, limit + 1, 2):
        yield i

gen = even_numbers(10)

for num in gen:
    print(num)

#Genrator using next
def numbers():
    yield "One"
    yield "Two"
    yield "Three"

gen = numbers()

print(next(gen))
print(next(gen))
print(next(gen))
