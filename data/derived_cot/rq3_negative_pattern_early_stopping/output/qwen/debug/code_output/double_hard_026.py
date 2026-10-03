from collections import deque

class Solution:
    def isPossible(self, n: int, edges: list[list[int]]) -> bool:
        # Build graph and check connectivity
        graph = [[] for _ in range(n)]
        for edge in edges:
            a, b = edge
            a -= 1
            b -= 1
            graph[a].append(b)
            graph[b].append(a)
        
        # Check connectivity using BFS/DFS
        visited = [False] * n
        if n > 0:
            visited[0] = True
            queue = deque([0])
            while queue:
                node = queue.popleft()
                for neighbor in graph[node]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)
        
        # If the graph is not connected, then we cannot have an Eulerian trail (unless we are allowed to connect components, but the problem doesn't specify)
        # However, note: the problem might allow adding edges arbitrarily, but the graph must be connected to have an Eulerian trail.
        # But the problem does not specify if we can add edges to connect components. We'll assume that the graph must be connected.
        if not all(visited):
            return False
        
        # Count degrees
        degrees = [len(graph[i]) for i in range(n)]
        oddDegreesNodes = [i for i in range(n) if degrees[i] % 2 == 1]
        numOdd = len(oddDegreesNodes)
        
        # In an Eulerian trail, the number of odd-degree nodes must be 0 or 2.
        # But note: the Chinese Postman Problem allows fixing by adding edges (or duplicating) to make all degrees even, which requires an even number of odd-degree nodes (0, 2, 4, ...).
        # However, the problem is about making the graph Eulerian (which requires 0 odd-degree nodes). But note: an Eulerian trail requires 0 or 2 odd-degree nodes (for trail, not circuit). But wait: Eulerian trail (not circuit) requires exactly 0 or 2 odd-degree nodes.
        # But the problem says "Eulerian trail", so we require 0 or 2 odd-degree nodes.
        if numOdd == 0 or numOdd == 2:
            return True
        else:
            return False
