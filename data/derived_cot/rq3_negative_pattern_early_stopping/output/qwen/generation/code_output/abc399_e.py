import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().splitlines()
    n = int(data[0])
    S = data[1].strip()
    T = data[2].strip()
    
    # If S is already T, return 0.
    if S == T:
        print(0)
        return
        
    # Build mapping from each character in S to the target in T.
    # But note: the same character in S must map to the same character in T.
    # However, different characters in S can map to the same character in T.
    # But if a character in S maps to two different characters in T, that's impossible.
    # So, first, check for consistency: for each character c in S, the corresponding T[i] for each occurrence of c must be the same.
    # Actually, no: because the operations are global. The mapping is defined by the operations, and the same operation might change multiple letters.

    # Actually, we can think of the problem as: we have a graph where nodes are letters (from 'a' to 'z'). 
    # We need to map each letter c (that appears in S) to a letter d (which is in T) such that for each occurrence of c in S, d is T[i].
    # But note: the mapping must be consistent for all occurrences of c.

    # However, the operations allow us to change one letter to another. The minimal number of operations is the number of edges in the transformation graph.

    # Steps:
    # 1. Check if for each letter c in S, all the T[i] for which S[i] == c are the same. If not, return -1.
    # 2. Build a graph of the required transformations.

    # But note: the operations are not necessarily one-to-one. We can have multiple letters mapping to the same letter.

    # Actually, we can model the problem as: we have a set of letters (from S and T). We need to define a mapping from the letters in S to the letters in T such that the mapping is consistent (i.e., if a letter c in S is mapped to d in T, then every occurrence of c must be mapped to d).

    # Then, the problem reduces to: what is the minimum number of operations (each operation is an edge from x to y) to achieve the mapping.

    # But note: the operations are global and can be chained. So, the minimal number of operations is the number of edges in a minimum spanning tree of the mapping graph? Or the number of edges needed to cover all the mappings.

    # Alternatively, we can think in terms of connected components.

    # Let me define a graph where:
    #   - Nodes are the letters that appear in S and T.
    #   - We have an edge from c to d if c must be mapped to d (i.e., for some i, S[i] = c and T[i] = d).
    #   - But note: multiple edges from the same node c to different nodes d would be invalid (unless they are the same d). So, first, we must check that for each c, there is only one d.

    # Actually, the first step is to check consistency: for each letter c in S, all the T[i] for which S[i] == c must be the same. Let's call that d. Then, we have a mapping from c to d.

    # Now, we have a set of mappings: from each letter c (in S) to a letter d (in T). But note: the mapping must be defined for all letters that appear in S.

    # Now, the operations are: we can change one letter to another. The goal is to have all letters in S transformed to their corresponding T letters.

    # The minimal number of operations is the number of edges in a graph that connects all the letters in S to their T counterparts, but with the possibility of chaining.

    # Actually, we can consider the following: 
    #   We have a directed graph where an edge from c to d means that c is mapped to d (directly). But we can also have chains: c -> e -> d, which is two operations.

    # The minimal number of operations is the number of edges in a minimum spanning tree for the mapping? Or the number of edges needed to cover all the mappings.

    # But note: we can also use intermediate letters. 

    # Actually, the problem is similar to finding the minimum number of edges to connect a set of nodes (the letters) with the constraint that we can only add edges (operations) that are from one letter to another, and the goal is to have a path from each letter c to its target d.

    # But note: the operations are not directed in the sense of graph edges? Actually, each