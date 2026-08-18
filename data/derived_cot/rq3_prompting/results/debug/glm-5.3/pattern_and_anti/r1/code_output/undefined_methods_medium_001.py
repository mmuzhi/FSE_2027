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
        # s1 = sum of nums[0..i-1], s2 = sum of nums[i..n-1] (includes num itself)
        left = num * i - s1
        right = (s2 - num) - num * (n - i - 1)
        return left + right