# 2. Write a program that takes user input for age as a string, converts it to an integer, and checks if the user is eligible to vote.
try:
    age = input("Enter age : ")
    age = int(age)

    if age>=18:
        print("Eligible to vote")

    else:
        print("Not Eligible to vote")

except ValueError:
    print("Enter a valid number ")

except Exception as e:
    print("Error : ",e)
