#Array Rotation
#https://www.hackerrank.com/challenges/array-left-rotation/problem?isFullScreen=true
def rotateLeft(d, arr):
    # Write your code here
    temp1 = arr[0:d]
    temp2 = arr[d:]
    temp2.extend(temp1)
    return temp2

#2 Sum
#https://leetcode.com/problems/two-sum/
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        num_to_index = {}
        for i, num in enumerate(nums):
            complement = target - num
            if complement in num_to_index:
                return [num_to_index[complement], i]
            num_to_index[num] = i

