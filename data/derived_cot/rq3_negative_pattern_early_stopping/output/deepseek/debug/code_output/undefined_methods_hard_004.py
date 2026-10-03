from functools import lru_cache
from typing import List

class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts = sorted(cuts + [0, n])
        
        @lru_cache(maxsize=None)
        def dfs(l: int, r: int) -> int:
            length = cuts[r] - cuts[l]
            return min((dfs(l, i) + dfs(i, r) for i in range(l+1, r)),
                       default=-length) + length
        
        return dfs(0, len(cuts)-1)