from typing import List
from functools import cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        @cache
        def fn(i, x):
            """Return sum of subsequence of toppingCosts[i:] closest to x."""
            if x < 0 or i == len(toppingCosts):
                return 0
            return min(fn(i+1, x), 
                       toppingCosts[i] + fn(i+1, x-toppingCosts[i]), 
                       2*toppingCosts[i] + fn(i+1, x-2*toppingCosts[i]), 
                       key=lambda y: (abs(y-x), y))
        
        ans = float('inf')
        for bc in baseCosts: 
            ans = min(ans, bc + fn(0, target - bc), key=lambda x: (abs(x-target), x))
        return ans