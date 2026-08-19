from math import ceil
from typing import List


class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        n = len(dist)
        if hour <= n - 1:
            return -1
        left = 1
        right = max(max(dist), ceil(dist[-1] / (hour - n + 1)))
        while left < right:
            mid = (left + right) // 2
            if sum(ceil(d / mid) for d in dist[:-1]) + dist[-1] / mid <= hour:
                right = mid
            else:
                left = mid + 1
        return left