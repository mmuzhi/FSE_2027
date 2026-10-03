class Solution:
    def componentValue(self, nums: List[int], edges: List[List[int]]) -> int:
        n = len(nums)
        tree = [[] for _ in range(n)]
        for u, v in edges:
            tree[u].append(v)
            tree[v].append(u)
        
        total = sum(nums)
        if total == 0:
            return 0
        
        parent = [-1] * n
        order = []
        stack = [0]
        while stack:
            u = stack.pop()
            order.append(u)
            for v in tree[u]:
                if v == parent[u]:
                    continue
                parent[v] = u
                stack.append(v)
        
        subtree_sum = [0] * n
        for i in range(len(order)-1, -1, -1):
            u = order[i]
            s = nums[u]
            for v in tree[u]:
                if v == parent[u]:
                    continue
                s += subtree_sum[v]
            subtree_sum[u] = s
        
        ans = 0
        for cand in range(1, total//2 + 1):
            if total % cand != 0:
                continue
            # Check if the tree can be split into components of sum cand.
            def dfs(u, p):
                s = nums[u]
                for v in tree[u]:
                    if v == p:
                        continue
                    child_sum = dfs(v, u)
                    if child_sum == -1:
                        return -1
                    s += child_sum
                if s % cand != 0:
                    return -1
                return s // cand
            
            if dfs(0, -1) == 1:
                ans = max(ans, total // cand)
        
        return ans