from collections import deque
from typing import List


class Solution:
    def getAncestors(self, n: int, edges: List[List[int]]) -> List[List[int]]:
        graph = [[] for _ in range(n)]
        indegrees = [0] * n

        for edge in edges:
            src, dest = edge[0], edge[1]
            graph[src].append(dest)
            indegrees[dest] += 1

        queue = deque()
        ans = [set() for _ in range(n)]

        for i in range(len(indegrees)):
            if indegrees[i] == 0:
                queue.append(i)

        while queue:
            cur = queue.popleft()

            for neighbor in graph[cur]:
                # current node is ancestor to each and every neighboring node!
                ans[neighbor].add(cur)
                # every ancestor of current node is also an ancestor to the neighboring node!
                ans[neighbor].update(ans[cur])
                indegrees[neighbor] -= 1
                if indegrees[neighbor] == 0:
                    queue.append(neighbor)

        # at the end, we should have the set of ancestors for each and every node!
        # in the worst case, all vertices could be ancestors of node i, so sort each set
        ans = [sorted(list(s)) for s in ans]
        return ans