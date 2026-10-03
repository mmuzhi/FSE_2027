def main():
    import sys
    data = sys.stdin.read().split()
    n = int(data[0])
    P = list(map(int, data[1:1+n]))
    Q = list(map(int, data[1+n:1+2*n]))
    
    # Create an array for the rank of each row index in P
    rankP = [0] * (n+1)
    for idx, val in enumerate(P):
        rankP[val] = idx  # rankP[i] = the index (0-indexed) of row i in P

    # Create an array for the rank of each column index in Q
    rankQ = [0] * (n+1)
    for idx, val in enumerate(Q):
        rankQ[val] = idx  # rankQ[j] = the index (0-indexed) of column j in Q

    # We'll create a grid of characters, initially all zeros.
    grid = [['0'] * n for _ in range(n)]
    
    # We want to assign the rows: row i should be the binary representation of rankP[i] (with n bits)
    # But note: the condition for rows is that the row with the smallest rank (i.e., first in P) is the smallest lexicographically.
    # However, we also have the column condition. The column condition requires that the columns (when ordered by Q) are increasing.

    # But wait: if we set the grid by row i: the j-th character is the j-th bit of the binary representation of rankP[i] (from least significant to most, or vice versa?),
    # then the columns might not be increasing in the order of Q.

    # Alternatively, we can set the grid such that the row i is set to a string that is increasing in the order of the columns as per Q.

    # However, note: the problem does not require the grid to be built by the row's rank in P. We can use a different method.

    # Let's try to set the grid by the following:

    # We want the rows to be increasing in the order P. We can set the row i to be a string that is all zeros except for the last few bits (or the first few) that indicate the rank.

    # But note: the lex order of the rows must be the same as the order of P. So the row with the smallest rank (P_1) must be the smallest. The smallest binary string is all zeros.

    # So set row i to be a string of zeros, except that we set some bits to 1 to indicate the rank.

    # However, we have two conditions. We can set the grid such that the row i is a string that is the binary representation of the rank of i in P, but then the columns are fixed.

    # But the column condition: the columns must be increasing in the order Q. The column j is the j-th column of the grid. The j-th column is a string of length n (each character is from the row i's representation).

    # We need to ensure that when we reorder the columns by Q (i.e., the first column is the one with index Q_1, then Q_2, etc.), the lexicographical order is increasing.

    # We can set the grid as follows:

    # Let's define a matrix M of size n x n, where M[i][j] = 1 if (rankP[i] * (n - rankQ[j])) > 0, but that doesn't work.

    # Another idea: We can set the grid such that the cell (i, j) is '1' if and only if (the rank of row i in P) is greater than (the rank of column j in Q) or something? 

    # Actually, we can set the grid by comparing the ranks of the row and column in their respective permutations.

    # Consider: We want the row ordering to be increasing by P. So the row with the smallest rank (0) must be the smallest. Similarly, the column with the smallest rank (0) must be the smallest.

    # We can set the grid such that the cell (i, j) is '1' if the rank of row i in P is greater than the rank of column j in Q? 

    # But then, for a fixed row i, the columns j for which rankQ[j] is less than rankP[i] will be '1', and the others '0'. Then, the row i would be a string that has zeros for columns with high rankQ (i.e., columns that are later in Q) and ones for columns with low rankQ (i.e., columns that are earlier in Q). 

    # Now, consider two rows i and k with i having a smaller rank in P than k (so i comes before k). Then, for a