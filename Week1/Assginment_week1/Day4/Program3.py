#3. Write a Python program that prompts the user to enter their birthdate in the format 'YYYY-MM-DD' and validates the birthdate format using a regular expression and calculates their age if the format is correct and 'Invalid Format' otherwise.
import re
from datetime import datetime

try:
    birthdate = input("Enter your birthdate (YYYY-MM-DD): ")
    pattern = r"^\d{4}-\d{2}-\d{2}$"
    if re.fullmatch(pattern, birthdate):
        dob = datetime.strptime(birthdate, "%Y-%m-%d")
        today = datetime.today()
        age = today.year - dob.year
        print("Age : " , age)

    else:
        print("Invalid Format ")

except Exception as e:
    print("Error ",e)