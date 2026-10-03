from collections import deque
from typing import List

class Solution:
    def numberOfComponents(self, properties: List[List[int]], k: int) -> int:
        n = len(properties)
        if n == 0:
            return 0
        
        prop_sets = [set(props) for props in properties]
        graph = [[] for _ in range(n)]
        
        for i in range(n):
            for j in range(i+1, n):
                common_count = len(prop_sets[i] & prop_sets[j])
                if common_count >= k:
                    graph[i].append(j)
                    graph[j].append(i)
        
        visited = [False] * n
        components = 0
        
        for i in range(n):
            if not visited[i]:
                components += 1
                queue = deque([i])
                visited[i] = True
                while queue:
                    node = queue.popleft()
                    for neighbor in graph[node]:
                        if not visited[neighbor]:
                            visited[neighbor] = True
                            queue.append(neighbor)
        return components