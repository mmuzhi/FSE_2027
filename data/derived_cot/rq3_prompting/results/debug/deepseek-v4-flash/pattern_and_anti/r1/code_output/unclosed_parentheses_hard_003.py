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

        def dfs(i: int, l: int, p: int) -> None:
            level[i] = l
            parent[i] = p
            for j in g[i]:
                if j != p:
                    dfs(j, l + 1, i)

        def LCA(a: int, b: int) -> int:
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
            w = LCA(a, b)
            x, y = a, b
            while x != w:
                freq[x] += 1
                x = parent[x]
            freq[x] += 1
            while y != w:
                freq[y] += 1
                y = parent[y]

        def dp(i: int, p: int):
            not_halved = price[i] * freq[i]
            halved = price[i] * freq[i] // 2

            for j in g[i]:
                if j != p:
                    child_not, child_halved = dp(j, i)
                    not_halved += min(child_not, child_halved)
                    halved += child_not

            return [not_halved, halved]

        return min(dp(0, -1))