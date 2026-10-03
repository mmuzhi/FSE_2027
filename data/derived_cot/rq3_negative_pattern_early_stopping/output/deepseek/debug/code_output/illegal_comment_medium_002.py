from typing import List

class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        n = len(roads) + 1
        adjacencyList = [[] for _ in range(n)]
        for road in roads:
            u, v = road
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)
        
        res = [0]
        visited = [0] * n
        visited[0] = 1  # capital is visited initially
        
        def dfs(i: int, visited: List[int]) -> int:
            if visited[i] == 1:
                return 0
            visited[i] = 1
            tot = 1  # count this node itself
            for k in adjacencyList[i]:
                tot += dfs(k, visited)
            res[0] += (tot + seats - 1) // seats
            return tot
        
        for neighbor in adjacencyList[0]:
            dfs(neighbor, visited)
        
        return res[0]