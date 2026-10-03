from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        MOD = 10**9 + 7
        n = len(s)
        memo = defaultdict(int)

        def dfs(pos: int, less: int) -> int:
            if pos == n:
                return 1
            key = (pos, less)
            if key in memo:
                return memo[key]
            total = 0
            if s[pos] == 'D':
                for new_less in range(less):
                    total = (total + dfs(pos + 1, new_less)) % MOD
            else:
                for new_less in range(less, n - pos):
                    total = (total + dfs(pos + 1, new_less)) % MOD
            memo[key] = total
            return total

        ans = 0
        for first_less in range(n + 1):
            ans = (ans + dfs(0, first_less)) % MOD
        return ans