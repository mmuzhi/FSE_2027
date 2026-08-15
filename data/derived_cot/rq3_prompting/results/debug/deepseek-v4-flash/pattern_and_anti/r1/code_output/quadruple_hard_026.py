from collections import Counter, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = [deque() for _ in range(10)]
        for i, ch in enumerate(t):
            pos[int(ch)].append(i)

        max_pos = [-1] * 10

        for ch in s:
            d = int(ch)
            p = pos[d].popleft()

            for smaller in range(d):
                if max_pos[smaller] > p:
                    return False

            if p > max_pos[d]:
                max_pos[d] = p

        return True