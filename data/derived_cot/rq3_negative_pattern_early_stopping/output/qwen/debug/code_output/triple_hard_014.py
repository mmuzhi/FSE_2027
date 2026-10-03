class Solution:
    def dp(self, i, s, prev, k, ct, n, dct):
        if k < 0:
            return float('inf')
        if i >= n:
            # Base case: we are at the end of the string, account for the current group
            if ct == 0:
                return 0
            if ct == 1:
                return 1
            return 1 + len(str(ct))
        if (i, prev, ct, k) in dct:
            return dct[(i, prev, ct, k)]
        
        # Option 1: Skip the current character (remove it)
        res = self.dp(i+1, s, prev, k-1, ct, n, dct)
        
        # Option 2: Keep the current character
        if s[i] == prev:
            # We are continuing the current group
            res = min(res, self.dp(i+1, s, prev, k, ct+1, n, dct))
        else:
            # We break the current group (if any) and start a new group with the current character
            if ct > 0:
                # Account for the current group and then start a new group
                cost = 1 + len(str(ct)) if ct > 1 else 1
                res = min(res, cost + self.dp(i+1, s, s[i], k, 1, n, dct))
            else:
                # No current group, so just start a new group
                res = min(res, self.dp(i+1, s, s[i], k, 1, n, dct))
        
        dct[(i, prev, ct, k)] = res
        return res

    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        # Start with no previous character and count 0
        return self.dp(0, s, "", k, 0, n, {})
