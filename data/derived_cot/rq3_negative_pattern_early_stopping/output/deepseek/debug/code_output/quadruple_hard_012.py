class Solution:
    def dp(self, i, s, prev, k, ct, n, dct):
        if k < 0:
            return float("inf")
        if i >= n:
            if ct == 0:
                return 0
            elif ct == 1:
                return 1
            else:
                return 1 + len(str(ct))
        key = (i, prev, ct, k)
        if key in dct:
            return dct[key]
        if s[i] == prev:
            inc = self.dp(i + 1, s, prev, k, ct + 1, n, dct)
        else:
            x = 0
            if ct > 1:
                x = 1 + len(str(ct))
            elif ct == 1:
                x = 1
            inc = x + self.dp(i + 1, s, s[i], k, 1, n, dct)
        exc = self.dp(i + 1, s, prev, k - 1, ct, n, dct)
        res = min(inc, exc)
        dct[key] = res
        return res

    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        return self.dp(0, s, "", k, 0, n, {})