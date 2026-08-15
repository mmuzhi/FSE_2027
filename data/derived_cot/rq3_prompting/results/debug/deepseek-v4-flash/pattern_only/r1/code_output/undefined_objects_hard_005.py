from typing import List

class Solution:
    def countSubgraphsForEachDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u - 1].append(v - 1)
            adj[v - 1].append(u - 1)

        def comb(p, q):
            if len(q) < len(p):
                p, q = q, p
            res = [0] * len(q)
            res[0] = p[0] * q[0]

            for i in range(1, len(p)):
                p[i] += p[i - 1]
            for i in range(1, len(q)):
                q[i] += q[i - 1]

            for i in range(1, len(p)):
                res[i] = p[i] * q[i] - p[i - 1] * q[i - 1]

            for i in range(len(p), len(q)):
                res[i] = (q[i] - q[i - 1]) * p[-1]

            return res

        def dfs(r, p):
            d = [1]
            for v in adj[r]:
                if v == p:
                    continue
                t = [1] + dfs(v, r)
                d = comb(t, d)
            return d

        ans = [0] * n

        # Odd diameters: center edge
        for u, v in edges:
            u -= 1
            v -= 1
            p = dfs(u, v)
            q = dfs(v, u)
            for i in range(min(len(p), len(q))):
                ans[2 * i + 1] += p[i] * q[i]

        # Even diameters: center vertex
        for v in range(n):
            if len(adj[v]) <= 1:
                continue

            tree = [1] + dfs(adj[v][0], v)
            curr = [0] * n

            for u in adj[v][1:]:
                q = [1] + dfs(u, v)

                # Extend already counted even-diameter subtrees with a smaller branch
                j = 1
                t = q[1] + 1  # q[0] + q[1]
                for diam in range(4, n, 2):
                    r = diam // 2
                    while j + 1 < min(r, len(q)):
                        j += 1
                        t += q[j]
                    curr[diam] *= t

                # Form new even-diameter subtrees with equal branch heights
                for i in range(min(len(tree), len(q))):
                    curr[2 * i] += tree[i] * q[i]

                tree = comb(tree, q)

            for diam in range(2, n, 2):
                ans[diam] += curr[diam]

        return ans[1:]