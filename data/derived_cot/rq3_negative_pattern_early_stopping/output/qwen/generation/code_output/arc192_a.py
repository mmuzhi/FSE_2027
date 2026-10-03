def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # If there are no zeros, then we don't need any operation, so any string is good.
    if 0 not in A:
        print("Yes")
        return
        
    # Let's count the number of zeros.
    zeros = [i for i in range(n) if A[i] == 0]
    k = len(zeros)
    
    # We are going to think about the possibility of covering zeros with operations.
    # Each operation covers two zeros (if they are zeros). But note: the operations are defined by patterns and the string S is circular.
    # However, we are free to choose S arbitrarily. So we can set S to have the necessary patterns.

    # But note: the operations are defined by two patterns: "ARC" and "CRA". Each occurrence of "ARC" (at positions i, i+1, i+2) can flip the zeros at i and i+1.
    # Similarly, each occurrence of "CRA" (at positions i, i+1, i+2) can flip the zeros at i and i+2.

    # However, we cannot assign the same letter to two different positions arbitrarily without affecting multiple patterns.

    # Alternate Insight:

    # The problem is equivalent to: we have a circular graph of n nodes (each node is an index). We can place two types of edges (or operations) that cover two zeros. But note: the operations are defined by consecutive triples.

    # Actually, note: the operations are defined on consecutive triples. So the operations are local.

    # We can consider: we need to cover all zeros with a set of operations. Each operation is either an edge of type1 (covering two adjacent zeros) or type2 (covering two zeros that are two apart, i.e., with one in between).

    # But note: the operation condition requires the pattern to be set in S. And S is fixed. So we must assign letters to S such that for every operation we wish to use, the pattern is set.

    # However, we are free to choose S arbitrarily. So we can set S to have the necessary patterns to cover the zeros.

    # But note: the same triple of S cannot be two different patterns. So if we use a triple for operation1, we cannot use it for operation2.

    # However, we can use multiple triples (overlapping or not) to cover the zeros.

    # Let's reframe: We need to cover the zeros with a set of edges (each edge is either an adjacent pair or a skip-one pair) such that the entire set of zeros is covered. But note: the operations are defined by the triple, and the triple must be set to a specific pattern.

    # But note: the operations are independent of the current state of A. They just set the two positions to 1. So we can use an operation multiple times, but we only need to use it once for each zero.

    # However, the problem is: can we assign letters to S (a string of length n) such that for every zero (say at position i) there is at least one operation (either type1 or type2) that covers it?

    # Conditions for covering a zero at position i:

    #   For type1: we need an operation1 at position i (then the triple (i, i+1, i+2) must be "ARC") OR at position i-1 (then the triple (i-1, i, i+1) must be "ARC" and then it flips A_{i-1} and A_i) OR at position i-2 (then the triple (i-2, i-1, i) must be "ARC" and then it flips A_{i-2} and A_{i-1})? Actually, wait:

    # Operation1 is defined at index i: it requires S_i='A', S_{i+1}='R', S_{i+2}='C'. Then it flips A_i and A_{i+1}. So to cover a zero at position i, we can use:
    #   Operation1 at index i-1: then it flips A_{i-1} and A_i (so if A_i is 0, then we need an operation1 at index i-1).
    #   Operation1 at index i: then it flips A_i and A_{i+1} (so if A_i is 0, then we need an operation1 at index i, but then we also flip A_{i+1}).
    #   Operation1 at index i-2: then it flips A_{i-2} and A_{i-1} (so that doesn't