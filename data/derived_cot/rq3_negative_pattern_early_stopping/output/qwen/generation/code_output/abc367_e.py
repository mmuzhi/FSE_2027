import sys
from collections import defaultdict, deque

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    # Read the next n integers for X
    X = list(map(int, data[2:2+n]))
    # Read the next n integers for A
    A = list(map(int, data[2+n:2+2*n]))
    
    # If k is 0, then we output A
    if k == 0:
        print(" ".join(map(str, A)))
        return
        
    # We are going to consider the transformation as a permutation of indices? 
    # But note: the operation is defined by the sequence X, which is not necessarily a permutation (it can have duplicates). 
    # However, note the constraints: each element of X is between 1 and N, inclusive, and length N. 
    # But the operation is: 
    #   T(A)[i] = A[X[i]-1]
    # We can think of the transformation on the indices: 
    #   Let f(i) = X[i]-1 (so f maps the index i to the index X[i]-1). Then T(A)[i] = A[f(i)].
    #
    # Then applying T k times: 
    #   T^k(A)[i] = A[ f^k(i) ]
    #
    # But note: the operation is defined by the same X each time, so the transformation is the same function f applied k times.
    #
    # However, note: the operation is applied to the entire array. But the transformation is independent for each index? 
    # Actually, the transformation is: 
    #   T^k(A)[i] = A[ (f composed k times)(i) ]
    #
    # But wait, let's check with sample input 1:
    #   n=7, k=3, X = [5,2,6,3,1,4,6] -> in 0-indexed: [4,1,5,2,0,3,5]
    #   A = [1,2,3,5,7,9,11]
    #   Operation 1: 
    #       A1[0] = A[4] = 7
    #       A1[1] = A[1] = 2
    #       A1[2] = A[5] = 9
    #       A1[3] = A[2] = 3
    #       A1[4] = A[0] = 1
    #       A1[5] = A[3] = 5
    #       A1[6] = A[5] = 9
    #   Operation 2:
    #       A2[0] = A1[4] = 1
    #       A2[1] = A1[1] = 2
    #       A2[2] = A1[5] = 5
    #       A2[3] = A1[2] = 9
    #       A2[4] = A1[0] = 7
    #       A2[5] = A1[3] = 3
    #       A2[6] = A1[5] = 5
    #   Operation 3:
    #       A3[0] = A2[4] = 7
    #       A3[1] = A2[1] = 2
    #       A3[2] = A2[5] = 3
    #       A3[3] = A2[2] = 5
    #       A3[4] = A2[0] = 1
    #       A3[5] = A2[3] = 9
    #       A3[6] = A2[5] = 5
    #
    # So the result is [7,2,3,5,1,9,5] but the sample output is [7,2,3,5,1,9,3]. 
    #
    # Wait, there is a discrepancy. The sample output for three operations is: 
    #   "7 2 3 5 1 9 3"
    #
    # Let me recalc manually for the third operation using the sample's own steps:
    #   After one operation: (7,2,9,3,1,5,9)
    #   After two operations: (1,2,5,9,7,3,5)
    #   After three operations: (7,2,3