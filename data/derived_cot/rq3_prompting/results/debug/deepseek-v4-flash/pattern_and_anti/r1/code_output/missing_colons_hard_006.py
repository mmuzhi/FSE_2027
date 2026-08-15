from collections import deque

class Solution:
    def kSimilarity(self, s1: str, s2: str) -> int:
        q = deque([s1])
        seen = {s1}
        ans = 0

        while q:
            for _ in range(len(q)):
                s = q.popleft()
                if s == s2:
                    return ans

                i = 0
                while s[i] == s2[i]:
                    i += 1

                for j in range(i + 1, len(s)):
                    if s[j] == s2[i] and s[j] != s2[j]:
                        nxt = s[:i] + s[j] + s[i+1:j] + s[i] + s[j+1:]
                        if nxt not in seen:
                            seen.add(nxt)
                            q.append(nxt)

            ans += 1

        return -1