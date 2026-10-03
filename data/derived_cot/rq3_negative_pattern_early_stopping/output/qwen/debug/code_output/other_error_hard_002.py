class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for i, j in edges:
            g[i].append(j)
            g[j].append(i)
            
        freq = [0] * n
        level = [0] * n
        parent_arr = [0] * n
        
        def dfs(i, l, p):
            level[i] = l
            parent_arr[i] = p
            for j in g[i]:
                if j != p:
                    dfs(j, l + 1, i)
        
        def LCA(a, b):
            if level[a] > level[b]:
                a, b = b, a
            d = level[b] - level[a]
            while d:
                b = parent_arr[b]
                d -= 1
            if a == b:
                return a
            while a != b:
                a = parent_arr[a]
                b = parent_arr[b]
            return a
        
        dfs(0, 0, -1)
        for i, j in trips:
            lca = LCA(i, j)
            while i != lca:
                freq[i] += 1
                i = parent_arr[i]
            freq[lca] += 1
            while j != lca:
                freq[j] += 1
                j = parent_arr[j]
        
        dp0 = [0] * n
        dp1 = [0] * n
        stack = [0]
        parent_arr = [-1] * n
        order = []
        while stack:
            node = stack.pop()
            order.append(node)
            for neighbor in g[node]:
                if neighbor != parent_arr[node]:
                    parent_arr[neighbor] = node
                    stack.append(neighbor)
        order.reverse()
