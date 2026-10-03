class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        ans = float('inf')
        for bc in baseCosts:
            x = target - bc
            if x < 0:
                candidate = bc
            else:
                n = 2 * x + 1
                dp = [False] * n
                dp[0] = True
                for cost in toppingCosts:
                    for j in range(cost, n):
                        if dp[j-cost]:
                            dp[j] = True
                best_diff = float('inf')
                best_sum = 0
                for j in range(n):
                    if dp[j]:
                        diff = abs(j - x)
                        if diff < best_diff:
                            best_diff = diff
                            best_sum = j
                        elif diff == best_diff and j < best_sum:
                            best_sum = j
                candidate = bc + best_sum
            if abs(candidate - target) < abs(ans - target):
                ans = candidate
            elif abs(candidate - target) == abs(ans - target) and candidate < ans:
                ans = candidate
        return ans
