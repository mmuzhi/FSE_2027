from collections import Counter, defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = defaultdict(deque)
        for i, ch in enumerate(t):
            pos[ch].append(i)

        target = []
        for ch in s:
            target.append(pos[ch].popleft())

        last = [-1] * 10
        for i, ch in enumerate(s):
            d = int(ch)
            p = target[i]
            for smaller in range(d):
                if last[smaller] > p:
                    return False
            last[d] = p

        return True