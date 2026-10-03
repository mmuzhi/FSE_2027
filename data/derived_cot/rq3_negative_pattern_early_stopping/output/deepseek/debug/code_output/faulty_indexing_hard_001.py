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
        added = [0] * n          # extra power added to each station
        orig_power = sum(stations[0:min(n, r + 1)])
        cur_added = 0            # sum of added power affecting current city

        for i in range(n):
            if i > 0:
                left_out = i - r - 1
                if left_out >= 0:
                    orig_power -= stations[left_out]
                    cur_added -= added[left_out]
                right_in = i + r
                if right_in < n:
                    orig_power += stations[right_in]
                    cur_added += added[right_in]

            total_power = orig_power + cur_added

            if total_power < target:
                diff = target - total_power
                if diff > k:
                    return False
                j = min(i + r, n - 1)
                added[j] += diff
                k -= diff
                cur_added += diff   # this station is within the current window
                total_power = target

        return True