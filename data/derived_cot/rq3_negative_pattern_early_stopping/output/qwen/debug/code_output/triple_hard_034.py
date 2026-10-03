class BIT():
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def sum(self, i):
        ans = 0
        i += 1
        while i > 0:
            ans += self.tree[i]
            i -= (i & -i)
        return ans

    def update(self, i, value):
        i += 1
        while i <= self.n:
            self.tree[i] += value
            i -= (i & -i)

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        from collections import Counter, defaultdict, deque
        if Counter(s) != Counter(t):
            return False
        ind = defaultdict(deque)
        for id, char in enumerate(t):
            ind[char].append(id)
        a = []
        for char in s:
            a.append(ind[char].popleft())
        n = len(a)
        bt = BIT(n)
        for i in range(n):
            inv = bt.sum(n) - bt.sum(a[i])
            bt.update(a[i], 1)
            if a[i] < i - inv:
                return False
        return True