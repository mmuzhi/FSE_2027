from typing import List

class Solution:
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        n = len(nums)
        tree = [[] for _ in range(n)]
        for u, v in edges:
            tree[u].append(v)
            tree[v].append(u)
        
        total = sum(nums)
        
        def dfs(u: int, p: int, cand: int) -> int:
            s = nums[u]
            for v in tree[u]:
                if v != p:
                    s += dfs(v, u, cand)
            return 0 if s == cand else s
        
        for cand in range(1, total // 2 + 1):
            if total % cand == 0 and dfs(0, -1, cand) == 0:
                return total // cand - 1
        return 0