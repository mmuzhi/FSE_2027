from collections import deque
from typing import List

class Solution:
    def frogPosition(self, n: int, edges: List[List[int]], t: int, target: int) -> float:
        if not edges:
            return 1.0 if target == 1 else 0.0

        g = [[] for _ in range(n + 1)]
        for u, v in edges:
            g[u].append(v)
            g[v].append(u)

        visited = [False] * (n + 1)
        q = deque()
        q.append((1, 1.0))          # (node, probability)
        visited[1] = True

        for _ in range(t):
            level_size = len(q)
            stays = []
            for _ in range(level_size):
                node, prob = q.popleft()
                children = [nei for nei in g[node] if not visited[nei]]
                cnt = len(children)
                if cnt == 0:
                    stays.append((node, prob))
                else:
                    for nei in children:
                        visited[nei] = True
                        q.append((nei, prob / cnt))
            q.extend(stays)

        for node, prob in q:
            if node == target:
                return prob
        return 0.0