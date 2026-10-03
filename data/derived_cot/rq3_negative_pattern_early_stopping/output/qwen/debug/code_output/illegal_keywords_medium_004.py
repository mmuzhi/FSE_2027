from typing import List

class Solution:
    def minimumDeletions(self, nums: List[int]) -> int:
        n = len(nums)
        if n <= 1:
            return 0
        
        # Create a DP array where dp[i] is the length of the longest non-decreasing subsequence ending at i
        dp = [1] * n
        for i in range(n):
            for j in range(i):
                if nums[i] >= nums[j]:
                    dp[i] = max(dp[i], dp[j] + 1)
        
        longest = max(dp)
        return n - longest