def main():
    import sys
    data = sys.stdin.read().splitlines()
    n = int(data[0].strip())
    s = data[1].strip()
    total_vertices = 2 * n
    white_positions = [i+1 for i, char in enumerate(s) if char == 'W']
    black_positions = [i+1 for i, char in enumerate(s) if char == 'B']
    
    # If the number of W and B is not n, but the problem states they are, so we assume.
    # The graph has a chain 1->2->...->2n.
    # We need to form n pairs (white, black) and add an edge from white to black.
    # The graph must be strongly connected.

    # Conditions for strong connectivity:
    # 1. The graph must have a cycle that covers all vertices? Not necessarily, but must be strongly connected.

    # Observation: The chain edges form a directed path. The added edges are from white to black.
    # For the graph to be strongly connected, the following must hold:
    #   - There must be a way to go from any vertex to any other.
    #   - In particular, the entire graph must be one strongly connected component.

    # Let's consider the structure: The chain edges go from lower index to higher index. The added edges go from white to black, which can be from a lower index to a higher or higher to lower.

    # We can think of the graph as having two types of edges: the chain (forward) and the added (which can be backward or forward).

    # The key is that the graph must have a cycle that includes all vertices. But note: the chain edges alone do not form a cycle (unless n=1 and the pairing is done appropriately).

    # Another observation: The graph must be able to go from any vertex to any other. In particular, from a black vertex to a white vertex and vice versa.

    # Let me try to break down the problem:

    # Condition 1: The graph must have a path from the first vertex (vertex1) to every other vertex. Similarly, from every vertex to vertex1.

    # But note: the chain edges go from lower to higher. So to go from a higher vertex to a lower, we must use an added edge (from white to black) that goes backward.

    # Therefore, for the graph to be strongly connected, we must have at least one added edge that goes from a white vertex to a black vertex with a lower index (i.e., backward) so that we can come back.

    # However, the sample input N=2, S="BWBW" (which is "BW" for vertex1 and vertex4) actually has two backward edges? Wait, in the sample, the pairing (2,3) and (4,1) gives edges 2->3 (forward, since 2<3) and 4->1 (backward). So the backward edge is necessary.

    # But wait, in the first pairing (2,1) and (4,3): edges 2->1 (backward) and 4->3 (backward). But still not strongly connected.

    # So having backward edges is necessary but not sufficient.

    # Let me think of necessary conditions:

    # 1. The graph must have a cycle that includes all vertices. This cycle must use both chain edges and added edges.

    # 2. The added edges must form a set that, together with the chain, allows cycles that cover the entire graph.

    # Another idea: Consider the graph as a directed graph with two types of edges. The chain edges are fixed. The added edges are from white to black. The graph is strongly connected if and only if:

    #   a) The graph has a directed path from the first vertex to the last, and from the last to the first, and so on.

    # But note: the chain edges already give a path from 1 to 2n. The problem is to have a path from any vertex to any other.

    # Actually, the chain edges give a total order from 1 to 2n. The added edges can break this order by providing backward edges.

    # The necessary and sufficient condition might be that the graph must have a cycle that includes all vertices, and the cycle must use the chain edges and the added edges appropriately.

    # Alternatively, we can use the concept of strongly connected components. The graph must have exactly one strongly connected component.

    # However, with constraints up to 200,000, we need a combinatorial approach.

    # Let me try to find a pattern or known result.

    # Consider the following: The graph is strongly connected if and only if the following holds:

    #   - The set of