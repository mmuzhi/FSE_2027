from typing import List
from functools import cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2

        @cache
        def fn(i: int, x: int) -> int:
            """Return sum of subsequence of toppingCosts[i:] closest to x."""
            if x < 0 or i == len(toppingCosts):
                return 0
            skip = fn(i+1, x)
            take = toppingCosts[i] + fn(i+1, x - toppingCosts[i])
            return min(skip, take, key=lambda y: (abs(y - x), y))

        ans = float('inf')
        for bc in baseCosts:
            ans = min(ans, bc + fn(0, target - bc), key=lambda x: (abs(x - target), x))
        return ans