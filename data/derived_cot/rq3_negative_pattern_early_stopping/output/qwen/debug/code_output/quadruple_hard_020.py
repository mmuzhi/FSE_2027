from collections import Counter, defaultdict, deque

class BIT:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def sum(self, i):
        s = 0
        idx = i + 1
        while idx:
            s += self.tree[idx]
            idx -= (idx & -idx)
        return s

    def update(self, i, delta):
        idx = i + 1
        while idx <= self.n:
            self.tree[idx] += delta
            idx += (idx & -idx)

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False
        
        n = len(s)
        ind = defaultdict(deque)
        for idx, char in enumerate(t):
            ind[char].append(idx)
        
        a = []
        for char in s:
            a.append(ind[char].popleft())
        
        bt = BIT(n + 1)
        for i in range(n):
            inv = bt.sum(n) - bt.sum(a[i])
            bt.update(a[i], 1)
            for dig in range(int(s[i]) - 1, -1, -1):
                if ind[dig] and ind[dig][0] >= i - inv:
                    return False
            ind[int(s[i])].append(i - inv)
        return True