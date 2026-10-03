class Solution:
    def numWays(self, s: str) -> int:
        MOD = 10**9 + 7
        N = len(s)
        c1 = s.count('1')
        if c1 == 0:
            return ((N - 1) * (N - 2) // 2) % MOD
        if c1 % 3 != 0:
            return 0
        k = c1 // 3
        A = []
        for i, char in enumerate(s):
            if char == '1':
                A.append(i)
        return (A[k] - A[k-1]) * (A[2*k] - A[2*k-1]) % MOD