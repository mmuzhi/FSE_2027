class Solution:
    def dp(self, i, s, prev, k, ct, n, dct):
        if i >= n + 1:
            if ct == 0:
                return 0
            elif ct == 1:
                return 1
            else:
                return len(str(ct))
        if (i, prev, ct, k) in dct:
            return dct[(i, prev, ct, k)]
        if s[i] == prev:
            inc = self.dp(i+1, s, prev, k, ct+1, n, dct)
        else:
            # Break the run: account for the current run (if any) and then start a new run with s[i]
            if ct == 0:
                inc = self.dp(i+1, s, s[i], k, 1, n, dct)
            else:
                # Account for the broken run
                if ct == 1:
                    cost_break = 1
                else:
                    cost_break = len(str(ct))
                inc = cost_break + self.dp(i+1, s, s[i], k, 1, n, dct)
        exc = self.dp(i+1, s, prev, k-1, ct, n, dct)
        dct[(i, prev, ct, k)] = min(inc, exc)
        return min(inc, exc)

    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        return self.dp(0, s, "", k, 0, n, {})
