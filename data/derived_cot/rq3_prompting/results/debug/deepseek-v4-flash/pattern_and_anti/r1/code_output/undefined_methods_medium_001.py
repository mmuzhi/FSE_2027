from typing import List

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        total = sum(nums)
        left_sum = 0
        right_sum = total
        ans = []

        for i, x in enumerate(nums):
            ans.append(x * i - left_sum + (right_sum - x) - x * (n - i - 1))
            left_sum += x
            right_sum -= x

        return ans