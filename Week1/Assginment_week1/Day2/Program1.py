# 1. Write a Python program that counts the occurrences of each character in a given string.
try:
    txt = input("Enter text : ")
    count = {}

    for char in txt:
        if char in count:
            count[char] += 1
        else:
            count[char] = 1

    print("Occurence of characters : ")
    for k,v in count.items():
        print(f"{k} : {v}")
    
except Exception as e :
    print("error : ",e)