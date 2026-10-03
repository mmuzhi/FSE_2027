class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        graph = [[] for _ in range(n)]
        for i, j in edges:
            graph[i].append(j)
            graph[j].append(i)
            
        parent_arr = [-1] * n
        level_arr = [-1] * n
        
        stack = [0]
        parent_arr[0] = -1
        level_arr[0] = 0
        while stack:
            node = stack.pop()
            for neighbor in graph[node]:
                if neighbor == parent_arr[node]:
                    continue
                parent_arr[neighbor] = node
                level_arr[neighbor] = level_arr[node] + 1
                stack.append(neighbor)
        
        def lca(a, b):
            if level_arr[a] < level_arr[b]:
                a, b = b, a
            d = level_arr[a] - level_arr[b]
            while d:
                a = parent_arr[a]
                d -= 1
            if a == b:
                return a
            while a != b:
                a = parent_arr[a]
                b = parent_arr[b]
            return a
        
        freq = [0] * n
        for trip in trips:
            u, v = trip[0], trip[1]
            w = lca(u, v)
            while u != w:
                freq[u] += 1
                u = parent_arr[u]
            freq[w] += 1
            while v != w:
                freq[v] += 1
                v = parent_arr[v]
        
        def dfs_dp(i, p):
            state0 = (price[i] // 2) * freq[i] if freq[i] > 0 else 0
            state1 = price[i] * freq[i] if freq[i] > 0 else 0
            for neighbor in graph[i]:
                if neighbor == p:
                    continue
                child0, child1 = dfs_dp(neighbor, i)
                state0 += min(child0, child1)
                state1 += child0
            return (state0, state1)
        
        state0, state1 = dfs_dp(0, -1)
        return min(state0, state1)