# 58. Length of Last Word
# https://leetcode.com/problems/length-of-last-word/description/?envType=problem-list-v2&envId=string
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        s = s.rstrip()
        space = 0
        for i in s :
            if i == " " :
                space +=1
        if space == 0:
            return len(s)
        temp = 0
        ans = 0
        for i in s:
            if i == " ":
                temp += 1
            if temp == space:
                ans += 1
            
        return ans-1

# Better approach
class Solution:
    def lengthOfLastWord(self, s: str) -> int:
        return len(s.split()[-1])