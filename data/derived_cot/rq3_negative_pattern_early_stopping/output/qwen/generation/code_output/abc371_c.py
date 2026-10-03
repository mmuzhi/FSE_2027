import itertools
import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    it = iter(data)
    n = int(next(it))
    m_g = int(next(it))
    edges_g = []
    for _ in range(m_g):
        u = int(next(it)); v = int(next(it))
        edges_g.append((u, v))
        
    m_h = int(next(it))
    edges_h = []
    for _ in range(m_h):
        a = int(next(it)); b = int(next(it))
        edges_h.append((a, b))
        
    # Read the cost matrix A
    # The input gives A_{1,2}, A_{1,3}, ... A_{1,N}, then A_{2,3}, ... A_{2,N}, etc.
    # So, we'll read the first row (n-1 numbers), then the next row (n-2 numbers), etc.
    # We'll build a 2D list A of size n x n, with A[i][j] = cost for edge (i+1, j+1)
    # Note: the vertices are 1-indexed in input, but we'll use 0-indexed in code.
    A = [[0]*n for _ in range(n)]
    for i in range(n-1):
        row = []
        for j in range(i+1, n):
            row.append(int(next(it)))
        # Now, we need to assign these to A[i][j] and A[j][i]
        for idx, j in enumerate(range(i+1, n)):
            A[i][j] = row[idx]
            A[j][i] = row[idx]
            
    # Now, we have graph G (edges_g) and graph H (edges_h) and cost matrix A.
    # We need to find a permutation P (of 0 to n-1) such that the graph H' (with edges (P[u], P[v]) for each edge (u,v) in G) is exactly the same as the graph we get by flipping edges in H to match the edge set of G under permutation P.
    # But note: the operation flips edges arbitrarily. So, we can change H to any graph. The condition is that the final graph H' must be isomorphic to G.

    # However, note: the problem allows flipping edges arbitrarily. So, we can turn H into any graph. The minimal cost is independent of the initial H? Actually, no. The cost depends on the initial H and the target graph (which is determined by the permutation).

    # Let me reframe: We need to choose a graph H' (which is a permutation of the vertex set) such that H' is isomorphic to G. Then, the cost is the sum over all edges (i,j) of:
    #   if (i,j) is in H' and not in H, then cost A[i][j]
    #   if (i,j) is not in H' and in H, then cost A[i][j]
    # But wait, that's not exactly. The operation flips edges. So, for each edge (i,j) (with i<j), we can consider:
    #   Let x = 1 if (i,j) is in H, else 0.
    #   Let y = 1 if (i,j) is in H', else 0.
    #   Then, the cost for edge (i,j) is A[i][j] * (x != y) [because if they differ, we need to flip once, else 0].

    # But note: the target graph H' is defined by the permutation P and G. Specifically, H' should have an edge (P_i, P_j) if and only if (i,j) is an edge in G.

    # So, for a given permutation P, the target graph H' has edges: for each edge (i,j) in G, we have an edge (P_i, P_j) in H'.

    # Then, the cost for edge (i,j) (in the original graph H) is:
    #   Let e = (i,j) (with i<j). Then, in H, we have x = 1 if (i,j) is in H, else 0.
    #   In H', we have y = 1 if (P^{-1}_i, P^{-1}_j) is an edge in G? Wait, no.

    # Actually, the edge set of H' is defined by: for each edge (a,b) in G, we have an edge (P_a, P_b) in H'. So, to check if (i,j) is in H', we need to see if there exists an edge (a,b) in G such that P_a = i and P_b