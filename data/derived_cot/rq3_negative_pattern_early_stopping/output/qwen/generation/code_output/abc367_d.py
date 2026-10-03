import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    A = list(map(int, data[2:2+n]))
    total = sum(A)
    P = [0]*(n+1)
    for i in range(1, n+1):
        P[i] = P[i-1] + A[i-1]
    
    # We are going to consider the circle. The clockwise distance from i to j (0-indexed) is:
    #   if j >= i: P[j+1] - P[i]   [but wait, our P[i] is defined as the sum of the first i elements, so the distance from i to j (if j>=i) is P[j+1]-P[i]?
    # Let me redefine: Let P[i] be the sum of the first i segments. Then the distance from node0 to node i is P[i]. 
    # Then, the distance from node i to node j (0-indexed) is:
    #   if j >= i: P[j] - P[i]   (because from node i to node j, we need the segments from i to j-1, which is P[j] - P[i])
    #   if j < i: (total - P[i]) + P[j]   (because from i to the end: total - P[i] (since P[i] is the sum from 0 to i-1, so the rest is total - P[i]), and then from 0 to j: P[j])
    #
    # But wait, our P array is defined for indices 0 to n, and P[i] is the sum of the first i elements (so P[0]=0, P[1]=A0, P[2]=A0+A1, ..., P[n]=total).
    #
    # Actually, the distance from node i to node j (0-indexed) is:
    #   Let d = P[j] - P[i]   if j >= i
    #   Otherwise, d = P[j] + (total - P[i])
    #
    # But note: the distance from node i to node j (clockwise) is the same as the distance from node0 to node j minus the distance from node0 to node i, if j>=i. But if j < i, then we go from i to the end (which is total - P[i]) and then from 0 to j (which is P[j]).
    #
    # However, we can also think of the circle as having a fixed total. The condition is that d % m == 0.
    #
    # But note: the distance d must be positive and less than or equal to total (if we take the long way, it's total - (short way)). But the problem counts the long way as the clockwise distance.
    #
    # But wait, the problem says "the minimum number of steps required to walk clockwise". This is confusing. But the sample counts the long way as the clockwise distance. 
    #
    # Actually, the problem likely means: the clockwise distance (which is the only way if we are walking clockwise) and that distance is the minimum steps required to walk clockwise (which might be the long way if the counterclockwise is not allowed). But the problem says "walk clockwise", so we are forced to take the clockwise path (which might be the long way). 
    #
    # Therefore, we need to count the pairs (i, j) (i != j) such that the clockwise distance (which is the long way if necessary) is divisible by M.
    #
    # But note: the clockwise distance from i to j is the same as the counterclockwise distance from j to i (if we consider the circle). But we are only considering clockwise.
    #
    # We can use the following: 
    #   Let d(i, j) = (P[j] - P[i]) % total   [but this modulo gives a value in [0, total-1], but we need the actual distance, which is the long way if necessary. But the condition is that the distance (which is the actual value, not modulo) is divisible by M.
    #
    # However, the distance d(i, j) is either P[j]-P[i] (if j>=i) or P[j] + (total - P[i]) (if j < i). But note that P[j]-P[i] (if j>=i) is positive and less than total, and if j < i, then P[j] + (total - P[i]) is also positive and less than or equal to total (if we consider that the circle is closed, then the distance from i to j (clockwise) is the same as the distance from j to