from functools import lru_cache
from typing import List

class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts = sorted(set(cuts + [0, n]))

        @lru_cache(None)
        def dfs(l: int, r: int) -> int:
            if r - l <= 1:
                return 0
            return min(
                dfs(l, k) + dfs(k, r) + (cuts[r] - cuts[l])
                for k in range(l + 1, r)
            )

        return dfs(0, len(cuts) - 1)