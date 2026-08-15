from collections import Counter, defaultdict, deque

class Solution:
    def isTransformable(self, s: str, t: str) -> bool:
        if Counter(s) != Counter(t):
            return False

        pos = defaultdict(deque)
        for i, ch in enumerate(t):
            pos[ch].append(i)

        last = [-1] * 10

        for ch in s:
            p = pos[ch].popleft()
            cur = ord(ch) - ord('0')

            for d in range(cur):
                if last[d] >= p:
                    return False

            last[cur] = p

        return True