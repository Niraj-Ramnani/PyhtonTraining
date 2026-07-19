# 4. Write a Python program that reads a CSV file named 'data.csv' containing information about students (columns: Name, Age, Grade). The program should read the CSV file, convert CSV into JSON format, and send the JSON data to a specific API endpoint using the requests library.
import csv
import json
import requests

try:
    students = []
    with open("test.csv" , "r") as file :
        reader = csv.DictReader(file)

        for row in reader:
            students.append(row)
    json_data = json.dumps(students, indent=4)
    print("JSON Data:")
    print(json_data)
    url = "https://httpbin.org/post"
    response = requests.post(
        url,
        headers={"Content-Type": "application/json"},
        data=json_data
    )

    print("\nStatus Code:", response.status_code)

    if response.status_code == 200:
        print("JSON sent successfully.")
    else:
        print("Failed to send data.")

except Exception as e:
    print("Error : ",e)
