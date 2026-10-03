class Solution:
    def getLengthOfOptimalCompression(self, s: str, k: int) -> int:
        n = len(s)
        
        from functools import lru_cache
        
        @lru_cache(maxsize=None)
        def dp(i, prev, ct, k):
            if k < 0:
                return float('inf')
            if i >= n:
                if ct == 0:
                    return 0
                return len(str(ct)) + 1
            
            res = float('inf')
            # Option 1: Skip the current character (remove it)
            res = min(res, dp(i+1, prev, ct, k-1))
            
            # Option 2: Keep the current character
            if s[i] == prev:
                res = min(res, dp(i+1, prev, ct+1, k))
            else:
                res = min(res, dp(i+1, s[i], 1, k) + (len(str(ct)) + 1 if ct > 1 else 1 if ct == 1 else 0))
            
            return res
        
        return dp(0, '', 0, k)
