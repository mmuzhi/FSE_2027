from typing import List

class Solution:
    def longestCycle(self, edges: List[int]) -> int:
        n = len(edges)
        visited = [0] * n
        ans = -1

        for i in range(n):
            if visited[i]:
                continue

            pos = {}
            cur = i
            dist = 0

            while cur != -1 and not visited[cur]:
                visited[cur] = 1
                pos[cur] = dist
                dist += 1
                cur = edges[cur]

            if cur != -1 and cur in pos:
                ans = max(ans, dist - pos[cur])

        return ans