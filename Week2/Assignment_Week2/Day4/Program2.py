# 2. Create a generator that yields prime numbers up to a specified limit.
def prime_number_generator(limit):
    for i in range (2,limit + 1):
        is_prime = True
        for j in range (2,int(i**0.5) +1):
            if i % j == 0:
                is_prime = False
                break
        if is_prime:
            yield i

def main():
    try:
        limit = int(input("Enter limit : "))
        print("Prime number in this range are : ")
        for i in prime_number_generator(limit):
            print(i)
    except Exception as e:
        print("Error : ",e)

if __name__ == "__main__":
    main()