from functools import lru_cache
from math import inf
from typing import List


class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts = toppingCosts * 2

        @lru_cache(None)
        def fn(i: int, x: int) -> int:
            if x < 0 or i == len(toppingCosts):
                return 0

            skip = fn(i + 1, x)
            take = toppingCosts[i] + fn(i + 1, x - toppingCosts[i])
            return min(skip, take, key=lambda y: (abs(y - x), y))

        ans = inf
        for bc in baseCosts:
            ans = min(ans, bc + fn(0, target - bc), key=lambda x: (abs(x - target), x))

        return ans