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

        def lca(u, v):
            if level[u] < level[v]:
                u, v = v, u
            diff = level[u] - level[v]
            while diff:
                u = parent[u]
                diff -= 1
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
            freq[w] += 1
            while y != w:
                freq[y] += 1
                y = parent[y]

        def dp(u, p):
            not_half = price[u] * freq[u]
            half = price[u] * freq[u] // 2

            for v in g[u]:
                if v != p:
                    child_not, child_half = dp(v, u)
                    not_half += min(child_not, child_half)
                    half += child_not

            return [not_half, half]

        return min(dp(0, -1))