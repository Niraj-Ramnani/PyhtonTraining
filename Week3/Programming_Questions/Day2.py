# https://leetcode.com/problems/valid-palindrome/?envType=problem-list-v2&envId=string
class Solution:
    def isPalindrome(self, s: str) -> bool:
        temp = ""
        for i  in s:
            if i.isalnum():
                temp += i.lower()
        rev = temp[::-1]
        return rev == temp
# https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/submissions/?envType=problem-list-v2&envId=string
class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        return haystack.find(needle)
        