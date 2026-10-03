import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().splitlines()
    if not data:
        print(0)
        return
    n = int(data[0])
    edges = []
    graph = defaultdict(list)
    nodes = set()
    for i in range(1, n+1):
        s = data[i].strip()
        edges.append(s)
        u, v = s[0], s[1]
        nodes.add(u)
        nodes.add(v)
        graph[u].append(v)
        # For directed graph, we don't need to add reverse unless specified.

    # Build the graph as a directed graph.
    # We'll compute the in-degree and out-degree for each node.
    out_degree = defaultdict(int)
    in_degree = defaultdict(int)
    for u, v in edges:
        out_degree[u] += 1
        in_degree[v] += 1

    # The problem is to cover all edges (each product name) with the minimum number of walks (strings).
    # We are allowed to use edges multiple times, so we can balance the graph by adding extra edges (but we don't add, we just traverse multiple times).
    # However, the minimal number of walks is determined by the number of "components" or the imbalance.

    # But note: the sample input 3 has 6 edges and is strongly connected, but the degrees are not balanced. 
    # However, we can cover with one walk because we can traverse edges multiple times.

    # Actually, the minimal number of walks is the number of vertices with in_degree != out_degree, but then we have to balance them.

    # In a directed graph, the minimum number of walks needed to cover all edges (each at least once) is the number of vertices with in_degree != out_degree divided by 2? 

    # But wait, consider: 
    # Let d(v) = out_degree(v) - in_degree(v)
    # Then, the sum of d(v) over all v is 0 (because each edge contributes +1 to the start and -1 to the end).
    # The minimal number of walks is the maximum of the number of vertices with positive d(v) and the number of vertices with negative d(v). 

    # Actually, the problem is: we can start a walk at a vertex with positive d(v) and end at a vertex with negative d(v). 

    # The minimal number of walks is the maximum between the number of vertices with out_degree > in_degree and the number of vertices with in_degree > out_degree.

    # But wait, consider: 
    # In a directed graph, to cover all edges, we can use the following: 
    #   Let A be the set of vertices with out_degree > in_degree.
    #   Let B be the set of vertices with in_degree > out_degree.
    #   Then, we need at least |A| walks starting from A and |B| walks ending at B. 
    #   But each walk can start in A and end in B. 
    #   So, the minimal number of walks is max(|A|, |B|).

    # However, let me test with sample input 1.

    # Sample Input 1: edges = ['AB','BC','CA','CD','DE','DF','XX']
    # Nodes: A, B, C, D, E, F, X.

    # Compute degrees:
    # A: out: AB, CA? Wait, no: 
    #   AB: A->B, so out_degree[A] +=1, in_degree[B] +=1.
    #   BC: B->C, out_degree[B] +=1, in_degree[C] +=1.
    #   CA: C->A, out_degree[C] +=1, in_degree[A] +=1.
    #   CD: C->D, out_degree[C] +=1, in_degree[D] +=1.
    #   DE: D->E, out_degree[D] +=1, in_degree[E] +=1.
    #   DF: D->F, out_degree[D] +=1, in_degree[F] +=1.
    #   XX: X->X, out_degree[X] +=1, in_degree[X] +=1.

    # Now, degrees:
    # A: out_degree=1 (AB), in_degree=1 (CA)
    # B: out_degree=1 (BC), in_degree=1 (AB)
    # C: out_degree=2 (CA, CD), in_degree=1 (BC)
    # D: out_degree=2 (DE, DF), in_degree=2 (CD)
    # E: out_degree=0, in_degree=1 (DE)
    # F: out_degree=0, in_degree=1 (DF)
    # X: out_degree=1,