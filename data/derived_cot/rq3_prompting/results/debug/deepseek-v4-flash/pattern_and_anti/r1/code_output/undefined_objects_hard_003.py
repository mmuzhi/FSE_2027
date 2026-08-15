from collections import Counter, defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = defaultdict(deque)
        for i, ch in enumerate(t):
            pos[ch].append(i)

        last = [-1] * 10

        for ch in s:
            p = pos[ch].popleft()
            d = int(ch)
            for smaller in range(d):
                if last[smaller] > p:
                    return False
            last[d] = p

        return True