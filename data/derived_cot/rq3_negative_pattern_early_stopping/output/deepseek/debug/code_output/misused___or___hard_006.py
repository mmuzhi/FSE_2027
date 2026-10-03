from collections import defaultdict
from typing import List

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        N = len(points)
        if N <= 2:
            return N
        D = defaultdict(set)
        for i in range(N):
            x1, y1 = points[i]
            for j in range(i+1, N):
                x2, y2 = points[j]
                if y1 == y2:
                    k1, k2 = 0, y1
                elif x1 == x2:
                    k1, k2 = x1, 'inf'
                else:
                    k1 = (y2 - y1) / (x2 - x1)
                    k2 = (x2 * y1 - x1 * y2) / (x2 - x1)
                D[(k1, k2)].add(tuple(points[i]))
                D[(k1, k2)].add(tuple(points[j]))
        return max(len(v) for v in D.values())