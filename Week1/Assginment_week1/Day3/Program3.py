# 3. Write a one-liner Python program that uses lambda, map, and apply to transform a list of integers by adding 10 to each element and then squaring the result
try:
    lst = [1,2,3,4,5]
    res = list(map(lambda x : (x+10)**2 , lst))
    print(res)

except Exception as e:
    print("Error : ",e)