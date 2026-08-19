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
            pos = idx[d].popleft()
            for j in range(d):
                if idx[j] and idx[j][0] < pos:
                    return False
        return True