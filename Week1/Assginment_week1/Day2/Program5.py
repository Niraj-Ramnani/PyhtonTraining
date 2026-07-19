# 5. Develop a Python script that takes user input and writes it to a new text file
try:
    text = input("Enter text : ")
    with open("file.txt" , "w") as file:
        file.write(text)
    print("Data Written to file ")

except Exception as e:
    print("Error : ",e)