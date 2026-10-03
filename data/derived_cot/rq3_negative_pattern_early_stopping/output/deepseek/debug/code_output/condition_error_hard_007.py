from functools import lru_cache

class Solution:
    def numberOfArrays(self, s: str, k: int) -> int:
        n = len(s)
        mod = 10**9 + 7

        @lru_cache(None)
        def rec(i: int = 0) -> int:
            if i == n:
                return 1
            if s[i] == "0":
                return 0
            res = 0
            curr = ""
            for x in range(i, n):
                curr += s[x]
                if int(curr) <= k:
                    res = (res + rec(x + 1)) % mod
                else:
                    break
            return res

        return rec()