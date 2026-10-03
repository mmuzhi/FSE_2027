from collections import deque
from typing import List

class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for i, j in edges:
            g[i].append(j)
            g[j].append(i)
        
        parent = [-1] * n
        level = [0] * n
        q = deque([0])
        parent[0] = -1
        while q:
            u = q.popleft()
            for v in g[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                level[v] = level[u] + 1
                q.append(v)
        
        def LCA(a, b):
            if level[a] < level[b]:
                a, b = b, a
            while level[a] != level[b]:
                a = parent[a]
            if a == b:
                return a
            while parent[a] != parent[b]:
                a = parent[a]
                b = parent[b]
            return parent[a]
        
        freq = [0] * n
        for a, b in trips:
            lca = LCA(a, b)
            while a != lca:
                freq[a] += 1
                a = parent[a]
            freq[lca] += 1
            while b != lca:
                freq[b] += 1
                b = parent[b]
        
        dp0 = [0] * n
        dp1 = [0] * n
        order = []
        stack = [0]
        while stack:
            u = stack.pop()
            order.append(u)
            for v in g[u]:
                if v == parent[u]:
                    continue
                stack.append(v)
        for u in order[::-1]:
            dp0[u] = price[u] * (freq[u] % 2)
            dp1[u] = (price[u] * (freq[u] - 1)) // 2
            for v in g[u]:
                if v == parent[u]:
                    continue
                dp0[u] += min(dp0[v], dp1[v])
                dp1[u] += min(dp0[v], dp1[v])
        
        return min(dp0[0], dp1[0])