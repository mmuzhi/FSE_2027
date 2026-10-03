from typing import List
from collections import defaultdict

class Solution:
    def numberOfArithmeticSlices(self, nums: List[int]) -> int:
        total, n = 0, len(nums)
        dp = [defaultdict(int) for _ in nums]
        for i in range(1, n):
            for j in range(i):
                diff = nums[i] - nums[j]
                dp[i][diff] += dp[j][diff] + 1
                total += dp[j][diff]
        return total