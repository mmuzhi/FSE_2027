class Solution:
    def maximumCoins(self, coins: List[List[int]], k: int) -> int:
        events = []
        for l, r, c in coins:
            events.append((l, c))
            events.append((r + 1, -c))
        events.sort(key=lambda x: x[0])
        n = len(events)
        # Build an array of the coin values for the entire line? Not possible because coordinates are up to 10^9.
        # Instead, we can use a two-pointer on the events to compute the coin value for any bag? But we need to compute the sum for a window of k bags.
        # Alternatively, we can use a segment tree or a sparse table? But k is up to 10^9, so we cannot iterate over each bag.
        # Another idea: the maximum window must start at a segment boundary or a gap boundary? Actually, the optimal window might start at a segment boundary because the coin value changes only at boundaries.
        # But note: the window is consecutive, so the starting point can be any integer. However, the coin value is constant in segments, so the maximum window must start at a point where the coin value changes (i.e., at a boundary) or just after a boundary? Actually, the window can start anywhere, but the optimal window will have its start and end at boundaries? Not necessarily, but we can consider only the boundaries as candidate starting points because the coin value is constant in between.

        # Let's collect all the boundaries (the start and end+1 of each segment) and also consider the gaps. But the gaps are from r+1 to next segment's l-1.

        # Actually, we can use a different approach: 
        # 1. Create a list of all segment boundaries (l and r+1 for each segment) and sort them.
        # 2. Then, the entire line is divided into segments (by the boundaries). But note, the boundaries are the points where the coin value changes.

        # But then, how to compute the sum for a window of k consecutive bags? 

        # Alternatively, we can use a two-pointer that moves over the events (the boundaries) and use a data structure to compute the sum for a window. But the window is of fixed length k, which might be very large.

        # Another idea: use a line sweep and a Fenwick tree? But k is fixed and the array is sparse.

        # Let me think: the problem is similar to "maximum sum subarray of fixed length" but the array is defined by segments. 

        # We can use a method that considers the entire set of segments and gaps, and then use a sliding window that expands and contracts over the segments. But the window is fixed length k.

        # Steps:
        # 1. Precompute the total length of the segments and the gaps. But the gaps are infinite? Actually, the segments are finite, but the number line is infinite. However, if k is larger than the entire span of the segments, then the maximum coins we can get is the maximum segment's coin value multiplied by the number of times we can cover that segment? Actually, no: because the window is consecutive, we can only cover each segment once. 

        # Actually, the maximum coins we can get is the maximum value of (sum of coins in the window). The window is k consecutive bags. 

        # We can consider that the window might cover multiple segments and gaps. The gaps contribute 0, so we only care about the segments.

        # The challenge is to compute the sum of coins in the window without iterating over each bag.

        # We can use a two-pointer that moves over the segments and gaps, but the window length is k, which might be very large. 

        # Alternatively, we can use a technique similar to "maximum sum subarray" with a fixed window size, but the array is represented by events.

        # Let me reframe: 
        # We have a set of intervals [l_i, r_i] with value c_i. The rest is 0. We want the maximum sum of a contiguous subarray of length k.

        # We can use a difference array (events) and then use a two-pointer that moves the window by events. But the window is fixed length, so we need to compute the sum for a window that starts at a boundary and ends at a boundary.

        # Steps:
        # 1. Create an array of events: (position, delta). For each segment [l, r, c], add (l, c) and (r+1, -c).
        # 2. Sort the events by position.
        # 3. Then, we can use two pointers (left and right) to maintain a window that covers k bags. But how to move the window? The window is of fixed length k, but the events are sparse