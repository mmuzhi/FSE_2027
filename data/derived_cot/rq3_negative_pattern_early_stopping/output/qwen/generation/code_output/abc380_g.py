def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    p = list(map(int, data[2:2+n]))
    
    # If K == 1, then no inversion can be created, so answer is 0.
    if k == 1:
        print(0)
        return
        
    # Precompute factorials and inverse factorials for combinations if needed? 
    # But note: we are going to consider all pairs (i, j) with i < j. There are n*(n-1)//2 pairs, which is up to 200000*199999//2 ~ 20e9 pairs, which is too many to iterate over.

    # We need a smarter way.

    # Let's reframe: the expected inversion number is the sum over all pairs (i, j) (i < j) of the probability that A_i > A_j.

    # For a fixed pair (i, j), the probability is:
    #   Let p0 = 1 if i < j and p[i] > p[j] (in the original permutation) then the original relative order is 1, else 0.
    #   Let p1 = 1 if i < j and p[i] < p[j] then 0, else 1? Actually, no: the original relative order is 1 if p[i] > p[j] and 0 if p[i] < p[j]. But note: the indices i and j are fixed, and the array is given.

    # But note: the array is a permutation, so the original relative order is fixed.

    # Now, the probability that the operation changes the relative order is the probability that the chosen window contains both i and j, which is:
    #   Let L = max(1, max(i, j) - k + 1)
    #   Let R = min(i, j)
    #   Then the number of windows containing both i and j is: max(0, R - L + 1) if L <= R, else 0.
    #   Let total_windows = n - k + 1
    #   Then p = (number of windows containing both) / total_windows

    # Then the expected probability for the pair (i, j) is:
    #   If originally p[i] > p[j]: then (1 - p) * 1 + p * 0.5
    #   Else: (1 - p) * 0 + p * 0.5

    # But wait, the original relative order is fixed. However, the problem is that we cannot iterate over all pairs (n up to 200000, so pairs are 20e9) because that is too slow.

    # We need to compute the sum without iterating over each pair.

    # Let me denote:
    #   Let F(i, j) = 1 if i < j and p[i] > p[j] (original inversion) else 0.
    #   Then the expected contribution of (i, j) is: F(i, j) * (1 - p) + (1 - F(i, j)) * 0.5 * p   [if F(i, j) is 0 or 1]

    # Actually, we can write:
    #   Expected = sum_{i<j} [ F(i, j) * (1 - p) + (1 - F(i, j)) * 0.5 * p ]

    # But note: p depends on i and j.

    # We can split the sum into two parts:
    #   = sum_{i<j} F(i, j) * (1 - p) + sum_{i<j} (1 - F(i, j)) * 0.5 * p

    # But note: F(i, j) is 1 for inversions and 0 otherwise.

    # Alternatively, we can write:
    #   = sum_{i<j} [0.5 * p + 0.5 * F(i, j) * (1 - p)]   [because 1 - F(i, j) is 1 for non-inversions, and F(i, j) is 1 for inversions]

    # But wait, let me check:
    #   For an inversion (F(i, j)=1): 
    #       0.5 * p + 0.5 * (1 - p) = 0.5 * p + 0.5 - 0.5*p = 0.5
    #   For a non-inversion (F(i, j)=0):
    #       0.5