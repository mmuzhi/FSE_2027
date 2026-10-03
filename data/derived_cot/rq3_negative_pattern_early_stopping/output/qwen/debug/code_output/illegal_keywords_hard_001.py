class BIT():
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def sum(self, i):
        ans = 0
        i += 1
        while i > 0:
            if i <= self.n:
                ans += self.tree[i]
            i -= (i & (-i))
        return ans

    def update(self, i, value):
        i += 1
        while i <= self.n:
            self.tree[i] += value
            i += (i & (-i))


from collections import defaultdict, deque
from typing import Counter

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False
        n = len(s)
        ind_map = defaultdict(deque)
        for idx, char in enumerate(t):
            ind_map[char].append(idx)
        
        a = []
        for char in s:
            if not ind_map[char]:
                return False
            a.append(ind_map[char].popleft())
        
        bt = BIT(n)
        ind = defaultdict(lambda: -1)
        for i in range(n):
            inv = bt.sum(n-1) - bt.sum(a[i])
            bt.update(a[i], 1)
            for dig in range(int(s[i])-1, -1, -1):
                if ind[dig] >= i - inv:
                    return False
            ind[int(s[i])] = i - inv
        return True
