#https://www.hackerrank.com/challenges/ginorts/problem
#String sorting 
s = input().strip()

evenlst = []
oddlst = []
upperlst = []
lowerlst = []

for ch in s:
    if ch.isdigit():
        if int(ch) % 2 == 0:
            evenlst.append(ch)
        else:
            oddlst.append(ch)
    elif ch.isupper():
        upperlst.append(ch)
    elif ch.islower():
        lowerlst.append(ch)


lowerlst.sort()
upperlst.sort()
oddlst.sort()
evenlst.sort()

print("".join(lowerlst + upperlst + oddlst + evenlst))

#https://leetcode.com/problems/remove-outermost-parentheses/description/
#Remove Outermost Parentheses
class Solution:
    def removeOuterParentheses(self, s: str) -> str:
        res = []
        check = 0
        
        for char in s:
            if char == '(':
               
                if check > 0:
                    res.append(char)
                check += 1
            else:  
                check -= 1
                if check > 0:
                    res.append(char)
                    
        return "".join(res)