from typing import List

class Solution:
    def minimumFuelCost(self, roads: List[List[int]], seats: int) -> int:
        adjacencyList = [[] for _ in range(len(roads) + 1)]

        for road in roads:
            adjacencyList[road[0]].append(road[1])
            adjacencyList[road[1]].append(road[0])

        visited = [0] * (len(roads) + 1)
        visited[0] = 1
        res = [0]

        def dfs(node: int, visited: List[int]) -> int:
            if visited[node] == 1:
                return 0

            visited[node] = 1
            total = 1

            for neighbor in adjacencyList[node]:
                total += dfs(neighbor, visited)

            res[0] += (total + seats - 1) // seats
            return total

        for neighbor in adjacencyList[0]:
            dfs(neighbor, visited)

        return res[0]