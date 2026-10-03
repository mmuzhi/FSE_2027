from typing import List
from functools import lru_cache

class Solution:
    def closestCost(self, baseCosts: List[int], toppingCosts: List[int], target: int) -> int:
        toppingCosts *= 2
        
        @lru_cache(None)
        def fn(i: int, x: int) -> int:
            if x < 0 or i == len(toppingCosts):
                return 0
            skip = fn(i+1, x)
            take = toppingCosts[i] + fn(i+2, x - toppingCosts[i])
            if abs(skip - x) < abs(take - x):
                return skip
            elif abs(take - x) < abs(skip - x):
                return take
            else:
                return min(skip, take)
        
        ans = float('inf')
        for bc in baseCosts:
            cand = bc + fn(0, target - bc)
            if abs(cand - target) < abs(ans - target) or (abs(cand - target) == abs(ans - target) and cand < ans):
                ans = cand
        return ans