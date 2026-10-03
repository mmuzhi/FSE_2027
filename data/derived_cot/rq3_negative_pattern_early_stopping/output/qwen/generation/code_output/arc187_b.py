import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    B = list(map(int, [x if x != '-' else -1 for x in data[2:2+n]]))
    
    # Count the number of -1s (wildcards)
    q = B.count(-1)
    # Precompute powers of M modulo MOD up to q
    powM = [1] * (q+1)
    for i in range(1, q+1):
        powM[i] = powM[i-1] * m % MOD

    # Separate the indices into fixed and wildcards
    fixed = [i for i, x in enumerate(B) if x != -1]
    wildcards = [i for i, x in enumerate(B) if x == -1]
    
    # We'll use dynamic programming or inclusion-exclusion. But note: the graph is built by the condition on the entire sequence.
    # Alternatively, we can think of the connected components as being determined by the relative ordering of the numbers.

    # However, note that the graph is built by the condition: for i<j, edge if A_i <= A_j.
    # The connected components are the same as the equivalence classes of the relation: i ~ j if there is a path from i to j (via edges defined by the condition).

    # But note: the graph is actually the same as the graph of a sequence with edges for every pair (i, j) (i<j) that satisfies A_i <= A_j.

    # We can also note that the graph is the complement of the graph where edges are drawn for i<j and A_i > A_j.

    # But perhaps a better way is to use the linearity of expectation? Or to break the problem by considering the contribution of each pair.

    # Alternatively, we can use the fact that the number of connected components is equal to N minus the number of edges (if the graph were a tree) but it's not.

    # Actually, we can use the concept of "graph connectedness" and use the principle of inclusion-exclusion to count the number of sequences that yield a particular graph.

    # But note: the problem asks for the sum of f(B') over all sequences.

    # Another idea: use the linearity of the sum. The sum of f(B') is the sum over all sequences of the number of connected components.

    # And the number of connected components is the sum over all vertices of the indicator that the vertex is the root of its component? Or we can use the fact that the connected components can be counted by considering the complement graph.

    # But note: the graph is defined by the condition on the entire sequence. We can also think of the graph as being built by the following: the graph is the union of cliques for each value? Actually, no.

    # Let me try to reframe: the graph is the same as the graph of a sequence with edges for every pair (i, j) (i<j) that satisfies A_i <= A_j. This is the same as the graph of a permutation (if we ignore the wildcards) but with ties.

    # Actually, the graph is the comparability graph of the sequence with respect to the natural order, but only for pairs (i, j) with i<j.

    # But note: the graph is undirected, so the edge is present if A_i <= A_j for i<j OR A_j <= A_i for j>i? No, the condition is only for i<j. So the edge is present only if for the pair (i, j) (with i<j) the condition holds.

    # Now, the connected components are the same as the equivalence classes of the relation: i ~ j if there is a path from i to j (via edges). But note that the graph is built by the condition on the entire sequence.

    # We can also note that the graph is the same as the graph of a sequence with edges for every pair (i, j) (i<j) that satisfies A_i <= A_j. This graph is known as a "threshold graph" or "friendship graph"? Not exactly.

    # Alternatively, we can use the following idea: the graph is the same as the graph of a sequence with edges for every pair (i, j) (i<j) that satisfies A_i <= A_j. This graph is actually a "comparability graph" of the sequence, but the sequence is fixed.

    # But note: the problem is to sum over all completions.

    # Let me try to break down the problem by considering the contribution of each pair of vertices (i, j) (i<j) to the connected components.

    # Actually, the number of connected