from collections import Counter, defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = defaultdict(deque)
        for i, ch in enumerate(t):
            pos[int(ch)].append(i)

        for ch in s:
            cur = int(ch)
            idx = pos[cur].popleft()

            for larger in range(cur + 1, 10):
                if pos[larger] and pos[larger][0] < idx:
                    return False

        return True