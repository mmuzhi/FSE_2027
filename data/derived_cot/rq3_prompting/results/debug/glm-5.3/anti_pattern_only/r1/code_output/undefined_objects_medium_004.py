class Solution:
    def minIncrements(self, n: int, cost: List[int]) -> int:
        ans = 0
        n //= 2
        for i in reversed(range(n)):
            mn, mx = sorted((cost[2 * i + 1], cost[2 * i + 2]))
            ans += mx - mn
            cost[i] += mx
        return ans