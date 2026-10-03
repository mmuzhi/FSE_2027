from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        mem = defaultdict(int)

        def dfs(i: int, j: int = 0) -> int:
            if i == len(s):
                return 1
            if (i, j) in mem:
                return mem[(i, j)]

            total = 0
            if s[i] == 'D':
                for r in range(0, j):          # r in [0, j-1]
                    total = (total + dfs(i+1, r)) % MOD
            else:  # 'I'
                for r in range(j+1, i+2):      # r in [j+1, i+1]
                    total = (total + dfs(i+1, r)) % MOD

            mem[(i, j)] = total
            return total

        return dfs(0)