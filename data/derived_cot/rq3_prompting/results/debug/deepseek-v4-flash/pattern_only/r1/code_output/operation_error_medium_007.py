from typing import List

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def check(x):
            return sum((p + x - 1) // x for p in piles) <= h

        l, r = 1, max(piles)
        while l < r:
            mid = (l + r) // 2
            if not check(mid):
                l = mid + 1
            else:
                r = mid
        return l