try:
    text = input("Enter text : ")
    with open("file.txt" , "w") as file:
        file.write(text)
    print("Data Written to file ")

except Exception as e:
    print("Error : ",e)