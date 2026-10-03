class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        if not roads:
            return 0
        
        nodes_set = set()
        for a, b in roads:
            nodes_set.add(a)
            nodes_set.add(b)
        n = max(nodes_set) + 1
        
        adjacencyList = [[] for _ in range(n)]
        for a, b in roads:
            adjacencyList[a].append(b)
            adjacencyList[b].append(a)
        
        visited = [0] * n
        visited[0] = 1
        
        res = [0]
        
        def dfs(i):
            if visited[i] == 1:
                return 0
            visited[i] = 1
            tot = 1
            for neighbor in adjacencyList[i]:
                tot += dfs(neighbor)
            buses = (tot + seats - 1) // seats
            res[0] += buses
            return tot
        
        for neighbor in adjacencyList[0]:
            dfs(neighbor)
        
        return res[0]