class Solution:
    def dp(self, i, s, prev, ct, k, n, dct):
        if k < 0:
            return float("infinity")
        if i >= n:
            if ct == 0:
                return 0
            elif ct == 1:
                return 1
            else:
                return len(str(ct))
        if (i, prev, ct, k) in dct:
            return dct[(i, prev, ct, k)]
        if s[i] == prev:
            res = self.dp(i+1, s, prev, ct+1, k, n, dct)
        else:
            x = 0
            if ct > 0:
                if ct == 1:
                    x = 1
                else:
                    x = len(str(ct))
            inc = x + self.dp(i+1, s, s[i], 1, k, n, dct)
            exc = self.dp(i+1, s, prev, ct, k-1, n, dct)
            res = min(inc, exc)
        dct[(i, prev, ct, k)] = res
        return res

    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        return self.dp(0, s, "", 0, k, n, {})