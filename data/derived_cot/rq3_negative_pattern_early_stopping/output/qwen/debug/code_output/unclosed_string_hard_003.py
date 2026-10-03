class Solution:
    def dp(self, i, s, prev, k, ct, n, dct):
        if k < 0:
            return float("inf")
        if i >= n:
            if ct == 0:
                return 0
            if ct == 1:
                return 1
            else:
                return len(str(ct)) + 1
        
        if (i, prev, k, ct) in dct:
            return dct[(i, prev, k, ct)]
        
        res = float('inf')
        
        # Option 1: Remove the current character
        if k > 0:
            res = min(res, self.dp(i+1, s, prev, k-1, ct, n, dct))
        
        # Option 2: Keep the current character
        if s[i] == prev:
            res = min(res, self.dp(i+1, s, prev, k, ct+1, n, dct))
        else:
            # If we have a current run (ct>0), we need to account for it and then start a new run
            if ct > 0:
                cost_here = len(str(ct)) + 1 if ct > 1 else 1
                res = min(res, cost_here + self.dp(i+1, s, s[i], k, 1, n, dct))
            else:
                res = min(res, self.dp(i+1, s, s[i], k, 1, n, dct))
        
        dct[(i, prev, k, ct)] = res
        return res

    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        return self.dp(0, s, "", k, 0, n, {})