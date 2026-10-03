class Solution:
    def numberOfArrays(self, s: str, k: int) -> int:

        n = len(s)
        mod = 10**9+7

        from functools import lru_cache

        @lru_cache(maxsize=None)
        def rec(i):
            if i == n:
                return 1
            res = 0
            curr = ""
            for x in range(i, n):
                curr += s[x]
                if len(curr) > 1 and curr[0]=='0':
                    break
                num = int(curr)
                if num > k:
                    break
                res = (res + rec(x+1)) % mod
            return res % mod
        
        return rec(0)
