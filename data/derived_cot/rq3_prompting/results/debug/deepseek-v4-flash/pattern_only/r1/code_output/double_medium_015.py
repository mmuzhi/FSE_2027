from typing import List

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        total = sum(nums)
        left_sum = 0
        ans = []

        for i, x in enumerate(nums):
            right_sum = total - left_sum - x
            ans.append(x * i - left_sum + right_sum - x * (n - i - 1))
            left_sum += x

        return ans