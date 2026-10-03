def main():
    import sys
    data = sys.stdin.read().splitlines()
    K = int(data[0].strip())
    S = data[1].strip()
    T = data[2].strip()
    
    n = len(S)
    m = len(T)
    
    # If the length difference is more than K, then impossible.
    if abs(n - m) > K:
        print("No")
        return
        
    # We'll use a BFS-like approach but with limited operations (K<=20) and the strings are long, but we can use the fact that we only need to consider a small window around the common subsequence.

    # Alternatively, we can use the concept of "edit distance" with a limit, but we can use a recursive function with memoization? But the strings are long.

    # Another idea: use the fact that the edit distance is the minimum number of operations. We can compute the edit distance with a bounded K by considering only the first min(n, m) + K characters? 

    # But note: we are allowed to insert and delete anywhere, so the transformation might involve changing a small part of the string.

    # We can use a two-pointer to find the longest common subsequence (LCS) and then the edit distance is at least (n + m - 2 * LCS) and then we have to account for the length difference.

    # However, the standard edit distance formula is: 
    #   d = (n + m - 2 * LCS_length) + abs(n-m) ??? Not exactly.

    # Actually, the edit distance is the minimum number of operations. We can use the following:

    # We are allowed to do at most K operations. We can consider that the transformation must involve a common subsequence that is at least (n + m - K) / 2? Not exactly.

    # Let's think: we can use a recursive function that considers the operations, but the state space is too big.

    # Alternatively, we can use the following known fact: 
    #   The edit distance between S and T is at least the absolute difference of the lengths and at least the number of positions where the characters differ in a common subsequence.

    # But we can use a greedy approach: 

    # We are allowed up to K operations. We can try to align the strings and count the minimum operations required.

    # However, we can use the following: 

    # We can use a two-pointer to traverse both strings and count the minimum operations required to transform S to T, but we are limited by K.

    # But note: the operations are not necessarily contiguous. 

    # We can use a BFS with state (i, j, ops) where i is the current index in S, j in T, and ops is the number of operations done so far. But the strings are long (500000) so we cannot do that.

    # We need a smarter way.

    # Insight: Since K is at most 20, the total number of operations is small. Therefore, the transformed string T must be obtained from S by changing at most 20 characters (if we consider that insertions and deletions change the length, but replacements don't). 

    # Actually, we can consider that the transformation must involve a common subsequence of length at least (n + m - K) / 2? 

    # Alternatively, we can use the following: 

    #   Let d = edit_distance(S, T) but we don't want to compute it fully.

    # We can use the fact that the edit distance is the minimum number of operations. We can compute the edit distance with a bounded K by considering that the edit distance is at most K.

    # There is an efficient way to compute the edit distance for small K? 

    # We can use the following: 

    #   We are allowed to do at most K operations. Then, the transformed string T must be obtainable from S by a sequence of at most K operations.

    # We can use a recursive function that tries to match the strings from the beginning and count the operations, but we can use memoization with the remaining operations and the current positions. However, the positions can be up to 500000, so we cannot use a DP table.

    # But note: we are only allowed up to 20 operations. So the transformation must be done by changing a small part of the string. 

    # We can consider that the common subsequence must be long enough. The minimum edit distance is:

    #   d = (n + m - 2 * LCS_length) + abs(n-m)   [This is not correct]

    # Actually, the edit distance is defined as:

    #   d = minimum operations (insert, delete, replace) to transform S to T.

    # We can use a