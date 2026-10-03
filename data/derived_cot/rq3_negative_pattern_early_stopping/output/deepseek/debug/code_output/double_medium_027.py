from typing import List
import math

class Solution:
    def minSpeedOnTime(self, dist: List[int], hour: float) -> int:
        n = len(dist)
        if hour <= n - 1:
            return -1
        
        left, right = 1, 10**7
        
        def feasible(speed: int) -> bool:
            total_time = 0.0
            for d in dist[:-1]:
                total_time += (d + speed - 1) // speed  # integer ceil
            total_time += dist[-1] / speed
            return total_time <= hour
        
        while left < right:
            mid = (left + right) // 2
            if feasible(mid):
                right = mid
            else:
                left = mid + 1
        
        return left