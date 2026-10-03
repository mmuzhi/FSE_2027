from typing import List

class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        n = len(roads) + 1
        adj = [[] for _ in range(n)]
        for u, v in roads:
            adj[u].append(v)
            adj[v].append(u)

        res = 0

        def dfs(node: int, parent: int) -> int:
            nonlocal res
            people = 1
            for nei in adj[node]:
                if nei != parent:
                    people += dfs(nei, node)
            if node != 0:
                res += (people + seats - 1) // seats
            return people

        dfs(0, -1)
        return res