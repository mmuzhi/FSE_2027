from typing import List
from itertools import chain
from functools import lru_cache

class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts = sorted(chain(cuts, [0, n]))

        @lru_cache(None)
        def dfs(l, r):
            if r - l <= 1:
                return 0
            return cuts[r] - cuts[l] + min(
                dfs(l, i) + dfs(i, r) for i in range(l + 1, r)
            )

        return dfs(0, len(cuts) - 1)