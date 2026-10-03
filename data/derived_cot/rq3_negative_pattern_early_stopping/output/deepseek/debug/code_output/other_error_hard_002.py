from typing import List

class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for i, j in edges:
            g[i].append(j)
            g[j].append(i)

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
        for start, end in trips:
            lca = LCA(start, end)
            while start != lca:
                freq[start] += 1
                start = parent[start]
            while end != lca:
                freq[end] += 1
                end = parent[end]
            freq[lca] += 1

        total = 0
        for i in range(n):
            total += freq[i] * price[i]

        def dp(i: int, p: int) -> List[int]:
            not_halve = 0
            halve = freq[i] * (price[i] - price[i] // 2)  # reduction from halving this node
            for j in g[i]:
                if j != p:
                    child = dp(j, i)
                    not_halve += max(child[0], child[1])
                    halve += child[0]
            return [not_halve, halve]

        best_reduction = max(dp(0, -1))
        return total - best_reduction