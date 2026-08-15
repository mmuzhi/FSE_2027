from typing import List
from collections import deque

class Solution:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        graph = [[] for _ in range(n)]
        indegrees = [0] * n

        for src, dest in edges:
            graph[src].append(dest)
            indegrees[dest] += 1

        ans = [set() for _ in range(n)]
        q = deque(i for i in range(n) if indegrees[i] == 0)

        while q:
            cur = q.popleft()
            for nxt in graph[cur]:
                ans[nxt].add(cur)
                ans[nxt].update(ans[cur])
                indegrees[nxt] -= 1
                if indegrees[nxt] == 0:
                    q.append(nxt)

        return [sorted(s) for s in ans]