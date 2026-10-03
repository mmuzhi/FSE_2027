def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    total = n * m
    # We'll build a graph with total+1 nodes (0 to total)
    graph = [[] for _ in range(total+1)]
    # For each vertex i from 1 to total, connect to max(i - n, 0)
    for i in range(1, total+1):
        j = i - n
        if j < 0:
            j = 0
        graph[i].append(j)
        graph[j].append(i)
    
    # We need to compute the expected number of operations.
    # The process: start at 0, and until all are painted, move randomly to an adjacent vertex and if unpainted, paint it.
    # We are to compute the expected number of operations (moves) until all are painted.

    # We can use dynamic programming or state reduction. However, note that the graph is a grid-like structure with two dimensions: rows and columns, where each row has m nodes, and there are n rows.

    # Actually, the graph is a directed graph in the sense that from a node i (which is in row i//m, column i%m) we can go to i - n (if exists) and i + n (if exists) and also to i + 1 and i - 1? Wait, no. The edges are only between i and max(i-n,0). But wait, the edge is defined for each i from 1 to total, connecting i and max(i-n,0). So the graph is actually a collection of chains? Or a grid?

    # Let me reexamine: for example, n=2, m=2, total=4.
    # Edges:
    #   Edge 1: connects 1 and max(1-2,0)=0
    #   Edge 2: connects 2 and max(2-2,0)=0
    #   Edge 3: connects 3 and max(3-2,0)=1
    #   Edge 4: connects 4 and max(4-2,0)=2
    # So the graph has edges: 0-1, 0-2, 1-3, 2-4.
    # So the graph is a tree with root 0, and two children (1 and 2), and then 1 has a child 3, 2 has a child 4.

    # Actually, the graph is a directed graph from higher indices to lower indices (if we consider the edge from i to max(i-n,0)), but since it's undirected, we can traverse both ways.

    # The problem is: we start at 0, and we move randomly to an adjacent vertex. We paint a vertex only if it's unpainted. We stop when all are painted.

    # We need the expected number of moves.

    # This is a Markov chain problem. We can use the concept of expected steps to absorption. But the state space is the set of painted vertices, which is too large (2^(n*m) states). So we need a smarter way.

    # Observation: the graph is a grid of n rows and m columns, but the edges are only between a node and the node n steps below (if exists) and the node n steps above (if exists). Actually, no: the edge connects i and max(i-n,0). So from node i, we can go to i-n (if i>=n) and to i+n (if i+n <= total). But wait, the edge is defined for each i from 1 to total, so the graph is actually a directed graph from i to i-n (if exists) and from i-n to i (if exists). But the problem says "adjacent", so it's undirected.

    # Actually, the graph is a directed graph with edges from i to max(i-n,0) for each i from 1 to total, and then we consider the reverse edges as well? Or is the graph built by adding an undirected edge for each i?

    # The problem says: "The i-th edge (1 ≤ i ≤ N×M) connects vertices i and max(i−N,0)." So the graph is undirected.

    # Therefore, from vertex i, the neighbors are:
    #   - max(i - N, 0)   [the parent]
    #   - and also, if i + N <= total, then i + N is a neighbor? No, because the edge is defined for each i from 1 to total, so the edge for vertex i+N would be defined separately. Actually, no: the edge for