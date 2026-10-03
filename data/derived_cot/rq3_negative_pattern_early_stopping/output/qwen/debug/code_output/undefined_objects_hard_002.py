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
    
    def check(self, stations, r, k, target):
        n = len(stations)
        # We'll use a greedy method from left to right.
        # We maintain an array `add` to record the added power for each station.
        add = [0] * n
        # We'll also maintain the current window's total power (base + added) for the current station.
        # But note: the window for station i is [i-r+1, i+r-1].
        # We'll use a two-pointer to maintain the window and update the current power.
        # However, we can use a different approach: we'll iterate i from 0 to n-1 and maintain the window's power.
        # Let `curr` be the current window's total power (base + added) for station i.
        # But we need to know the window's power without iterating over all stations in the window each time.
        # We can use a sliding window and update `curr` by removing the station that is leaving and adding the station that is entering.
        # The window for station i is [i-r+1, i+r-1].
        # For station i, the window is [i-r+1, i+r-1].
        # For station i+1, the window is [i+1-r+1, i+1+r-1] = [i-r+2, i+r].
        # So we remove station i-r+1 and add station i+r.
        # But note: the window for station i might be shorter at the boundaries.

        # We'll maintain:
        #   `curr`: the current window's total power (base + added)
        #   `left` and `right` pointers for the window boundaries.
        #   But we can also maintain the window's base sum separately.

        # Alternatively, we can use a two-pointer that expands the window for each station and then updates the window's power.

        # Let's define:
        #   `curr` = 0
        #   `l` = 0
        #   `r` = 0
        #   `base_sum` = 0
        #   `added_sum` = 0

        # But then we need to update the window for each station.

        # We'll do:

        #   For station i from 0 to n-1:
        #       Let left_bound = i - r + 1
        #       Let right_bound = i + r - 1

        #       But then we need to ensure that the window is [left_bound, right_bound].

        #       We can move the left pointer to left_bound and the right pointer to right_bound.

        #       But then the complexity is O(n^2).

        #   We need to use a two-pointer that moves only forward.

        #   We can do:

        #       Let `curr` = 0
        #       Let `l` = 0
        #       Let `r` = 0
        #       Let `base_sum` = 0
        #       Let `added_sum` = 0

        #       For i in range(n):
        #           # The window for station i is [i-r+1, i+r-1]
        #           # We need to extend the window to the right until we reach i+r-1.
        #           while r < n and r <= i+r-1:
        #               base_sum += stations[r]
        #               added_sum += add[r]
        #               r += 1
        #           # Now, the window's base_sum is the sum of stations from l to r-1.
        #           # But the window should be [i-r+1, i+r-1], so we need to set l = i-r+1.
        #           l = i - r + 1
        #           # But then we need to subtract the stations from 0 to l-1.
        #           while l > 0:
        #               base_sum -= stations[l-1]
        #               added_sum -= add[l-1]
        #               l -= 1

        #       This is not efficient.

        #   Given the complexity, I decide to use a simpler approach: for each station i, we compute the window