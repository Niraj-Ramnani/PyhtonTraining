from utility_tools.math_utils import greatest_common_divisor, least_common_multiple
from utility_tools.string_utils import reverse_words, count_vowels
from utility_tools.validation import validate_email, validate_phone_number


print("--- Math Utility---")
a,b = map(int,input("Enter two number : ").split())
print("GCD : " , greatest_common_divisor(a,b))

a,b = map(int,input("Enter two number : ").split())
print("LCM : " , least_common_multiple(a,b))

print("--- String Utility---")
txt = input("Enter text : ")
print("Original : ",txt)
print("Reversed : ",reverse_words(txt))
print("Vowel Count : ",count_vowels(txt))

print("--- Validation Utility---")
email = input("Enter email : ")
mobile = input("Enter mobile number : ")

print("Email Valid : ",validate_email(email))
print("Mobile Valid : ",validate_phone_number(mobile))