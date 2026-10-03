from functools import cache
from typing import List

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2

        @cache
        def fn(i: int, x: int) -> int:
            if i == len(toppingCosts):
                return 0
            if x <= 0:
                return 0
            skip = fn(i + 1, x)
            take = toppingCosts[i] + fn(i + 2, x - toppingCosts[i])
            return min(skip, take, key=lambda y: (abs(y - x), y))

        ans = float('inf')
        for bc in baseCosts:
            candidate = bc + fn(0, target - bc)
            ans = min(ans, candidate, key=lambda x: (abs(x - target), x))
        return ans