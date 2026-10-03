from math import ceil
from typing import List

class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        if len(dist) - 1 >= hour:
            return -1
        frac = 1 if hour.is_integer() else hour - int(hour)
        right = ceil(max(max(dist), dist[-1] / frac))
        left = 1
        while left < right:
            mid = (left + right) // 2
            if sum(ceil(i / mid) for i in dist[:-1]) + (dist[-1] / mid) <= hour:
                right = mid
            else:
                left = mid + 1
        return left