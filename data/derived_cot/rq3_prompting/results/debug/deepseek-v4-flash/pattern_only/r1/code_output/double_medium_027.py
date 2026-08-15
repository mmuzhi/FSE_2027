from typing import List
from math import ceil

class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        n = len(dist)
        if hour <= n - 1:
            return -1

        right = max(
            max(dist[:-1]) if n > 1 else 0,
            ceil(dist[-1] / (hour - (n - 1)))
        )
        left = 1

        while left < right:
            mid = (left + right) // 2
            total = 0
            for i in range(n - 1):
                total += (dist[i] + mid - 1) // mid
            total += dist[-1] / mid

            if total <= hour:
                right = mid
            else:
                left = mid + 1

        return left