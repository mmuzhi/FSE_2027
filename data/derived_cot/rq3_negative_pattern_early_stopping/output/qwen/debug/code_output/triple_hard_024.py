class Solution:
    def dp(self, i, s, prev, k, ct, n, dct):
        if k < 0:
            return float("inf")
        if i >= n:
            if ct == 0:
                return 0
            if ct == 1:
                return 1
            return len(str(ct)) + 1
        if (i, prev, ct, k) in dct:
            return dct[(i, prev, ct, k)]
        res = float("inf")
        if s[i] == prev:
            # Option 1: extend the run
            option1 = self.dp(i+1, s, prev, k, ct+1, n, dct)
            # Option 2: remove the current character
            option2 = self.dp(i+1, s, prev, k-1, ct, n, dct)
            res = min(option1, option2)
        else:
            # Option 1: break the run and start a new one
            # First, account for the current run (prev, ct)
            if ct == 0:
                cost_prev = 0
            elif ct == 1:
                cost_prev = 1
            else:
                cost_prev = len(str(ct)) + 1
            option1 = cost_prev + self.dp(i+1, s, s[i], k, 1, n, dct)
            # Option 2: remove the current character
            option2 = self.dp(i+1, s, prev, k-1, ct, n, dct)
            res = min(option1, option2)
        dct[(i, prev, ct, k)] = res
        return res

    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        # We start with no previous character and count 0, and k removals.
        # But note: the initial state: i=0, prev="", ct=0, k=k.
        return self.dp(0, s, "", k, 0, n, {})
