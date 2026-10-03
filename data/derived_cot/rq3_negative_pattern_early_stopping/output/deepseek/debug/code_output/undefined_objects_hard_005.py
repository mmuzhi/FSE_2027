from typing import List

class Solution:
    def countSubgraphsForEachDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u-1].append(v-1)
            adj[v-1].append(u-1)

        def comb(p, q):
            if len(q) < len(p):
                p, q = q, p
            res = [0] * len(q)
            for i in range(1, len(p)):
                p[i] += p[i-1]
            for i in range(1, len(q)):
                q[i] += q[i-1]
            res[0] = p[0] * q[0]
            for i in range(1, len(p)):
                res[i] = p[i] * q[i] - p[i-1] * q[i-1]
            for i in range(len(p), len(q)):
                res[i] = (q[i] - q[i-1]) * p[-1]
            return res

        def dfs(r, p):
            d = [1]   # depth 0: just the node itself
            for v in adj[r]:
                if v == p:
                    continue
                t = [1] + dfs(v, r)   # branch from r: depth 0 (not taken) or depths >=1
                d = comb(t, d)
            return d

        ans = [0] * n   # ans[d] = count of subgraphs with diameter d

        for u, v in edges:
            u -= 1
            v -= 1
            pu = dfs(u, v)
            pv = dfs(v, u)
            for i in range(min(len(pu), len(pv))):
                ans[2*i+1] += pu[i] * pv[i]

        for v in range(n):
            branches = []          # list of distributions for each neighbour
            for u in adj[v]:
                child = dfs(u, v)   # depths from u
                br = [0] * (len(child) + 1)
                br[0] = 1
                for i in range(1, len(child)+1):
                    br[i] = child[i-1]
                branches.append(br)
            if not branches:
                continue

            maxK = max(len(br)-1 for br in branches)
            pref = []
            for br in branches:
                psum = [0] * (maxK+1)
                s = 0
                for d in range(maxK+1):
                    if d < len(br):
                        s += br[d]
                    psum[d] = s
                pref.append(psum)

            total_prod = [1] * (maxK+1)
            for d in range(maxK+1):
                prod = 1
                for psum in pref:
                    prod *= psum[d]
                total_prod[d] = prod

            for k in range(1, maxK+1):
                total = total_prod[k]
                total_prev = total_prod[k-1]
                single = 0
                for idx, br in enumerate(branches):
                    brk = br[k] if k < len(br) else 0
                    if brk == 0:
                        continue
                    other_prod = total_prod[k-1] // pref[idx][k-1]
                    single += brk * other_prod
                cnt = total - total_prev - single
                ans[2*k] += cnt

        return ans[1:]   # diameters 1 .. n-1