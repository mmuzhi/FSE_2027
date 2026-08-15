from typing import List

class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for a, b in edges:
            g[a].append(b)
            g[b].append(a)

        freq = [0] * n
        level = [0] * n
        parent = [0] * n

        def dfs(u: int, l: int, p: int) -> None:
            level[u] = l
            parent[u] = p
            for v in g[u]:
                if v != p:
                    dfs(v, l + 1, u)

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
            c = LCA(a, b)
            while a != c:
                freq[a] += 1
                a = parent[a]
            freq[a] += 1
            while b != c:
                freq[b] += 1
                b = parent[b]

        def dp(u: int, p: int):
            save0 = 0
            save1 = (price[u] - price[u] // 2) * freq[u]
            for v in g[u]:
                if v == p:
                    continue
                child = dp(v, u)
                save0 += max(child)
                save1 += child[0]
            return [save0, save1]

        total = sum(price[i] * freq[i] for i in range(n))
        return total - max(dp(0, -1))