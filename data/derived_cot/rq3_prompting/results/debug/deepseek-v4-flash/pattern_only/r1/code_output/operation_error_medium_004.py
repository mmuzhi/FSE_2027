from typing import List

class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        n = len(roads) + 1
        graph = [[] for _ in range(n)]
        for u, v in roads:
            graph[u].append(v)
            graph[v].append(u)

        parent = [-1] * n
        visited = [False] * n
        order = []
        stack = [0]
        visited[0] = True

        while stack:
            node = stack.pop()
            order.append(node)
            for nxt in graph[node]:
                if not visited[nxt]:
                    visited[nxt] = True
                    parent[nxt] = node
                    stack.append(nxt)

        subtree = [1] * n
        ans = 0

        for node in reversed(order):
            if node == 0:
                continue
            ans += (subtree[node] + seats - 1) // seats
            subtree[parent[node]] += subtree[node]

        return ans