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
        # We'll use a greedy approach: we traverse the stations and ensure that every window of length (2*r+1) has at least `target` power.
        # But note: the problem is to achieve at least `target` in every window? Actually, the binary search is for the maximum power that we can ensure is at least `target` in every window? 
        # Let me clarify: the goal is to have every window of length (2*r+1) to have at least `target` power. Then we are trying to find the maximum `target` that we can achieve with budget k.
        # However, the original code was trying to do something else.

        # We are going to simulate the circular array. We can break the circularity by duplicating the array.
        arr = stations + stations  # to handle circularity
        m = len(arr) // 2  # the original length

        # We'll use a sliding window of length (2*r+1) and keep track of the current sum in the window.
        # We also need to account for the budget k.

        # We are going to traverse the first half (original length) and for each window, if the current sum is less than target, we need to add some budget to make it at least target.
        # But note: we can only add to stations, and the same station might be covered by multiple windows.

        # However, the original code's approach was flawed. Let's try a different approach in the check function.

        # We'll use a greedy method: we traverse the stations and whenever a window has a deficit (current sum < target), we add the deficit to the station that is leaving the window (or the one that is at the rightmost of the window) and then update the budget.

        # But note: the window is of fixed length (2*r+1). We can break the circularity by duplicating the array.

        # Let's define:
        #   current_sum = sum of the current window (from i to i+2*r)
        #   We traverse i from 0 to n-1 (the first half of the duplicated array, but we only need to cover the original stations once)

        # However, the problem is circular, so we can break the array and then consider the windows that wrap around.

        # Alternatively, we can use a two-pass method: first, we consider the non-circular part and then the circular part.

        # But note: the original code tried to do a circular simulation by using modulo indexing. Let's stick to the duplicated array.

        # We'll use a variable `current` to keep the sum of the current window (from i to i+2*r).
        # We'll also keep an array `add` to record how much we add to each station (so we don't add the same station multiple times).

        # Steps:
        #   Let `current` = sum of the first window (from 0 to 2*r)
        #   For i from 0 to n-1 (the original stations):
        #       If current < target, then we need to add (target - current) to the current window. But we can only add to stations that are in the current window and haven't been fully accounted for by previous additions? Actually, we can add to any station, but we want to minimize the total budget used.

        #   However, the optimal way is to add the deficit to the station that is leaving the window (i.e., the station at position i-1) because that station will not be in the next window? But note: the window is moving to the right.

        #   Actually, we can use a greedy method: we traverse the array and whenever the window's sum is below target, we add the deficit to the station that is at the leftmost of the window (the one that is leaving) because that station is no longer in the next window? But wait, the window is of fixed length and we are moving from left to right.

        #   Let me explain:
        #       Window i: [i, i+2*r]
        #       Next window: [i+1, i+2*r+1]
        #       The station that leaves is i,