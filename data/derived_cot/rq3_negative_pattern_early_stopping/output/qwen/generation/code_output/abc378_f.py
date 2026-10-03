import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    edges = []
    index = 1
    graph = [[] for _ in range(n+1)]
    for i in range(n-1):
        u = int(data[index]); v = int(data[index+1]); index += 2
        edges.append((u, v))
        graph[u].append(v)
        graph[v].append(u)
    
    # If the tree has only 3 vertices, then adding an edge between two leaves (degree 1) would form a triangle, but then the degrees would be 2 for each vertex (each vertex has two edges: one from the tree and one from the new edge). But the condition requires degree 3. So, no solution for n=3? Actually, for n=3, the tree is two edges. Adding an edge between the two leaves (which are the two vertices of degree 1) would form a triangle. Each vertex has degree 2 (original degree 1 plus one from the new edge). So, condition not satisfied. So, answer 0 for n=3.

    # But wait, the problem says N>=3, so n=3 is allowed.

    # Actually, the condition is that all vertices in the cycle have degree 3. In the triangle, each vertex has degree 2. So, no.

    # So, we need to find pairs (u, v) such that adding the edge (u, v) creates a cycle where every vertex in the cycle has degree 3.

    # Conditions for a vertex to have degree 3 in the new graph:

    # Let d(u) be the degree of u in the tree (original graph). Then, in the new graph, the degree of u is d(u) + 1 if (u, v) is added and u is one of the endpoints, otherwise d(u).

    # But note: the cycle consists of the vertices on the unique path from u to v plus the edge (u, v). 

    # For a vertex w in the cycle (which is the unique path from u to v), the degree in the new graph is:
    #   If w is u or v: d(w) + 1 (because the new edge is incident to u and v).
    #   Otherwise: d(w) (because the new edge is not incident to w).

    # And we require that for every vertex w in the cycle, the degree is 3.

    # So, for u and v: d(u) + 1 = 3  => d(u) = 2. Similarly, d(v) = 2.
    # For every other vertex w in the cycle: d(w) = 3.

    # Therefore, the two endpoints must have degree 2 in the tree, and every vertex on the path (excluding u and v) must have degree 3 in the tree.

    # But wait, what if the cycle has only two vertices? Then the path from u to v is of length 1 (direct edge). Then the cycle is just the two vertices and the new edge. Then, for u and v: d(u)+1=3 => d(u)=2, and d(v)=2. And there are no other vertices. So, that's a cycle of length 2? But in an undirected graph, a cycle must have at least 3 vertices. So, the cycle must have at least 3 vertices.

    # Therefore, the path from u to v must have at least two edges (so the cycle has 3 vertices). 

    # So, the conditions are:
    #   u and v must have degree 2 in the tree.
    #   The unique path from u to v must not contain any vertex with degree not equal to 3 (except u and v which are 2).

    # But wait, what if the path from u to v has a vertex w that has degree 3 in the tree? Then in the new graph, w has degree 3 (same as tree) which is okay. But if w has degree not 3, then it's not okay.

    # Actually, the condition is that every vertex in the cycle must have degree 3 in the new graph. For vertices other than u and v, the degree is the same as in the tree. So, they must have degree 3 in the tree. For u and v, they must have degree 2 in the tree (so that after adding the edge, they become 3).

    # Therefore, we are looking for pairs (u, v) such that:
    #   - u and v have degree 2 in the tree.
    #   - The unique path from u to v (excluding u and v) consists only of vertices with degree 3 in the tree.

    #