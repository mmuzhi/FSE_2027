from collections import defaultdict, deque
from typing import List

class BIT:
    def __init__(self, n: int):
        self.n = n
        self.tree = [0] * (n + 1)

    def sum(self, i: int) -> int:
        ans = 0
        i += 1
        while i > 0:
            ans += self.tree[i]
            i -= (i & -i)
        return ans

    def update(self, i: int, value: int) -> None:
        i += 1
        while i <= self.n:
            self.tree[i] += value
            i += (i & -i)


class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        from collections import Counter
        if Counter(s) != Counter(t):
            return False

        ind = defaultdict(deque)
        for idx, ch in enumerate(t):
            ind[ch].append(idx)

        a = []
        for ch in s:
            a.append(ind[ch].popleft())

        n = len(a)
        bt = BIT(n + 1)
        pos = defaultdict(lambda: -1)

        for i in range(n):
            inv = bt.sum(n) - bt.sum(a[i])
            bt.update(a[i], 1)
            cur_pos = i - inv
            for d in range(int(s[i]) - 1, -1, -1):
                if pos[d] >= cur_pos:
                    return False
            pos[int(s[i])] = cur_pos

        return True