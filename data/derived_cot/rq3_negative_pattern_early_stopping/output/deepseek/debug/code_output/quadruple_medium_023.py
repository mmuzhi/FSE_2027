from typing import List
from functools import lru_cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2  

        @lru_cache(None)
        def fn(i: int, x: int) -> int:
            if x < 0 or i == len(toppingCosts):
                return 0
            skip = fn(i + 1, x)
            take = toppingCosts[i] + fn(i + 1, x - toppingCosts[i])
            return min(skip, take, key=lambda y: (abs(y - x), y))

        ans = float('inf')
        for bc in baseCosts:
            best_topping = fn(0, target - bc)
            cand = bc + best_topping
            ans = min(ans, cand, key=lambda c: (abs(c - target), c))
        return ans