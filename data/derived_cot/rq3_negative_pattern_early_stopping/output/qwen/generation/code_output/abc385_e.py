import sys
from collections import deque, defaultdict

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
    
    # We'll compute the degrees of each node in the original tree.
    deg = [0]*(n+1)
    for i in range(1, n+1):
        deg[i] = len(graph[i])
    
    # We need to consider each node as candidate for the central node.
    # But note: the central node must have at least one edge (x>=1). But in the remaining graph, we can only keep x edges from it.
    # However, we can delete edges arbitrarily (by deleting vertices). 

    # Alternatively, we can think: the Snowflake Tree has a central node with degree x (in the remaining graph) and x nodes with degree y+1 (in the remaining graph). 

    # We are allowed to delete vertices arbitrarily. So we can choose a central node and then choose x edges from it (in the original tree, we can only use edges that are present) and then from each of those x nodes, we can choose y edges (again, only the ones present in the original tree) such that the entire graph is connected.

    # But note: the entire graph must be connected. So the x nodes must be adjacent to the central node (in the original tree) and the leaves must be adjacent to the x nodes (in the original tree). 

    # However, we can delete vertices arbitrarily. So we can choose a central node C, then choose x neighbors of C (in the original tree) and then from each chosen neighbor, choose y leaves (which are neighbors of that neighbor in the original tree). 

    # But wait, the original tree is connected. The remaining graph must be connected. 

    # Actually, the remaining graph is the central node, the x nodes (each connected to the central node), and the leaves (each connected to an x node). 

    # So the edges we keep are:
    #   - The edge from C to each chosen x node.
    #   - The edges from each chosen x node to its chosen y leaves.

    # But note: the original tree might have a path from C to a leaf that goes through multiple nodes. We are allowed to delete vertices arbitrarily, so we can choose to keep only the direct edge from C to an x node and then from that x node to its leaves. 

    # However, the problem is: we are given a tree. We can delete vertices arbitrarily (and the edges incident to them). We want to keep a connected subgraph that is a Snowflake Tree.

    # The Snowflake Tree structure is fixed: one central node, x nodes (each connected to the central node), and y leaves per x node.

    # The total number of vertices is 1 + x + x*y.

    # We want to maximize that.

    # We can try to find, for each node as central node, the maximum x and y we can have.

    # But note: the central node must be connected to x nodes (each x node is a neighbor of the central node in the original tree? Not necessarily: we can delete the intermediate nodes. 

    # Actually, we can choose any x nodes (not necessarily adjacent in the original tree) as long as there is a path from the central node to that x node (and then from the x node to its y leaves). But wait, the structure requires that the central node is directly connected to the x node (by an edge in the remaining graph). 

    # But we can delete vertices arbitrarily. So we can choose to keep an edge from the central node to an x node even if in the original tree there was a longer path? 

    # Actually, no: the remaining graph must be a subgraph of the original tree. So the edges we keep must be edges from the original tree. 

    # Therefore, the central node must be connected (in the original tree) to the x nodes by an edge (because we can only keep edges that are present). 

    # Similarly, the x node must be connected to its leaves by edges that are present in the original tree.

    # So the candidate central node C must have at least x neighbors (in the original tree) that we can use as x nodes. And each x node must have at least y neighbors (in the original tree) that we can use as leaves (and we must not use the edge back to C, because then the x node would have degree y+1 (which is required) but the