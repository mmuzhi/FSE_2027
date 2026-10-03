def main():
    data = sys.stdin.read().splitlines()
    n = int(data[0].strip())
    s = data[1].strip()
    
    # Count the number of 1s in s
    k = s.count('1')
    
    # The graph has two types of edges: cycle edges and star edges (from each i to N)
    # For the cycle edges: there are n edges (each edge is between i and i+1 mod n). Each cycle edge can be oriented in two ways.
    # For the star edges: there are exactly k edges (for each i where s_i is '1') and each can be oriented in two ways.
    # However, the in-degrees of the vertices are affected by both types of edges.

    # Let's denote:
    #   Let A_i be the in-degree contribution from the cycle edges for vertex i.
    #   Let B_i be the in-degree contribution from the star edges for vertex i.

    # For the cycle edges: the graph is a cycle of n vertices (0 to n-1) and then vertex n is connected separately.
    # But note: the cycle edges are only between 0 to n-1. Vertex n is only connected by the star edges (from i to n) and the cycle edges don't connect to n.

    # Actually, the cycle edges are between i and (i+1) mod n for i from 0 to n-1. So the cycle is on vertices 0 to n-1, and vertex n is separate.

    # Now, for the cycle edges: each edge {u, v} can be oriented either way. The in-degree for u and v from that edge is either 1 or 0.

    # The entire graph has two parts: the cycle (vertices 0 to n-1) and the star (vertex n and the edges from i to n for each i with s_i='1').

    # However, note that the cycle edges are only among 0 to n-1, and the star edges are from i (0 to n-1) to n.

    # So, the in-degree of vertex n (d_n) is the number of star edges that are oriented towards n. Since there are k star edges, each can be oriented in two ways, so the in-degree of n can be any integer from 0 to k. But note: the star edges are independent.

    # For the cycle part (vertices 0 to n-1), each edge is oriented independently, but the in-degrees are constrained by the cycle structure.

    # Actually, the problem is more complex because the cycle edges are shared and the orientations are independent.

    # We can break the problem into two parts:

    # 1. The star edges: they only affect vertex n and the source vertices (the i's) for the star edges. But wait, the star edges are from i to n, so when we orient them, we have two choices: either i -> n or n -> i. So for each star edge, the in-degree of n increases by 1 if we choose n -> i (no, wait: if we orient the edge from i to n, then the in-degree of n increases by 1. If we orient from n to i, then the in-degree of n does not increase from that edge.

    # Actually, for a star edge between i and n:
    #   If we orient it as i -> n, then n gets an incoming edge (so d_n increases by 1).
    #   If we orient it as n -> i, then n does not get an incoming edge from this edge.

    # So the in-degree of n is exactly the number of star edges that are oriented towards n. And for each star edge, we have two choices. So the in-degree of n can be any integer from 0 to k, and the number of ways to get a particular in-degree for n is C(k, d_n) * (2^(k - d_n))? Wait, no: actually, for each star edge, we have two choices. The in-degree of n is the number of edges oriented as i->n. So the number of ways to get d_n = j is C(k, j) * (each of the remaining k-j edges must be oriented the other way, but that's already accounted for by the binomial coefficient). Actually, the total ways for the star edges is 2^k, and the distribution of d_n is binomial: the probability that an edge is oriented towards n is 1/2, so the number of ways to have j incoming edges to n is C(k, j) * (each edge is independent). So the number of ways for the star edges to contribute j to d_n is C(k, j