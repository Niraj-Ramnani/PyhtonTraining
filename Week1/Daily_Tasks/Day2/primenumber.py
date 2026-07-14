def primenumber(num):
    if num <=1 :
        print("Given number is not a prime number ")
        return
    for i in range(2,int(num**0.5) + 1):
        if num %i == 0:
            print("Given number is not a prime number ")
            return
        
    print("Given number is  a prime number ")

num = int(input("Enter a number : "))
primenumber(num)