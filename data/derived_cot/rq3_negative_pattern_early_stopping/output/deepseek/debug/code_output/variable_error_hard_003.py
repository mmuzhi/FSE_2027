from typing import List
from itertools import chain
from functools import lru_cache

class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts = sorted(chain(cuts, [0, n]))
        
        @lru_cache(None)
        def dfs(l: int, r: int) -> int:
            if r - l == 1:  # no cut in this segment
                return 0
            length = cuts[r] - cuts[l]
            best = float('inf')
            for i in range(l + 1, r):
                cost = dfs(l, i) + dfs(i, r) + length
                best = min(best, cost)
            return best
        
        return dfs(0, len(cuts) - 1)