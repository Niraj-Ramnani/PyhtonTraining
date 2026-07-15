#Fibonaci series
#link : https://leetcode.com/problems/fibonacci-number/
def fib(self, n):
    if n <= 1:
        return n
    return self.fib(n - 1) + self.fib(n - 2)


# merge sort
# link : https://www.geeksforgeeks.org/problems/merge-sort/1

class Solution:
    def merge(self, arr, l, m, h):
        temp = []
        left = l
        right = m + 1

     
        while left <= m and right <= h:
            if arr[left] <= arr[right]:
                temp.append(arr[left])
                left += 1
            else:
                temp.append(arr[right])
                right += 1

        while left <= m:
            temp.append(arr[left])
            left += 1

       
        while right <= h:
            temp.append(arr[right])
            right += 1

        
        for i in range(l, h + 1):
            arr[i] = temp[i - l]

    def mergeSort(self, arr, l, h):
        if l >= h:
            return

        m = (l + h) // 2

        self.mergeSort(arr, l, m)
        self.mergeSort(arr, m + 1, h)
        self.merge(arr, l, m, h)