import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    k = int(data[1])
    total_vertices = n * k
    edges = []
    index = 2
    graph = defaultdict(list)
    for i in range(total_vertices-1):
        u = int(data[index]); v = int(data[index+1]); index += 2
        graph[u].append(v)
        graph[v].append(u)
    
    # If k == 1, then we have n paths of 1 vertex. Then we just need to check if the tree has n vertices? 
    # But note: total_vertices = n*k = n, so the tree must have n vertices. And the tree has n vertices (since we have n*k vertices, and k=1, so n vertices). 
    # Then we can always decompose: each path is a single vertex. So we just need to check that the tree has n vertices? Actually, the input says the tree has n*k vertices, so if k=1, then n vertices. 
    # But note: the input gives edges for a tree with n*k vertices. So if k=1, then the tree has n vertices and n-1 edges. But the input edges are given for a tree with n*k-1 edges, so if k=1, then n-1 edges. 
    # However, the problem says the input is a tree with n*k vertices. So if k=1, then the tree has n vertices and n-1 edges. 
    # Then we can always decompose: we just assign each vertex as a path. So output "Yes" for k=1.

    # But wait: the problem says "each of length K", and if K=1, then the path has 1 vertex and 0 edges. So we don't need any edges. And we have n paths, each of length 1, and the entire set of vertices is used. 
    # So for k=1, it is always possible.

    # However, note: the tree must have exactly n vertices (since total_vertices = n*k = n). And the input gives a tree with n vertices (because the first number is n, and then edges for a tree with n vertices). 

    # But what if k>=2?

    # Conditions for k>=2:

    # We need to cover all vertices with n vertex-disjoint paths, each of length k (k vertices).

    # Note: the tree has total_vertices = n*k.

    # We can think of the decomposition as: we need to find n vertex-disjoint paths, each of k vertices.

    # However, note: the tree is connected. 

    # Another observation: the entire graph has n*k vertices. We are going to use n*k vertices. 

    # How can we form a path of k vertices? We need a contiguous chain of k vertices.

    # But note: the tree is connected, but the paths must be vertex-disjoint.

    # We can use the following idea:

    # 1. The tree must have at least two leaves (unless k=1). In fact, for k>=2, the decomposition requires that we have n*k vertices, and we are going to form n paths. 

    # 2. Consider the degrees of the vertices. In a path of k vertices, the two endpoints have degree 1 (in the path) and the internal vertices have degree 2. 

    # 3. In the entire decomposition, the total number of endpoints is 2*n (each path has two endpoints). The internal vertices (which are n*k - 2*n) must have degree 2 in the decomposition? 

    # But note: the decomposition is vertex-disjoint, so the degrees in the decomposition are the degrees in the paths. However, the original tree has degrees that might be higher.

    # However, the edges that are not used in the decomposition are simply not used. 

    # But wait: the problem does not require that the decomposition uses every edge. So we can ignore edges that are not used.

    # Therefore, the condition is: we need to assign each vertex to a path and arrange the paths so that consecutive vertices in a path are adjacent in the tree.

    # This is a matching problem on the tree.

    # However, note the constraints: total_vertices = n*k <= 200000.

    # We need an efficient solution.

    # Another idea: 

    # In a tree, we can root the tree arbitrarily. Then, we can consider the following:

    # - The decomposition must use exactly n*k vertices (all) and form n paths.

    # - Each path must be a contiguous chain of k vertices.

    # - The entire set of vertices must