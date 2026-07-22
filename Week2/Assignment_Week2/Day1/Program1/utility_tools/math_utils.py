from math import gcd

def greatest_common_divisor(a,b):
    return gcd(a,b)

def least_common_multiple(a,b):
    if a == 0 or b == 0:
        return 0
    return abs(a*b)//gcd(a,b)
