class Solution:
    def minIncrements(self, n: int, cost: List[int]) -> int:
        ans = 0
        for i in range(n // 2 - 1, -1, -1):
            left = cost[2 * i + 1]
            right = cost[2 * i + 2]
            ans += abs(left - right)
            cost[i] += max(left, right)
        return ans