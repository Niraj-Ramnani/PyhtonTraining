# https://leetcode.com/problems/contiguous-array/submissions/2086040069/?envType=problem-list-v2&envId=array
class Solution:
    def findMaxLength(self, nums: List[int]) -> int:
        first = {0: -1}
        count = 0
        ans = 0

        for i, num in enumerate(nums):
            if num == 1:
                count += 1
            else:
                count -= 1

            if count in first:
                ans = max(ans, i - first[count])
            else:
                first[count] = i

        return ans
# https://leetcode.com/problems/missing-number/?envType=problem-list-v2&envId=array
class Solution:
    def missingNumber(self, nums: List[int]) -> int:
        maxi = len(nums) +1
        for i in range(maxi):
            if i not in nums:
                return i

        