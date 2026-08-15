from collections import defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False

        positions = defaultdict(deque)
        for i, ch in enumerate(s):
            positions[int(ch)].append(i)

        for ch in t:
            d = int(ch)
            if d not in positions or not positions[d]:
                return False

            for smaller in range(d):
                if smaller in positions and positions[smaller] and positions[smaller][0] < positions[d][0]:
                    return False

            positions[d].popleft()
            if not positions[d]:
                del positions[d]

        return True