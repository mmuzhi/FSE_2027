def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data:
        return
    n = int(data[0])
    strings = data[1:1+n]
    # Find M (maximum length)
    M = max(len(s) for s in strings)
    
    # We'll create an array for each row j (from 1 to M) of the output.
    # For each row j (0-indexed j from 0 to M-1), we want to set the characters at positions (n-i) for each i (0-indexed i from 0 to n-1) if j < len(strings[i])
    # But note: the row index in the condition is (n-i) (if we use 0-indexed i, then the row index is n-i, because i from 0 to n-1, then row index = n-i, which is from n down to 1).
    # Actually, the condition uses 1-indexed i. Let's use 0-indexed for the input strings: 
    #   For the i-th string (0-indexed i), the row index is n - i (because i=0 -> row index = n, i=1 -> row index = n-1, ..., i=n-1 -> row index = 1).
    #
    # But note: the condition says: the (n-i+1)-th character of T_j (for the i-th string) — in 0-indexed, that is the (n-i)-th character (if we consider the string T_j as 0-indexed, then the (n-i+1)-th character is at index n-i).
    #
    # However, we are building T_j (the j-th row) as a string. We need to set the character at position (n-i) (0-indexed) to the j-th character (0-indexed j) of the i-th string, provided that j < len(strings[i]).
    #
    # But note: the condition says: the (n-i+1)-th character of T_j (1-indexed) is the j-th character of the i-th string (1-indexed). 
    # In 0-indexed, the (n-i+1)-th character is at index (n-i) (because 1-indexed position k is 0-indexed k-1).
    #
    # So for each row j (0-indexed j from 0 to M-1) and for each string i (0-indexed i from 0 to n-1):
    #   if j < len(strings[i]):
    #       set the character at position (n - i - 1) in T_j to strings[i][j]
    #
    # But wait, the row index in the condition is (n-i+1) (1-indexed) and we are building T_j (the j-th row) which is a string. 
    # The condition says: the (n-i+1)-th character of T_j (1-indexed) is the j-th character of the i-th string.
    # In 0-indexed, the (n-i+1)-th character is at index (n-i) (because 1-indexed position k -> 0-indexed k-1).
    #
    # However, note: the row index (n-i+1) is the same for all j. We are building T_j (the j-th row) and we are setting the (n-i+1)-th character (which is the (n-i)-th index in 0-indexed) of T_j to the j-th character of the i-th string.
    #
    # But wait, the condition says: for the i-th string, the j-th character goes to the (n-i+1)-th character of T_j. 
    # This means: for a fixed i and j, we set T_j at position (n-i) (0-indexed) to strings[i][j].
    #
    # However, note: the condition also says that the output has M rows (T_0 to T_{M-1}) and each T_j is a string.
    #
    # But note: the condition says that the (n-i+1)-th character of T_j must exist for j from 0 to len(strings[i])-1 (0-indexed j). 
    # This means that T_j must have at least (n-i+1) characters (1-indexed) -> in 0-indexed, at least (n-i) characters.
    #
    # Therefore, the length of T_j must be at least the maximum (n-i) for all i such that j < len(strings[i]).
    #
    # However, note: the row index (n-i) is the same for all j. We are setting the same position