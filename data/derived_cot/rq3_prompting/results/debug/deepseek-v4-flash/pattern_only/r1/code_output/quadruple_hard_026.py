from collections import Counter, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = [deque() for _ in range(10)]
        for i, ch in enumerate(t):
            pos[ord(ch) - 48].append(i)

        last = [-1] * 10

        for ch in s:
            d = ord(ch) - 48
            j = pos[d].popleft()

            for smaller in range(d):
                if last[smaller] > j:
                    return False

            last[d] = j

        return True