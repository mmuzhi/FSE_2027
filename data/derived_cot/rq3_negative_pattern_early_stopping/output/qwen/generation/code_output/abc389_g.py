import sys
from math import comb

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    P = int(data[1])
    total_edges = N*(N-1)//2
    max_M = total_edges
    min_M = N-1

    # Precompute factorials up to N
    fact = [1] * (N+1)
    for i in range(1, N+1):
        fact[i] = fact[i-1] * i

    # We'll use the concept of counting connected graphs with a fixed bipartition and then adjust for the condition.
    # However, note that the condition is about the bipartition by shortest path, which is not necessarily the fixed bipartition.
    # But there is a known result: the number of connected graphs with N labeled vertices and M edges that are bipartite with a fixed bipartition (A, B) is given by:
    #   C = (number of edges between A and B) choose M, but then we have to consider connectedness.
    # But we need to count graphs that are not necessarily bipartite but have the bipartition by shortest path of size N/2 each.

    # Alternatively, we can use the following approach:
    #   Let A be the set of vertices with even distance and B with odd distance, with |A| = |B| = N/2 and vertex 1 in A.
    #   Then, the graph must have no edges within A or within B? Actually, no. But the condition is that the bipartition by shortest path is (A, B). 
    #   However, if there is an edge within A, then the shortest path might change, but the bipartition by shortest path is still (A, B) because the distances remain even for A and odd for B.

    # Actually, the bipartition by shortest path is defined by the graph. We cannot fix A and B arbitrarily.

    # Another idea: use the concept of "graph growth" from vertex 1. We can use dynamic programming or inclusion-exclusion.

    # But note: the problem is known to be solved by generating functions and exponential generating functions for connected graphs.

    # However, after some research, I recall that the number of connected graphs with N labeled vertices and M edges is given by the formula:
    #   C(N, M) = (1/k) * sum_{i=0}^{k} (-1)^i * C(k, i) * C(N, i) * C(N-i-1, M-1)   [but this is for something else]

    # Actually, the number of connected graphs is given by the exponential formula, but that is complicated.

    # Alternatively, we can use the following combinatorial approach:

    # Let A be the set of vertices at even distance and B at odd distance, with |A| = N/2, |B| = N/2, and vertex 1 in A.
    # The graph must be connected. The edges can be:
    #   - Between A and B: these are necessary for connectivity and for the bipartition.
    #   - Within A or B: these are allowed but might affect the shortest path.

    # But note: the condition is only on the bipartition by shortest path. The graph can have edges within A or B, but the bipartition by shortest path must still be (A, B). 

    # However, if there is an edge within A, then the shortest path from 1 to a vertex in A might be updated if there is a shorter path via that edge? Actually, no, because the edge is within A, so the distance from 1 to the two endpoints are both even, and the edge adds 1 (odd) so the path from one to the other via the edge is even+1 (odd) which is not shorter than the direct even distance (if any). But if the direct distance was even, then the edge doesn't change the shortest path.

    # Actually, the existence of an edge within A does not change the bipartition by shortest path. Similarly for B.

    # Therefore, the condition is independent of edges within A or B. So we can break the problem into two parts:

    # 1. Choose a bipartition (A, B) with |A| = N/2, |B| = N/2, and vertex 1 in A. The number of ways to choose A is C(N-1, N/2 - 1) because vertex 1 is fixed in A, so we choose the remaining N/2 - 1 vertices from the other N-1.

    # 2. Count the number of connected graphs on the N vertices with M edges that have the bipartition (A, B) (meaning