def palindrome(num):
    org = num 
    reverse = 0
    while num > 0:
        digit = num %10
        reverse = reverse * 10 + digit
        num //=10
    if(org == reverse):
        print("palindrome number ")
    else:
        print("Not a plaindrome")

#---main program---#

num = int(input("enter a number : "))
palindrome(num)