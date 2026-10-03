from typing import List
from collections import defaultdict

class Solution:
    def maxPower(self, stations: List[int], r: int, k: int) -> int:
        start, end = min(stations), sum(stations) + k
        while start + 1 < end:
            mid = (start + end) // 2
            if self.check(stations, r, k, mid):
                start = mid
            else:
                end = mid
        if self.check(stations, r, k, end):
            return end
        else:
            return start
    
    def check(self, stations: List[int], r: int, k: int, target: int) -> bool:
        n = len(stations)
        newStations = defaultdict(int)
        power = sum(stations[:r])
        for i in range(n):
            if i + r < n:
                power += stations[i + r]
            if i - r - 1 >= 0:
                power -= stations[i - r - 1]
            if power >= target:
                continue
            elif power + k < target:
                return False
            else:
                diff = target - power
                power = target
                stations[min(i + r, n - 1)] += diff
                k -= diff
                newStations[min(i + r, n - 1)] += diff
        for i in newStations:
            stations[i] -= newStations[i]
        return True