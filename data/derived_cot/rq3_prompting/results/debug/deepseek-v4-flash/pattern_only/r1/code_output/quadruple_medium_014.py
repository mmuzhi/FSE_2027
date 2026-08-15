from typing import List
from functools import lru_cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        @lru_cache(None)
        def dfs(i: int, x: int) -> int:
            if i == len(toppingCosts) or x <= 0:
                return 0

            best = dfs(i + 1, x)
            for k in (1, 2):
                cand = k * toppingCosts[i] + dfs(i + 1, x - k * toppingCosts[i])
                if abs(cand - x) < abs(best - x) or (abs(cand - x) == abs(best - x) and cand < best):
                    best = cand
            return best

        ans = float('inf')
        for base in baseCosts:
            total = base + dfs(0, target - base)
            if abs(total - target) < abs(ans - target) or (abs(total - target) == abs(ans - target) and total < ans):
                ans = total

        return ans