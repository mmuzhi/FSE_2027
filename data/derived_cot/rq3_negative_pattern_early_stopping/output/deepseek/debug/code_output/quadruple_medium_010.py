from typing import List
from functools import cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        @cache
        def fn(i: int, x: int) -> int:
            """Return the additional topping cost from toppingCosts[i:] closest to x."""
            if i == len(toppingCosts) or x < 0:
                return 0
            best = fn(i + 1, x)
            best = min(best, toppingCosts[i] + fn(i + 1, x - toppingCosts[i]),
                       key=lambda y: (abs(y - x), y))
            two_cost = 2 * toppingCosts[i]
            if two_cost <= x:  # only consider if not overshooting x too much? Actually still valid even if overshoots, but adding two servings might make x-t will be negative, and base case handles it.
                best = min(best, two_cost + fn(i + 1, x - two_cost),
                           key=lambda y: (abs(y - x), y))
            return best

        ans = float('inf')
        for bc in baseCosts:
            total = bc + fn(0, target - bc)
            ans = min(ans, total, key=lambda x: (abs(x - target), x))
        return ans