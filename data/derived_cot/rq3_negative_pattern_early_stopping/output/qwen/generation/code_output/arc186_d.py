def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # Precompute Catalan numbers up to n-1 (since dp[n] = Catalan_{n-1})
    # Catalan numbers: C_0 = 1, C_1 = 1, C_2 = 2, C_3 = 5, ...
    # We need Catalan numbers for indices 0 to n-1.
    # Formula: C_0 = 1, C_{k} = (2*(2*k-1)*C_{k-1}) // (k+1) for k>=1.
    # But we need up to k = n-1.
    if n == 0:
        print(0)
        return
        
    max_k = n-1
    catalan = [0] * (max_k+1)
    catalan[0] = 1
    for k in range(1, max_k+1):
        catalan[k] = (2 * (2*k-1) * catalan[k-1]) // (k+1)
        catalan[k] %= mod
        
    # But note: the problem asks for Polish sequences of length N that are <= A.
    # We have dp[N] = catalan[N-1] (the number of Polish sequences of length N).
    # But wait, the sample: N=6, catalan[5] = 42. But the sample output is 2.
    # So clearly, dp[N] is not the total number of Polish sequences of length N, but the count of sequences <= A.

    # We need to count the number of Polish sequences of length N that are <= A.

    # We can use a DP that counts the number of Polish sequences of length N that are <= A.

    # Let's define a function that, given a sequence length and a bound, counts the number.

    # But the sequence is built recursively.

    # We can use a DFS with memoization, but N is up to 300,000.

    # Alternatively, we can use a combinatorial digit DP.

    # Let's define a DP state as (pos, tight) where:
    #   pos: current position in the sequence (0-indexed)
    #   tight: whether the prefix is equal to A's prefix

    # But the sequence is built by: first element k, then k Polish sequences.

    # However, the structure is not a simple digit; the first element k determines the number of children.

    # We need to consider the entire structure.

    # Let me define a function f(pos, tight) that returns the number of ways to complete the sequence from position pos to the end, given that the prefix is tight (equal to A's prefix).

    # But the sequence is built recursively: at pos, the first element is k (which is the first element of the sequence). Then, the next k sequences are the children.

    # But the length is fixed to N.

    # Alternatively, we can use a different approach.

    # Since the sequence is determined by its recursive structure, we can use a stack or a recursive function that, given a length and a bound, counts the number of Polish sequences.

    # But the length is fixed to N.

    # We can use a DP that for a given length L and a bound (whether the prefix is tight), counts the number of Polish sequences of length L that are <= A[0:L].

    # But the sequence is built by: first element k (which is a non-negative integer), then k sequences.

    # The first element k must be <= A[0] (if tight) or can be any number (if not tight).

    # But the entire sequence must have length N.

    # Let me define a function dp(pos, tight) that returns the number of ways to complete the sequence from pos to the end, given that the prefix is tight.

    # But the sequence is not a simple digit; the first element k determines the number of children.

    # Actually, the sequence is built as:
    #   [k, (sequence1), (sequence2), ..., (sequencek)]
    # where each sequencei is a Polish sequence.

    # The total length is 1 + (length of sequence1) + ... + (length of sequencek) = N.

    # So, if we are at position pos, then the first element is at pos, and then we have k sequences starting at pos+1.

    # But the length of each sequence is variable.

    # This is complex.

    # Given the complexity and the constraints, we need to use a combinatorial approach.

    # But after