# https://leetcode.com/problems/merge-two-sorted-lists/description/?utm_source=chatgpt.com
class Solution:
    def mergeTwoLists(self, list1, list2):

        dummy = ListNode(0)
        current = dummy

        while list1 and list2:

            if list1.val <= list2.val:
                current.next = list1
                list1 = list1.next
            else:
                current.next = list2
                list2 = list2.next

            current = current.next

        if list1:
            current.next = list1

        if list2:
            current.next = list2

        return dummy.next


#https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/
class Solution:
    def maxProfit(self, prices):
        min_price = float('inf')
        max_profit = 0

        for price in prices:
            if price < min_price:
                min_price = price
            else:
                max_profit = max(max_profit, price - min_price)

        return max_profit