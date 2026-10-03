class Solution:
    def numPermsDISequence(self, s: str) -> int:
        n = len(s) + 1
        mod = 10**9 + 7
        
        # dp[last_digit][mask] for the current step
        # We'll use a 2D list: 10 x 1024
        dp = [[0] * 1024 for _ in range(10)]
        
        # Initialize the first digit: for each digit d, set dp[d][mask] where mask has only the d-th bit set.
        for d in range(10):
            dp[d][1 << d] = 1
        
        # Iterate over each character in s
        for char in s:
            new_dp = [[0] * 1024 for _ in range(10)]
            for last in range(10):
                for mask in range(1024):
                    if dp[last][mask]:
                        if char == 'I':
                            # Next digit must be greater than last
                            for nxt in range(last + 1, 10):
                                if mask & (1 << nxt) == 0:
                                    new_mask = mask | (1 << nxt)
                                    new_dp[nxt][new_mask] = (new_dp[nxt][new_mask] + dp[last][mask]) % mod
                        else:  # 'D'
                            # Next digit must be less than last
                            for nxt in range(0, last):
                                if mask & (1 << nxt) == 0:
                                    new_mask = mask | (1 << nxt)
                                    new_dp[nxt][new_mask] = (new_dp[nxt][new_mask] + dp[last][mask]) % mod
            dp = new_dp
        
        # Sum over all last digits and all masks
        ans = 0
        for last in range(10):
            for mask in range(1024):
                ans = (ans + dp[last][mask]) % mod
        return ans
