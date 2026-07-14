def armstrong(num):
    org = num
    temp = 0
    count = len(str(num))
    while num >0:
        digit = num % 10
        temp += digit ** count
        num //=10
    if org == temp:
        print("Given number is Armstrong Number")
    else:
        print("Not a Armstrong Number")

#---Main Program---#

num = int(input("Enter a number : "))
armstrong(num)