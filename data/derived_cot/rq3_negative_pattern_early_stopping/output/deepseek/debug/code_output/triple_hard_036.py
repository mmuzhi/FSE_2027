from collections import defaultdict

class Solution:
    def numPermsDISequence(self, s: str) -> int:
        mod = 10**9 + 7
        n = len(s)
        mem = defaultdict(int)
        
        def dfs(i: int, last_rank: int) -> int:
            if i == n:
                return 1
            key = (i, last_rank)
            if key in mem:
                return mem[key]
            total = 0
            remaining = n - i
            if s[i] == 'D':
                for next_rank in range(last_rank):
                    total = (total + dfs(i + 1, next_rank)) % mod
            else:  # 'I'
                for next_rank in range(last_rank, remaining):
                    total = (total + dfs(i + 1, next_rank)) % mod
            mem[key] = total
            return total
        
        ans = 0
        for first_rank in range(n + 1):
            ans = (ans + dfs(0, first_rank)) % mod
        return ans