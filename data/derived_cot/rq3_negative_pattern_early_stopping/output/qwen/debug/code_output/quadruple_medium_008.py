from collections import deque
from typing import List, Dict, Tuple

class Solution:
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        INF = float('inf')
        n = len(edges)  # We assume edges is a list of length n (number of nodes) and edges[i] is the neighbor of node i, or -1 if none.
        # But note: the graph might not be connected, so we need to consider only nodes reachable from node1 and node2.

        # We'll do BFS from node1 and node2 separately.

        # BFS function
        def bfs(start):
            dist = [-1] * n
            q = deque()
            q.append(start)
            dist[start] = 0
            while q:
                cur = q.popleft()
                neighbor = edges[cur]
                if neighbor != -1 and dist[neighbor] == -1:
                    dist[neighbor] = dist[cur] + 1
                    q.append(neighbor)
            return dist

        dist1 = bfs(node1)
        dist2 = bfs(node2)

        ans = -1
        min_max_dist = INF

        for i in range(n):
            d1 = dist1[i]
            d2 = dist2[i]
            if d1 == -1 or d2 == -1:
                continue
            max_dist = max(d1, d2)
            if max_dist < min_max_dist:
                min_max_dist = max_dist
                ans = i
            elif max_dist == min_max_dist and i < ans:
                ans = i

        return ans