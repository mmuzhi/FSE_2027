class Solution:
    def validPartition(self, nums: List[int]) -> bool:
        n = len(nums)
        if n < 2:
            return False
        dp = [False] * n
        if n >= 2:
            dp[1] = (nums[0] == nums[1])
        if n >= 3:
            dp[2] = (nums[0] + 1 == nums[1] and nums[1] + 1 == nums[2])
        for i in range(3, n):
            if (dp[i-2] and (nums[i-2] == nums[i-1])) or (dp[i-3] and (nums[i-3] + 1 == nums[i-2] and nums[i-2] + 1 == nums[i-1])):
                dp[i] = True
        return dp[-1] if n >= 1 else False