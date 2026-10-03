import sys
from math import factorial
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    B = list(map(int, data[1+n:1+2*n]))
    
    # We are given A and B, each of length n.
    # We need to count the number of ways to assign three permutations (columns) such that:
    # 1. The set of 2n rows (the n original and the n reversed) are distinct.
    # 2. The lexicographical rank of the i-th row (the i-th row of the matrix) is A[i-1].
    # 3. The lexicographical rank of the reverse of the i-th row is B[i-1] (if B[i-1] != -1).
    #
    # However, note: the matrix is defined by three columns, each a permutation of 1..n.
    # The i-th row is (x_i, y_i, z_i) where x_i is the i-th element of the first column, etc.
    #
    # But note: the lexicographical order of the rows (each row is a triple) and their reverses (each row reversed is a triple) must be such that the given A and B are satisfied.
    #
    # This is a very complex problem. We need to break it down.
    #
    # Observation:
    # The entire set of 2n rows is the set S (the n original) and T (the n reversed). The lexicographical order is determined by comparing the triples.
    #
    # The rank of a row is determined by how many rows (from S ∪ T) are strictly less than it.
    #
    # The condition is that the i-th row (the row we built for the i-th row of the matrix) must have rank A[i] (if A[i] is given) and the reverse of the i-th row must have rank B[i] (if B[i] is given).
    #
    # But note: the matrix is built by columns. The i-th row is (x_i, y_i, z_i). The reverse is (z_i, y_i, x_i).
    #
    # However, the ranks depend on the entire set of 2n rows. This seems intractable.
    #
    # Alternative approach:
    # We are given A and B. The problem states that in the concatenation of A and B, each integer other than -1 appears at most once. This means that the ranks we are given for the original rows and the reversed rows are distinct and cover a subset of 1..2n.
    #
    # Let U be the set of ranks that are fixed by A and B. Then the remaining ranks are free.
    #
    # But note: the ranks must be consistent with the lexicographical order of the rows and their reverses.
    #
    # However, the problem is very abstract and requires a deep combinatorial insight.
    #
    # After reading sample input and output, and constraints, it's clear that a brute-force or even a DP with state of size 3000 is not feasible.
    #
    # There might be a combinatorial formula or a way to count by considering the relative orders of the rows and their reverses.
    #
    # But note: the problem is from a programming competition and the sample input is small (n=3). The sample output is 1.
    #
    # Another sample input is n=15, output is 758094847.
    #
    # Given the complexity, I suspect that the solution involves dynamic programming with state representing the current position in the matrix and the set of used numbers in the columns, but that state space is too large (n=3000, and 2^n possibilities for each column?).
    #
    # Alternatively, we can think of the problem as assigning three permutations (columns) and then checking the conditions on the ranks. But the rank conditions are global (they depend on the entire set of 2n rows).
    #
    # This problem is likely to be solved by inclusion-exclusion or by generating functions, but I don't see an immediate way.
    #
    # After some thought, note that the problem is symmetric in the columns? Not exactly, because the lexicographical order is defined by the entire triple.
    #
    # Another observation: the lexicographical order of the rows and their reverses is determined by the first element, then the second, then the third. Therefore, the entire set of 2n rows can be sorted by comparing the first elements, then the second