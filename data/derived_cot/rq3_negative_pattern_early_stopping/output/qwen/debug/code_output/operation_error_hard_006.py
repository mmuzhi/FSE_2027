from collections import Counter, defaultdict
from collections import deque

class BIT():
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def sum(self, i):
        ans = 0
        i += 1
        while i > 0:
            ans += self.tree[i]
            i -= (i & (-i))
        return ans

    def update(self, i, value):
        i += 1
        while i <= self.n:
            self.tree[i] += value
            i -= (i & (-i))

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False
        # We are allowed to swap adjacent characters arbitrarily, so any permutation is possible.
        return True