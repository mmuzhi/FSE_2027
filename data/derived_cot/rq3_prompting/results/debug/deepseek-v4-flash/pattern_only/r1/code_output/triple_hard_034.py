from collections import Counter, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = [deque() for _ in range(10)]
        for i, ch in enumerate(t):
            pos[int(ch)].append(i)

        for ch in s:
            d = int(ch)
            idx = pos[d].popleft()

            for larger in range(d + 1, 10):
                if pos[larger] and pos[larger][0] < idx:
                    return False

        return True