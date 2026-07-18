try:
    num = [1,2,3,4,5]

    print("list is : ",num)

    num.append(10)
    print("after appending : ",num)

    num.remove(4)
    print("after removing : ",num)

    temp = int(input("Enter element to search "))
    if temp in num:
        print(f"{temp} is present")
    else:
        print(f"{temp} is not present")

except Exception as e:
    print("error occured ")