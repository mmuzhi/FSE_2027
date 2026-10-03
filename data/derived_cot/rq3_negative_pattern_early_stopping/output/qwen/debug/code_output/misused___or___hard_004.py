from collections import deque
class Solution:
    def isPossible(self, n: int, edges: List[List[int]]) -> bool:
        # Build graph and degree list
        graph = [[] for _ in range(n)]
        degree = [0] * n
        for edge in edges:
            a, b = edge
            a -= 1
            b -= 1
            graph[a].append(b)
            graph[b].append(a)
            degree[a] += 1
            degree[b] += 1
        
        # Count odd degrees
        odd_degrees = [i for i in range(n) if degree[i] % 2 == 1]
        num_odd = len(odd_degrees)
        
        # Eulerian path requires 0 or 2 odd-degree nodes
        if num_odd not in (0, 2):
            return False
        
        # If there are no edges, then we can traverse (empty graph)
        if n == 0:
            return True
        
        # Check connectivity for nodes with degree >= 1
        # We'll consider only nodes with degree >= 1
        visited = [False] * n
        # If there are no edges, then we don't need to traverse, but n==0 is handled above.
        # We'll do BFS starting from any node with degree>=1
        stack = []
        # Find the first node with degree>=1
        start = None
        for i in range(n):
            if degree[i] > 0:
                start = i
                break
        if start is None:
            # No node with edges, so graph is empty -> True
            return True
        
        # BFS
        queue = deque([start])
        visited[start] = True
        count_visited = 1
        while queue:
            node = queue.popleft()
            for neighbor in graph[node]:
                if not visited[neighbor]:
                    visited[neighbor] = True
                    count_visited += 1
                    queue.append(neighbor)
        
        # Count the number of nodes with degree>=1 that are visited
        total_nodes_with_edges = sum(1 for i in range(n) if degree[i] > 0)
        if count_visited != total_nodes_with_edges:
            return False
        
        return True