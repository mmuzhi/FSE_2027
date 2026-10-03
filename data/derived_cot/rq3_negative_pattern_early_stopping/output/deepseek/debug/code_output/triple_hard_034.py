from collections import Counter, defaultdict, deque

class BIT:
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
            i += (i & (-i))


class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False
        pos = defaultdict(deque)
        for idx, ch in enumerate(t):
            pos[ch].append(idx)
        a = []
        for ch in s:
            a.append(pos[ch].popleft())
        n = len(a)
        bt = BIT(n)
        adjusted = defaultdict(lambda: -1)
        for i in range(n):
            inv = bt.sum(n) - bt.sum(a[i])
            bt.update(a[i], 1)
            for dig in range(int(s[i]) - 1, -1, -1):
                if adjusted[dig] >= i - inv:
                    return False
            adjusted[int(s[i])] = i - inv
        return True