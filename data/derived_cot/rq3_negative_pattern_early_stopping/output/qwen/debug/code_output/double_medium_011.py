from collections import deque

class Solution:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        graph = [[] for _ in range(n)]
        indegrees = [0] * n
        
        for edge in edges:
            src, dest = edge
            graph[src].append(dest)
            indegrees[dest] += 1
        
        ans = [set() for _ in range(n)]
        queue = deque()
        
        for i in range(n):
            if indegrees[i] == 0:
                queue.append(i)
                
        while queue:
            cur = queue.popleft()
            for neighbor in graph[cur]:
                ans[neighbor].add(cur)
                ans[neighbor].update(ans[cur])
                indegrees[neighbor] -= 1
                if indegrees[neighbor] == 0:
                    queue.append(neighbor)
                    
        result = []
        for s in ans:
            result.append(sorted(list(s)))
            
        return result