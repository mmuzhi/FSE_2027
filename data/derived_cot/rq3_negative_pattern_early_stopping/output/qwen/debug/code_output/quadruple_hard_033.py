from collections import defaultdict, deque

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
        from collections import Counter
        if Counter(s) != Counter(t):
            return False
        
        n = len(s)
        ind = defaultdict(deque)
        for id, char in enumerate(t):
            ind[char].append(id)
        
        a = []
        for char in s:
            a.append(ind[char].popleft())
        
        bt = BIT(n + 1)
        assigned = {}
        
        for i in range(n):
            bt.update(a[i], 1)
            inv = bt.sum(n) - bt.sum(a[i])
            
            if s[i].isdigit():
                d = int(s[i])
                for dig in range(d - 1, -1, -1):
                    if dig in assigned and assigned[dig] >= i - inv:
                        return False
                assigned[d] = i - inv
        
        return True