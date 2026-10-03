import sys
sys.setrecursionlimit(300000)

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); q = int(next(it))
    A = [0] * (n+1)
    for i in range(2, n+1):
        A[i] = int(next(it))
    
    # Precompute factorials and inverse factorials up to n (for combinations)
    max_n = n
    fact = [1] * (max_n+1)
    inv_fact = [1] * (max_n+1)
    for i in range(1, max_n+1):
        fact[i] = fact[i-1] * i % MOD
    inv_fact[max_n] = pow(fact[max_n], MOD-2, MOD)
    for i in range(max_n, 0, -1):
        inv_fact[i-1] = inv_fact[i] * i % MOD

    # Precompute the number of ways to choose parent for each node (which is (i-1) for node i)
    # But we need to compute the probability that an edge is on the path between u and v.

    # Actually, we can use the following idea:
    # The total number of trees is (n-1)! (since for node i, there are i-1 choices, and independent).
    # Now, for a fixed edge (i, parent) to be on the path from u to v, two conditions must hold:
    # 1. The edge must be on the path from u to the root (if u is in the subtree of i) or from v to the root (if v is in the subtree of i) but actually, the edge is between i and its parent. The edge is used in the path from u to v if and only if the parent of i is an ancestor of both u and v, and i is an ancestor of one of them (or vice versa). Actually, the edge (i, parent) is used if the path from u to v goes through i and parent. But note: the edge is from i to parent, so if u is in the subtree of i and v is in the subtree of parent but not i, then the edge is used? Actually, the edge is used if the path from u to v goes through i and parent. But the path from u to v is from u to LCA and then to v. The edge (i, parent) is used if i is on the path from u to LCA or from LCA to v.

    # Alternatively, we can use the concept of "rooted tree" and the fact that the parent of each node is chosen independently. The edge (i, parent) is present in the tree if the parent of i is chosen as that node. The condition for the edge to be on the path from u to v is that the edge is between the two parts of the path.

    # Actually, a better approach is to use the following known technique for such problems (sum over all trees):

    # The total distance between u and v over all trees is the sum over all edges (i, parent) of (A_i * (number of trees that contain the edge (i, parent) in the path from u to v)).

    # Now, how to compute the number of trees that contain the edge (i, parent) in the path from u to v?

    # Condition: The edge (i, parent) must be on the path from u to v. This happens if and only if:
    #   - The edge is on the path from u to the root (if u is in the subtree of i) and the edge is also on the path from v to the root (if v is in the subtree of parent) but actually, the edge is between i and parent, so the path from u to v must go through i and parent. This is equivalent to: the edge is on the path from u to the root and the edge is on the path from v to the root, but that would be if u and v are in different subtrees of the parent? Actually, the edge (i, parent) is used if one of u or v is in the subtree of i and the other is in the subtree of parent (but not i). 

    # Actually, the edge (i, parent) is used in the path from u to v if and only if the two nodes u and v are separated by the edge. That is, one is in the subtree of i and the other is in the subtree of parent (the parent of i). 

    # But note: the tree is rooted at 1, and the parent of i is chosen from 1 to i-1. The edge (i, parent) divides the tree