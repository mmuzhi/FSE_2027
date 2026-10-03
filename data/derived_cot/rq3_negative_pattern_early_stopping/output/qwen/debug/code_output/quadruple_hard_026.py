from collections import defaultdict, deque, Counter

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
        n = len(s)
        pos_dict = defaultdict(deque)
        for idx, char in enumerate(t):
            pos_dict[int(char)].append(idx)
        
        last_occ = defaultdict(lambda: -1)
        bt = BIT(n)
        
        for i, char in enumerate(s):
            c = int(char)
            if not pos_dict[c]:
                return False
            idx_t = pos_dict[c].popleft()
            bt.update(idx_t, 1)
            total_matched = i + 1
            prefix_sum = bt.sum(idx_t)
            inv = total_matched - prefix_sum
            for dig in range(c - 1, -1, -1):
                if last_occ[dig] >= i - inv:
                    return False
            last_occ[c] = idx_t
        
        return True