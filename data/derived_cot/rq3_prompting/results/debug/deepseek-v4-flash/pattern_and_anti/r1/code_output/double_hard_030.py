from collections import deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        idx = [deque() for _ in range(10)]
        for i, c in enumerate(s):
            idx[int(c)].append(i)

        for c in t:
            d = int(c)
            if not idx[d]:
                return False

            p = idx[d][0]
            for smaller in range(d):
                if idx[smaller] and idx[smaller][0] < p:
                    return False

            idx[d].popleft()

        return True