from typing import List

class Solution:
    def getSumAbsoluteDifferences(self, nums: List[int]) -> List[int]:
        n = len(nums)
        total = sum(nums)
        left_sum = 0
        ans = []
        for i in range(n):
            right_sum = total - left_sum - nums[i]
            ans.append(i * nums[i] - left_sum + right_sum - (n - 1 - i) * nums[i])
            left_sum += nums[i]
        return ans