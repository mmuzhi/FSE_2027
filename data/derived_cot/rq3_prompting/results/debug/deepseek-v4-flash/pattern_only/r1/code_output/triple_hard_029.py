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

        def dfs(u: int, l: int, p: int) -> None:
            level[u] = l
            parent[u] = p
            for v in g[u]:
                if v != p:
                    dfs(v, l + 1, u)

        def lca(u: int, v: int) -> int:
            if level[u] > level[v]:
                u, v = v, u
            d = level[v] - level[u]
            while d:
                v = parent[v]
                d -= 1
            if u == v:
                return u
            while u != v:
                u = parent[u]
                v = parent[v]
            return u

        dfs(0, 0, -1)

        for u, v in trips:
            w = lca(u, v)
            x, y = u, v
            while x != w:
                freq[x] += 1
                x = parent[x]
            while y != w:
                freq[y] += 1
                y = parent[y]
            freq[w] += 1

        def dp(u: int, p: int) -> List[int]:
            res0 = 0
            res1 = (price[u] - price[u] // 2) * freq[u]
            for v in g[u]:
                if v != p:
                    child = dp(v, u)
                    res0 += max(child)
                    res1 += child[0]
            return [res0, res1]

        total = sum(freq[i] * price[i] for i in range(n))
        return total - max(dp(0, -1))