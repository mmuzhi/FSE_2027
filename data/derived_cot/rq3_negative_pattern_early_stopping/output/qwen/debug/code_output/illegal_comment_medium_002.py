class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        n = len(roads) + 1
        adjacencyList = [[] for _ in range(n)]
        for road in roads:
            u, v = road
            adjacencyList[u].append(v)
            adjacencyList[v].append(u)
        
        visited = [0] * n
        visited[0] = 1
        res = [0]
        
        def dfs(i, visited):
            if visited[i] == 1:
                return 0
            visited[i] = 1
            tot = 1
            for neighbor in adjacencyList[i]:
                tot += dfs(neighbor, visited)
            if tot % seats == 0:
                res[0] += tot // seats
            else:
                res[0] += tot // seats + 1
            return tot
        
        for neighbor in adjacencyList[0]:
            dfs(neighbor, visited)
        
        return res[0]