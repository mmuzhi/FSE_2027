class Solution:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        memo = {}

        def dp(i: int, prev: str, ct: int, k: int) -> int:
            if k < 0:
                return float('inf')
            if i >= n:
                if ct > 1:
                    return 1 + len(str(ct))
                elif ct == 1:
                    return 1
                return 0

            key = (i, prev, ct, k)
            if key in memo:
                return memo[key]

            if s[i] == prev:
                inc = dp(i + 1, prev, ct + 1, k)
            else:
                if ct > 1:
                    x = 1 + len(str(ct))
                elif ct == 1:
                    x = 1
                else:
                    x = 0
                inc = x + dp(i + 1, s[i], 1, k)

            exc = dp(i + 1, prev, ct, k - 1)

            memo[key] = min(inc, exc)
            return memo[key]

        return dp(0, "", 0, k)