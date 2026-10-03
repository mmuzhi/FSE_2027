import sys

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2+n]))
    B = list(map(int, data[2+n:2+2*n]))
    
    # If A is already B, output 0.
    if A == B:
        print(0)
        return
        
    total_ops = 0
    for i in range(n):
        # Compute the minimal circle distance from A[i] to B[i]
        d = (B[i] - A[i]) % m
        if d < 0:
            d += m
        circle_distance = min(d, m - d)
        total_ops += circle_distance
        
    # But wait, the sample input 1: 
    #   N=3, M=9, A=[2,0,1], B=[4,8,1] -> circle_distance for index0: (4-2)%9=2 -> min(2,7)=2; index1: (8-0)%9=8 -> min(8,1)=1; index2: (1-1)%9=0 -> min(0,9)=0 -> total_ops=3 -> matches.
    #   Sample input 2: already handled.
    #   But the second example (N=2, M=5, A=[0,1], B=[2,0]) gives 2+1=3, but we know the answer is 4.

    # Therefore, the above simple sum is not always correct.

    # We must account for the blocking by neighbors.

    # However, the problem is complex and the provided sample inputs are not enough to deduce a general formula.

    # Given the complexity and the fact that the problem is from a competition, there might be a known approach.

    # After research, this problem is similar to "Minimum Operations to Convert Time" but with circular and adjacency constraints.

    # But note: the sample input 1 works with the simple sum, but sample input 3 (large) might not.

    # Let's try sample input 3:

    # Sample Input 3:
    #   24 182
    #   128 115 133 52 166 92 164 119 143 99 54 162 86 2 59 166 24 78 81 5 109 67 172 99
    #   136 103 136 28 16 52 2 85 134 64 123 74 64 28 85 161 19 74 14 110 125 104 180 75

    #   The simple sum of circle distances for each index would be the answer if there were no blocking.

    #   But the provided sample output is 811.

    #   Let's compute the simple sum for sample input 3:

    #   We'll compute for each index i: circle_distance = min(|B_i - A_i|, 182 - |B_i - A_i|) but careful: we should use modulo.

    #   However, the sample input 3 is large, so we'll write a small program to compute the sum.

    #   But note: the sample input 3 might have blocking that increases the total steps.

    #   Without the exact answer from the simple sum, we cannot be sure.

    #   Given the complexity and the fact that the problem is not trivial, and the sample input 1 works with the simple sum but the second example does not, we must find a better approach.

    #   However, the problem statement says: "Determine if it is possible to make A equal to B, and if it is possible, find the minimum number of operations required."

    #   And the constraints are high.

    #   After further thought, note that the operations are independent and the only constraint is that after each operation, the entire sequence is good.

    #   This means that we can change an index i to B_i in circle_distance steps if and only if there exists a path from A_i to B_i that does not use any value that is equal to the current value of the adjacent indices at the time of the operation.

    #   But the adjacent indices are also being changed. 

    #   We can change the entire sequence from left to right. For index i, the left neighbor is fixed at B