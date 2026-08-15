from collections import defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        indexes = defaultdict(deque)
        for i, ch in enumerate(s):
            indexes[int(ch)].append(i)

        for ch in t:
            d = int(ch)
            if not indexes[d]:
                return False

            for smaller in range(d):
                if indexes[smaller] and indexes[smaller][0] < indexes[d][0]:
                    return False

            indexes[d].popleft()
            if not indexes[d]:
                del indexes[d]

        return True