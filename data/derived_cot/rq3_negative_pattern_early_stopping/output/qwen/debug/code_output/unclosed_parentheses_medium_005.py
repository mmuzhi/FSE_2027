class Solution:
    def validPartition(self, nums: List[int]) -> bool:
        n = len(nums)
        # dp[i] is True if the prefix nums[0..i-1] can be partitioned
        dp = [False] * (n+1)
        dp[0] = True  # base case: empty prefix is valid

        for i in range(1, n):
            # Option 1: last two elements form a two-element segment
            if i >= 1 and nums[i] == nums[i-1]:
                dp[i+1] = dp[i+1] or dp[i-1]
            # Option 2: last three elements form a three-element segment (consecutive numbers)
            if i >= 2 and nums[i] == nums[i-1] + 1 and nums[i-1] == nums[i-2] + 1:
                dp[i+1] = dp[i+1] or dp[i-2]

        return dp[n]