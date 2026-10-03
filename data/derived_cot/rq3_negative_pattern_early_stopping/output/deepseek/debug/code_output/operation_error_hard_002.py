from typing import List
from collections import defaultdict, Counter

class Solution:
    def numberOfArithmeticSlices(self, nums: List[int]) -> int:
        n = len(nums)
        ans = 0
        dp = defaultdict(Counter)
        for i in range(1, n):
            for j in range(i):
                d = nums[i] - nums[j]
                cnt = dp[j][d]
                ans += cnt
                dp[i][d] += cnt + 1
        return ans