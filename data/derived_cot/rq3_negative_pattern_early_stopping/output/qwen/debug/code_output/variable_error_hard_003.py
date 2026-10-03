class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        cuts = sorted([0, n] + cuts)
        m = len(cuts)
        
        @lru_cache(None)
        def dfs(l, r):
            if r == l + 1:
                return 0
            min_cost = float('inf')
            for i in range(l + 1, r):
                cost = dfs(l, i) + dfs(i, r) + (cuts[r] - cuts[l])
                if cost < min_cost:
                    min_cost = cost
            return min_cost
        
        return dfs(0, m - 1)