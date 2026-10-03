from collections import defaultdict
from fractions import Fraction

class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        N = len(points)
        D = defaultdict(set)
        if N <= 2:
            return N 
        for i in range(N):
            x1, y1 = points[i]
            for j in range(i+1, N):
                x2, y2 = points[j]
                if y1 == y2:
                    k1, k2 = 'inf', y1
                elif x1 == x2:
                    k1, k2 = x1, 'inf'
                else:
                    k1 = Fraction(y2 - y1, x2 - x1)
                    k2 = Fraction(x2 * y1 - x1 * y2, x2 - x1)
                D[(k1,k2)].add(tuple(points[i]))
                D[(k1,k2)].add(tuple(points[j]))
        return max([len(i) for i in D.values()])