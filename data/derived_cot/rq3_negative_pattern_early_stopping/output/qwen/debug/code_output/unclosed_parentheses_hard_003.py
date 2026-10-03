class Solution:
    def minimumTotalPrice(self, n: int, edges: List[List[int]], price: List[int], trips: List[List[int]]) -> int:
        g = [[] for _ in range(n)]
        for i, j in edges:
            g[i].append(j)
            g[j].append(i)
            
        freq = [0] * n
        parent_arr = [0] * n
        level_arr = [0] * n
        
        stack = [0]
        parent_arr[0] = -1
        while stack:
            node = stack.pop()
            for neighbor in g[node]:
                if neighbor == parent_arr[node]:
                    continue
                parent_arr[neighbor] = node
                level_arr[neighbor] = level_arr[node] + 1
                stack.append(neighbor)
                
        def lca(a, b):
            if level_arr[a] < level_arr[b]:
                a, b = b, a
            while level_arr[a] > level_arr[b]:
                a = parent_arr[a]
            if a == b:
                return a
            while a != b:
                a = parent_arr[a]
                b = parent_arr[b]
            return a
        
        for i, j in trips:
            l = lca(i, j)
            x = i
            while x != l:
                freq[x] += 1
                x = parent_arr[x]
            freq[l] += 1
            x = j
            while x != l:
                freq[x] += 1
                x = parent_arr[x]
        
        def dp(i, p):
            dp0 = price[i] * freq[i]
            dp1 = (price[i] * freq[i]) // 2
            for j in g[i]:
                if j == p:
                    continue
                child0, child1 = dp(j, i)
                dp0 += min(child0, child1)
                dp1 += min(child0, child1)
            return (dp0, dp1)
        
        dp0, dp1 = dp(0, -1)
        return min(dp0, dp1)