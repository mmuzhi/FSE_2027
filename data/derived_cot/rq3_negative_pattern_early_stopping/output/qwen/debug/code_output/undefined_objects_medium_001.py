from typing import List
from collections import deque, defaultdict

class Solution:
    def reachableNodes(self, n: int, edges: List[List[int]], restricted: List[int]) -> int:
        adj_list = defaultdict(list)
        for x, y in edges:
            adj_list[x].append(y)
            adj_list[y].append(x)
        
        if 0 not in adj_list:
            adj_list[0] = []
        
        que = deque()
        que.append(0)
        result = 0
        visited = set()
        for node in restricted:
            visited.add(node)
        
        while que:
            cur = que.popleft()
            if cur in visited:
                continue
            visited.add(cur)
            result += 1
            for neighbor in adj_list[cur]:
                que.append(neighbor)
        
        return result