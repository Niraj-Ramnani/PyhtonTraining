# 3. Write a program that asks the user to input a password. Check if the password meets the criteria
import string

password = input("Enter the password : ")
has_minlen = len(password) >=8
has_number = any(char.isdigit() for char in password)
has_special = any(char in string.punctuation for char in password)

if has_minlen and has_number and has_special:
    print("Valid Password")
else:
    print("Invalid Password")
    if not has_minlen:
        print("Password should be more than 8 characters ")
    elif not has_number:
        print("Password should have a numeric value")
    else:
        print("Password should have a special character ")