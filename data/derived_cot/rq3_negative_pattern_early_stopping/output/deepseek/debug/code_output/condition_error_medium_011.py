class Solution:
    def numWays(self, s: str) -> int:
        MOD = 10**9 + 7
        N = len(s)
        c1 = s.count('1')
        if c1 == 0:
            return ((N-1)*(N-2)//2) % MOD
        if c1 % 3 != 0:
            return 0
        
        ones = [i for i, ch in enumerate(s) if ch == '1']
        k = c1 // 3
        
        i1 = ones[k-1]          # index of k-th '1'
        i2 = ones[k]            # index of (k+1)-th '1'
        
        j1 = ones[2*k-1]        # index of 2k-th '1'
        j2 = ones[2*k]          # index of (2k+1)-th '1'
        
        first_gap = i2 - i1
        second_gap = j2 - j1
        
        return (first_gap * second_gap) % MOD