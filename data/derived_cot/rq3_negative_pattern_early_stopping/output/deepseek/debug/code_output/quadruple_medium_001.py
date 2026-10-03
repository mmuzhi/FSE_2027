from typing import List
from functools import cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2

        @cache
        def fn(i: int, x: int) -> int:
            if i == len(toppingCosts) or x < 0:
                return 0
            return min(
                fn(i + 2, x),
                toppingCosts[i] + fn(i + 1, x - toppingCosts[i]),
                key=lambda y: (abs(y - x), y)
            )

        ans = float('inf')
        for bc in baseCosts:
            ans = min(ans, bc + fn(0, target - bc), key=lambda v: (abs(v - target), v))
        return ans