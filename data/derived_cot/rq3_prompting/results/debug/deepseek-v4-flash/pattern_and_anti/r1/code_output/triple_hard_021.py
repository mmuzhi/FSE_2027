class Solution:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        memo = {}

        def dp(i, prev, cnt, k):
            if k < 0:
                return float('inf')
            if i == n:
                if cnt > 1:
                    return len(str(cnt)) + 1
                elif cnt == 1:
                    return 1
                return 0

            key = (i, prev, cnt, k)
            if key in memo:
                return memo[key]

            if s[i] == prev:
                keep = dp(i + 1, prev, cnt + 1, k)
            else:
                add = 0
                if cnt > 1:
                    add = len(str(cnt)) + 1
                elif cnt == 1:
                    add = 1
                keep = add + dp(i + 1, s[i], 1, k)

            delete = dp(i + 1, prev, cnt, k - 1)

            memo[key] = min(keep, delete)
            return memo[key]

        return dp(0, "", 0, k)