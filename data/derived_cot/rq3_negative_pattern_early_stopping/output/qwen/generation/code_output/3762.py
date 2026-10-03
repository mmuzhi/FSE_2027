class Solution:
    def maxScore(self, points: List[int], m: int) -> int:
        n = len(points)
        # We'll use binary search on the answer x (the minimum value)
        # The answer x must be between 0 and max(points) * m (but actually, we can set an upper bound)
        # But note: we are distributing m visits (each visit adds points[i]), so the maximum x is at most max(points) * (m) but actually, we are distributing over multiple indices.
        # But we can set high = max(points) * m  (since each index can be visited at most m times, and the maximum points is max(points), so the maximum x is at most max(points) * (m) but actually, we are distributing m visits over the entire array, so the maximum x is at most max(points) * (m) but that's too high.

        # Actually, the minimal required counts for an index i is ceil(x / points[i]), and the total visits is the sum of these. But the total visits must be <= m.

        # We can set high = max(points) * (m)  (but that's too high, because m can be 10^9 and points[i] up to 10^6, so high would be 10^15, which is acceptable for binary search in Python if we do it in logarithmic steps).

        # But we can set a better high: the maximum x is at most max(points) * (m) but actually, we are distributing m visits, so the maximum x is at most max(points) * (m) but that's not tight. But for binary search, we can set high = max(points) * (m) + 1.

        # But note: the minimal required counts for an index i is ceil(x / points[i]), and the total visits is the sum over the segment. The segment must include 0. The minimal total visits is at least ceil(x / points[0]). 

        # We can set high = max(points) * (m)  (since if x is larger than that, then even if we assign all m visits to the index with the maximum points, we get x_max = points[i] * m, but we are distributing over multiple indices, so the minimum value might be lower).

        # Actually, the maximum x we can achieve is at most the minimum value of (points[i] * (number of times we visit i)) for all i. But the number of times we visit i is at most m (if we visit only one index). 

        # But we are distributing m visits (each visit is one move). The minimal value is the minimum over i of (count[i] * points[i]). 

        # The maximum x is at most the maximum points[i] * (floor(m / (number of indices))) but that's not straightforward.

        # Alternatively, we can set high = max(points) * (m)  (since even if we visit one index m times, the value is points[i] * m, but we are distributing over multiple indices, so the minimum value might be lower). But for binary search, we can set high = max(points) * (m) + 1.

        # But note: the minimal required counts for an index i is ceil(x / points[i]). The total visits is the sum of these counts over the segment. The segment must include 0. The minimal total visits for a given x is the sum of ceil(x / points[i]) for i in the segment. 

        # We need to find the maximum x such that there exists a contiguous segment (including 0) with total minimal visits <= m.

        # We can use binary search on x from 0 to max(points) * (m) (or maybe a bit more, but we can set high = max(points) * (m) + 1).

        # But note: the minimal total visits for a segment is the sum of ceil(x / points[i]) for i in the segment. We need to check if there exists a contiguous segment (including 0) such that this sum <= m.

        # How to check for a given x?
        #   1. Compute an array req: for each index i, req[i] = (x + points[i] - 1) // points[i]  (this is ceil(x / points[i]) for integer x and points[i])
        #   2. Then, we need to find a contiguous segment [L, R] (with 0 in [L, R]) such that the sum of req[L..R] <= m.

        # But note: the segment must include 0. We can consider the entire array? But the array is fixed. We can use a two-pointer (sliding window) that starts at 0 and then expands to the left and