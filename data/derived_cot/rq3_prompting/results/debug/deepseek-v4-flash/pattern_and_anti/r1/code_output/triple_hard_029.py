from typing import List

class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        freq = [0] * n
        level = [0] * n
        parent = [0] * n

        def dfs(u, l, p):
            level[u] = l
            parent[u] = p
            for v in g[u]:
                if v != p:
                    dfs(v, l + 1, u)

        def lca(a, b):
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
            c = lca(a, b)
            x = a
            while x != c:
                freq[x] += 1
                x = parent[x]
            freq[c] += 1
            y = b
            while y != c:
                freq[y] += 1
                y = parent[y]

        def dp(u, p):
            res0 = 0
            res1 = (price[u] - price[u] // 2) * freq[u]
            for v in g[u]:
                if v != p:
                    curr = dp(v, u)
                    res0 += max(curr)
                    res1 += curr[0]
            return [res0, res1]

        ans = 0
        for i in range(n):
            ans += freq[i] * price[i]
        return ans - max(dp(0, -1))