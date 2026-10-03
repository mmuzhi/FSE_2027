from collections import defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        idx = defaultdict(deque)
        for i, c in enumerate(s):
            idx[int(c)].append(i)
        for c in t:
            d = int(c)
            if not idx[d]:
                return False
            i = idx[d].popleft()
            for k in range(d):
                if idx[k] and idx[k][0] < i:
                    return False
        return True