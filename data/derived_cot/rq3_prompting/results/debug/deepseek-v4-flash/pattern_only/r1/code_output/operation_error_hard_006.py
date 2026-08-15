from collections import Counter, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = [deque() for _ in range(10)]
        for i, ch in enumerate(s):
            pos[int(ch)].append(i)

        for ch in t:
            d = int(ch)
            if not pos[d]:
                return False
            p = pos[d].popleft()

            for smaller in range(d):
                if pos[smaller] and pos[smaller][0] < p:
                    return False

        return True