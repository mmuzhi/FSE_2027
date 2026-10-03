from typing import List
from functools import lru_cache

class Solution:
    def ways(self, pizza: List[str], k: int) -> int:
        MOD = 1000000007
        rows = len(pizza)
        cols = len(pizza[0])
        
        pre = [[0] * cols for _ in range(rows)]
        for i in range(rows):
            for j in range(cols):
                top = pre[i-1][j] if i > 0 else 0
                left = pre[i][j-1] if j > 0 else 0
                diag = pre[i-1][j-1] if i > 0 and j > 0 else 0
                pre[i][j] = top + left - diag + (1 if pizza[i][j] == 'A' else 0)
        
        def has_apple(r1, c1, r2, c2):
            """Check if sub-rectangle (r1,c1) to (r2,c2) inclusive has at least one apple."""
            total = pre[r2][c2]
            if r1 > 0:
                total -= pre[r1-1][c2]
            if c1 > 0:
                total -= pre[r2][c1-1]
            if r1 > 0 and c1 > 0:
                total += pre[r1-1][c1-1]
            return total > 0
        
        @lru_cache(None)
        def dfs(r, c, k):
            if k == 1:
                return 1 if has_apple(r, c, rows-1, cols-1) else 0
            
            res = 0
            for i in range(r, rows-1):
                if has_apple(r, c, i, cols-1):
                    res = (res + dfs(i+1, c, k-1)) % MOD
            for j in range(c, cols-1):
                if has_apple(r, c, rows-1, j):
                    res = (res + dfs(r, j+1, k-1)) % MOD
            return res
        
        if pre[rows-1][cols-1] < k:
            return 0
        return dfs(0, 0, k)