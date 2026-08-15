from typing import List
from functools import lru_cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts = toppingCosts * 2

        @lru_cache(None)
        def fn(i: int, x: int) -> int:
            if x < 0 or i == len(toppingCosts):
                return 0
            return min(
                fn(i + 1, x),
                toppingCosts[i] + fn(i + 1, x - toppingCosts[i]),
                key=lambda y: (abs(y - x), y)
            )

        ans = float('inf')
        for bc in baseCosts:
            ans = min(ans, bc + fn(0, target - bc), key=lambda y: (abs(y - target), y))
        return ans