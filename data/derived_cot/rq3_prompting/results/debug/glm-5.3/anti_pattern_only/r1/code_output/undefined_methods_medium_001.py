from typing import List

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:

        n = len(nums)
        total = sum(nums)
        s1 = 0
        s2 = total
        arr = []
        for i in range(n):
            arr.append(self.calculateAbsoluteDifference(s1, nums[i], i, s2, n))
            s1 = s1 + nums[i]
            s2 = total - s1

        return arr

    def calculateAbsoluteDifference(self, s1, num, i, s2, n):
        # s1 = sum of elements before index i
        # s2 = sum of elements from index i to the end
        left = num * i - s1
        right = s2 - num * (n - i)
        return left + right