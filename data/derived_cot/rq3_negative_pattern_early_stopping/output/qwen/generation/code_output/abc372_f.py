import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it)); m = int(next(it)); k = int(next(it))
    
    # Base edges: from i to i+1 (mod n)
    # Chords: m edges from X_i to Y_i
    chords = []
    for _ in range(m):
        x = int(next(it)); y = int(next(it))
        chords.append((x, y))
    
    # We are going to use dynamic programming with state being the vertex, but we need to optimize for large k.
    # However, note that the base graph is a cycle and the chords are few. We can use matrix exponentiation but on a reduced state space?
    # Alternatively, we can use the idea of breaking the cycle and using generating functions.

    # But note: the problem is similar to counting walks in a graph with a cycle and chords. We can use the following:

    # Let A be the adjacency matrix of the graph. Then the answer is the (1, v) entry of A^k, but we are only interested in the starting vertex 1.

    # However, n is up to 200000, so we cannot store the full matrix.

    # Another idea: use the fact that the base graph is a cycle and the chords are few. We can consider the graph as having two types of edges: the base edges and the chords.

    # We can use the following recurrence:

    # Let dp[k][v] = number of ways to reach vertex v in k steps.

    # Then:
    #   dp[0][1] = 1, else 0.
    #   For each step, dp[k][v] = (dp[k-1][v-1] (if v != 1 then from v-1 via base edge) + sum_{for each chord (u, v)} dp[k-1][u])

    # But note: the base edge from u to u+1, so to get to v, we can come from v-1 (if v != 1, then from v-1, and if v==1, then from n) via base edge.

    # However, the base edge is from u to u+1, so the reverse is: to get to v, the base edge comes from v-1 (with v-1 being modulo n, so if v=1, then from n).

    # But wait, the base edge is from i to i+1. So the reverse edge for base is from i+1 to i? No, we are moving forward. So from u, we go to u+1. So to get to v, we must have come from u such that u+1 = v, i.e., u = v-1 (with v-1 being modulo n, so if v=1, then u = n).

    # So the recurrence is:
    #   dp[k][v] = dp[k-1][v-1] (if we consider v-1 modulo n, so for v=1, v-1 is n) + sum_{for each chord (u, v)} dp[k-1][u]

    # But note: the base edge is always present, so from each vertex u, we can go to u+1. So the base edge contributes from u to u+1. Therefore, to get to v, the base edge contributes from v-1 (mod n).

    # However, the above recurrence is O(n) per step, and k can be up to 200000, so total O(n*k) which is 40e9 operations, which is too slow in Python.

    # We need a better way.

    # Let's try to use generating functions or matrix exponentiation on a reduced state space.

    # Notice that the graph is a cycle with chords. The chords are only 50. We can consider the following: 

    # The base cycle is periodic with period n. The chords break the periodicity. 

    # We can use the idea of "state" that is the current vertex, but we cannot store n states for each k.

    # Alternatively, we can use the concept of "eigenvalues" for the cycle graph. The cycle graph has a circulant adjacency matrix. The eigenvalues are known. But with chords, it becomes complicated.

    # Another idea: use the fact that the base graph is a cycle and use the idea of "rotating" the problem. 

    # Let f(k, v) be the number of ways to be at vertex v after k steps. Then:

    #   f(k, v) = f(k-1,