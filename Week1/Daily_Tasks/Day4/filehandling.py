filename = "file.txt"

#writing a file
with open(filename,"w") as f:
    ch = input("Enter data for the file : ")
    f.write(ch)
    f.write(ch + "\n")

print("Data written")

#Read a file
print("Content of the file : ")
with open(filename , "r") as f:
    content = f.read()
    print(content)

#Append data to the file
with open(filename , "a") as f:
    ch = input("Enter data to append in the file : ")
    f.write(ch)
print("Conten writen to the file ")

#Read the updated file
print("Content of the file : ")
with open(filename , "r") as f:
    content = f.read()
    print(content)