import sys
from collections import defaultdict
import bisect

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); q = int(next(it))
    
    # We'll maintain:
    # 1. A list `intervals` of intervals (l, r, color) for the entire row, sorted by l.
    # 2. A dictionary `color_intervals` that maps color to a sorted list of (l, r) for intervals of that color.
    # 3. An array `color_count` for counts of each color, indexed by color (colors are from 1 to n, but note: c can be up to n, but initially colors are from 1 to n, and queries use c in [1, n]).
    # 4. A list `cells` is not stored; we use intervals.
    
    # But note: initially, each cell i has color i. So we have intervals: for i from 1 to n, interval [i, i] with color i.
    intervals = []  # list of (l, r, color)
    color_intervals = defaultdict(list)  # color -> list of (l, r)
    color_count = [0] * (n+1)  # 1-indexed, index from 1 to n
    
    # Initialize: each cell i is an interval [i, i] with color i.
    for i in range(1, n+1):
        color_intervals[i].append((i, i))
        color_count[i] = 1
    
    # We'll maintain a sorted list of intervals by l. But we also need to be able to query by x.
    # Instead, we can store the intervals in a list and keep it sorted by l. Then, to find the interval containing x, we can do a binary search for the interval with l <= x and then check if x <= r.
    # But we need to update the intervals, so we'll use a list and keep it sorted by l. Then, we can use bisect to find the interval.
    # However, we also need to remove and insert intervals, so we'll use a sorted list and update it.
    # We'll maintain a separate list `intervals_list` that is sorted by l.
    intervals_list = []
    # But initially, we have many intervals. We can start with a list of all intervals [ (i, i, i) for i in range(1, n+1) ] and then sort by l.
    # But then, we need to update. Alternatively, we can use a balanced BST simulation with sorted list and bisect.
    # Let's use a list `intervals_list` that is sorted by l. We'll insert and remove using bisect and then maintain sorted order.
    # But then, the total number of intervals is initially n, and each query type 1 might merge intervals, so the number of intervals decreases.
    
    # Actually, we can use a different approach: store the intervals in a dictionary `color_intervals` and a global sorted list of all intervals (by l) for the entire row.
    # But then, to find the interval containing x, we can:
    #   - Find the interval in the global list that has l <= x <= r.
    #   - We can use bisect to find the interval with l <= x, and then check if x <= r.
    #   - But there might be multiple intervals with l <= x, so we need to find the one that has r >= x.
    #
    # Alternatively, we can store the intervals in a balanced BST keyed by l, and then also store a separate BST keyed by r? Or use a segment tree.
    #
    # Given the constraints, we can use a list `intervals_list` and use bisect to find the interval containing x.
    #
    # Steps for query type 1 x c:
    #   1. Find the interval containing x. We'll search in `intervals_list` for the interval with l <= x and the next interval has l > x, and then check if x <= r.
    #   2. But since the intervals are disjoint and cover the entire row, there is exactly one interval containing x.
    #
    # However, we need to update the intervals_list and color_intervals.
    #
    # Let's reinitialize:
    #   intervals_list = sorted list of (l, r, color) for all intervals, initially [(i, i, i) for i in range(1, n+1)]
    #   color_intervals: defaultdict(list) with each color i having [(i, i)]
    #   color_count: [0]*(n+1), then for i in 1..n: color_count[i] = 1
    #
    # But then, to