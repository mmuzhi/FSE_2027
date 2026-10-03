from typing import List
from functools import cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2

        @cache
        def fn(i: int, x: int) -> int:
            """Return sum of subsequence of toppingCosts[i:] closest to x."""
            if i == len(toppingCosts) or x <= 0:
                return 0
            skip = fn(i + 1, x)
            take = toppingCosts[i] + fn(i + 1, x - toppingCosts[i])
            return min(skip, take, key=lambda y: (abs(y - x), y))

        ans = float('inf')
        for bc in baseCosts:
            total = bc + fn(0, target - bc)
            ans = min(ans, total, key=lambda x: (abs(x - target), x))
        return ans