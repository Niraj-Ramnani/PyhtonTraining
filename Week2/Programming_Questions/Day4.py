# https://leetcode.com/problems/binary-search/description/
class Solution:
    def search(self, nums, target):
        left, right = 0, len(nums) - 1

        while left <= right:
            mid = (left + right) // 2

            if nums[mid] == target:
                return mid
            elif nums[mid] < target:
                left = mid + 1
            else:
                right = mid - 1

        return -1

#https://leetcode.com/problems/move-zeroes/description/
class Solution:
    def moveZeroes(self, nums):
        j = 0

        for i in range(len(nums)):
            if nums[i] != 0:
                nums[j], nums[i] = nums[i], nums[j]
                j += 1