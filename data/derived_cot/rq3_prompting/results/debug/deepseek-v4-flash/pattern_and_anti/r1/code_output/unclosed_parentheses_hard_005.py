from typing import List
from collections import defaultdict

class Solution:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        visited = [0] * n
        pos = defaultdict(int)
        ans = -1

        for i in range(n):
            if visited[i] == 0:
                x = i
                step = 0
                path = set()

                while x != -1 and visited[x] == 0:
                    visited[x] = 1
                    pos[x] = step
                    step += 1
                    path.add(x)
                    x = edges[x]

                if x != -1 and x in path:
                    ans = max(ans, step - pos[x])

        return ans