class Solution:
    def minCosts(self, cost: List[int]) -> List[int]:
        n = len(cost)
        dp = [float('inf')] * (n + 1)
        dp[n] = 0