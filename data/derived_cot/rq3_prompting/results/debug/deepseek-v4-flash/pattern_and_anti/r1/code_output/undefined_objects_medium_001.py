from collections import defaultdict, deque
from typing import List

class Solution:
    def reachableNodes(self, n: int, edges: List[List[int]], restricted: List[int]) -> int:
        adj_list = defaultdict(list)
        for x, y in edges:
            adj_list[x].append(y)
            adj_list[y].append(x)

        que = deque([0])
        result = 0
        visited = set(restricted)

        while que:
            cur = que.popleft()
            if cur in visited:
                continue

            visited.add(cur)
            result += 1

            for nxt in adj_list[cur]:
                que.append(nxt)

        return result