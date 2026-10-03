from typing import List

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        total = sum(nums)
        left_sum = 0
        result = [0] * n

        for i in range(n):
            right_sum = total - left_sum - nums[i]
            left_diff = nums[i] * i - left_sum
            right_diff = right_sum - nums[i] * (n - i - 1)
            result[i] = left_diff + right_diff
            left_sum += nums[i]

        return result