from typing import List

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        total = sum(nums)
        prefix = 0
        ans = []

        for i, x in enumerate(nums):
            left = x * i - prefix
            right = (total - prefix - x) - x * (n - i - 1)
            ans.append(left + right)
            prefix += x

        return ans