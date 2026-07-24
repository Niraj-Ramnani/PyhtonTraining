#  https://leetcode.com/problems/kth-largest-element-in-an-array/description/
import heapq

class Solution:
    def findKthLargest(self, nums, k):
        return heapq.nlargest(k, nums)[-1]

# https://leetcode.com/problems/top-k-frequent-elements/description/

from collections import Counter

class Solution:
    def topKFrequent(self, nums, k):
        count = Counter(nums)
        return [x for x, _ in count.most_common(k)]