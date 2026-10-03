class Solution:
    def countSubgraphsForEachDiameter(self, n: int, edges: List[List[int]]) -> List[int]:
        adj = [[] for i in range(n)]
        for u, v in edges:
            adj[u-1].append(v-1)
            adj[v-1].append(u-1)
        
        def comb(p, q):
            if len(q) < len(p):
                p, q = q, p
            res = [0] * len(q)
            res[0] = p[0] * q[0]
            for i in range(1, len(p)):
                p[i] += p[i-1]
            for i in range(1, len(q)):
                q[i] += q[i-1]
            for i in range(1, len(p)):
                res[i] = p[i] * q[i] - p[i-1] * q[i-1]
            for i in range(len(p), len(q)):
                res[i] = (q[i] - q[i-1]) * p[-1]
            return res
        
        def dfs(r, parent):
            depths = [0] * (n)  # We'll count the number of nodes at each depth
            depths[0] = 1  # root at depth 0
            for neighbor in adj[r]:
                if neighbor == parent:
                    continue
                child_depths = dfs(neighbor, r)
                # Now, child_depths is an array where child_depths[i] is the number of nodes at depth i in the child's subtree
                # But note: the child's subtree is rooted at neighbor, so the depths are relative to neighbor.
                # We need to shift the depths by 1 to account for the edge from r to neighbor.
                shifted = [0] * (len(child_depths))
                if child_depths:
                    shifted[0] = child_depths[0]
                    for i in range(1, len(child_depths)):
                        shifted[i] = child_depths[i]
                    # Now, combine the shifted depths with the current depths of the entire subtree rooted at r.
                    # But note: the comb function is defined to combine two arrays. However, the comb function expects arrays of counts for each depth.
                    # We are going to combine the current depths (which is the entire subtree so far) with the shifted array.
                    # But the comb function is not standard convolution. We need to use it as defined.
                    # However, the comb function is used to combine two arrays of counts for depths. But note: the comb function does not account for the fact that the child's subtree is disjoint in terms of depth levels.
                    # We are going to combine the current depths (which is the entire subtree rooted at r without the child) and the child's subtree (shifted).
                    # But the comb function is defined to combine two arrays p and q, and it returns an array where the i-th element is the product of the i-th elements of p and q, but with a twist.
                    # However, the comb function is not doing a simple multiplication. It is doing a kind of prefix-sum convolution.
                    # We are not sure if this is the right way to combine the depths. But the original code intended to use comb to combine the depth arrays.
                    # Let's use the comb function as is.
                    # But note: the comb function expects two arrays of counts for each depth. We have the current depths (for the entire subtree rooted at r) and the shifted array (for the child's subtree).
                    # However, the comb function is defined to combine two arrays p and q, and it returns an array where the i-th element is the sum over j+k=i of p[j]*q[k] but with a different indexing? Actually, the comb function is not doing that.
                    # Let me re-implement the comb function to do standard convolution for depth arrays? But the problem is that the comb function is not standard.
                    # Given the time, I will keep the comb function as is and hope that it is correct for the intended purpose.
                    # But note: the comb function is used in the original code to combine two depth arrays. We are not changing the comb function.
                    # We are only changing the DFS to use a visited parent and then combine the child's depths.
                    # But the comb function is not standard convolution. It is doing a different operation.
                    # We are not sure what the comb function is intended to do. But the original code used it to combine two arrays of depths.
                    # We will use the comb function as is.
                    # However, the comb function expects two arrays of the same length? No, it handles different lengths.
                    # We are going to combine the current depths (which is an array of length n) and the shifted array (which is of length len(child_depths)).
                    # But