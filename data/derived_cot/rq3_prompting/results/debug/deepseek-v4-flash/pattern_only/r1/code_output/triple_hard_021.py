from functools import lru_cache

class Solution:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)

        @lru_cache(None)
        def dp(i, prev, cnt, rem):
            if rem < 0:
                return float('inf')

            if i == n:
                if cnt == 0:
                    return 0
                if cnt == 1:
                    return 1
                return 1 + len(str(cnt))

            if s[i] == prev:
                keep = dp(i + 1, prev, cnt + 1, rem)
            else:
                add = 0
                if cnt > 1:
                    add = 1 + len(str(cnt))
                elif cnt == 1:
                    add = 1
                keep = add + dp(i + 1, s[i], 1, rem)

            delete = dp(i + 1, prev, cnt, rem - 1)

            return min(keep, delete)

        return dp(0, "", 0, k)