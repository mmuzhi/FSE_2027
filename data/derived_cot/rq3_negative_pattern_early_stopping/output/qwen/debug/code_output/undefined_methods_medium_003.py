import math

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        def check(x):
            total_hours = 0
            for ele in piles:
                total_hours += math.ceil(ele / x)
            return total_hours <= h
        
        l, r = 1, max(piles)
        while l < r:
            mid = (l + r) // 2
            if check(mid):
                r = mid
            else:
                l = mid + 1
        return l