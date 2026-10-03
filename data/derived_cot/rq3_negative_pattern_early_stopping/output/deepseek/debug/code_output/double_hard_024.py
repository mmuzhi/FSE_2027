class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for i, j in edges:
            g[i].append(j)
            g[j].append(i)
            
        freq = [0] * n
        level = [0] * n
        parent = [0] * n
        
        def dfs(i, l, p):
            level[i] = l
            parent[i] = p
            for j in g[i]:
                if j != p:
                    dfs(j, l + 1, i)
        
        def LCA(a, b):
            if level[a] > level[b]:
                a, b = b, a
            d = level[b] - level[a]
            while d:
                b = parent[b]
                d -= 1
            if a == b:
                return a
            while a != b:
                a = parent[a]
                b = parent[b]
            return a
        
        dfs(0, 0, -1)
        for a, b in trips:
            lca = LCA(a, b)
            while a != lca:
                freq[a] += 1
                a = parent[a]
            freq[lca] += 1
            while b != lca:
                freq[b] += 1
                b = parent[b]
        
        def dp(i, p):
            res0 = price[i] * freq[i]          # not halved
            res1 = (price[i] // 2) * freq[i]   # halved
            for j in g[i]:
                if j != p:
                    child_dp = dp(j, i)
                    res0 += min(child_dp)       # i not halved, child can be either
                    res1 += child_dp[0]         # i halved, child cannot be halved
            return [res0, res1]
        
        return min(dp(0, -1))