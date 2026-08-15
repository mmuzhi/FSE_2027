from functools import lru_cache
import sys

class Solution:
    def numberOfArrays(self, s: str, k: int) -> int:
        sys.setrecursionlimit(10000)
        n = len(s)
        mod = 10**9 + 7

        @lru_cache(None)
        def rec(i=0):
            if i == n:
                return 1
            if s[i] == "0":
                return 0

            res = 0
            curr = ""
            for x in range(i, n):
                curr += s[x]
                if int(curr) > k:
                    break
                res = (res + rec(x + 1)) % mod

            return res

        return rec()