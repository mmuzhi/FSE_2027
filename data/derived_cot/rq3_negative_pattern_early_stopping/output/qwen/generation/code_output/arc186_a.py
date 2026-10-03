def main():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    q = int(data[1])
    ks = list(map(int, data[2:2+q]))
    
    # We are to determine for each K_i in ks whether there exists a matrix with exactly K_i fixed elements.
    # The key is to find the set S of all possible numbers of fixed elements.
    # We know that the fixed elements are determined by the row and column sums.
    # The minimal fixed elements is 0 (as in the identity matrix example) and the maximal is N*N (if the matrix is the only one with its row and column sums, then all elements are fixed).
    # But note: the problem says that for a matrix A, an element is fixed if in every similar matrix B, A_{i,j} = B_{i,j}.
    # The set of similar matrices is the set of all 0-1 matrices with the same row and column sums as A.
    # The fixed elements are the coordinates that are invariant under all such transformations.
    # We need to find all possible numbers of fixed elements that can occur for some matrix A.

    # However, note that the problem does not require us to iterate over all matrices. We need to characterize the set S.

    # Observation: The fixed elements are the ones that are forced by the row and column sums. 
    # For example, if a row has sum 0, then all elements in that row must be 0. Similarly, if a row has sum N, then all elements must be 1.
    # Similarly for columns.

    # But even then, there might be more constraints. For example, if a row has sum 1 and a column has sum 1, and the only way to satisfy both is to put the 1 at the intersection, then that element is fixed.

    # Actually, the fixed elements are the ones that are forced by the row and column sums. 

    # We can think of the problem as: we are to assign row sums r1, r2, ..., rN and column sums c1, c2, ..., cN (each between 0 and N) such that the total sum is the same (sum(r_i) = sum(c_j) = T) and the matrix has exactly K fixed elements.

    # But note: the fixed elements are the ones that are forced by the row and column sums. 

    # How to compute the number of fixed elements for a given (r, c)? 

    # Actually, the fixed elements are the ones that cannot vary. 

    # We can model the problem as a bipartite graph with rows and columns, and the edges are the entries. The row sums and column sums are given. Then, the fixed elements are the edges that are forced to be 0 or 1.

    # This is similar to the concept of "fixed edges" in a transportation problem.

    # However, note that the problem is symmetric and we are allowed to choose the row and column sums arbitrarily (as long as there exists a 0-1 matrix with those margins).

    # We need to find the set S of all possible numbers of fixed elements.

    # Let's consider the following:

    # 1. The minimal fixed elements is 0. For example, the identity matrix (if N>=2) has 0 fixed elements because we can permute the columns arbitrarily (if the row and column sums are all 1, then the set of matrices is the set of permutation matrices, and no single element is fixed).

    # 2. The maximal fixed elements is N*N. This happens when the row and column sums force every element. For example, if we have a matrix where every row sum is 0, then the entire matrix is 0, so all elements are fixed. Similarly, if every row sum is N, then the matrix is all 1s. But also, there are other cases. For example, if we have a matrix with row sums [1,1,...,1] and column sums [1,1,...,1] (the permutation matrices case) then no element is fixed. But if we have a matrix with row sums [2,2,...,2] for N=3, then the fixed elements might be more.

    # Actually, the fixed elements are the ones that are forced by the row and column sums. 

    # We can use the following idea: 

    # The fixed elements are the ones that are determined by the row and column sums. 

    # In fact, the set of fixed elements is the set of positions (i, j) for which the value is forced by the row and column sums. 

    # This is equivalent to: 

    #   A_{i,j} = r_i - (sum of other elements in row