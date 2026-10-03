import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        return
    nq_line = data[0].split()
    n = int(nq_line[0])
    q = int(nq_line[1])
    s = data[1].strip()
    queries = []
    for i in range(2, 2+q):
        parts = data[i].split()
        L = int(parts[0])
        R = int(parts[1])
        queries.append((L, R))
    
    # Precompute arrays for the entire string S
    # We'll create three arrays: 
    #   left_ones[i]: number of '1's from the start of S to i (inclusive)
    #   left_twos[i]: number of '2's from the start of S to i (inclusive)
    #   left_slash[i]: the position of the next '/' to the right? Actually, we need to precompute for each position the cumulative counts.

    # Alternatively, we can precompute prefix sums for '1', '2', and the positions of '/'.

    # Let's create:
    #   pre1[i] = number of '1's in S[0:i] (i characters)
    #   pre2[i] = number of '2's in S[0:i]
    #   pre_slash[i] = the index of the next '/' after position i, or -1 if none.

    # But we need to answer queries [L, R]. We can use a Fenwick tree or segment trees, but note that the constraints are 10^5 and we have 10^5 queries, so we need O(1) or O(log n) per query.

    # Alternatively, we can precompute arrays for the entire string and then use binary search to get the counts in [L, R].

    # Let's define:
    #   pre1[i] = number of '1's from 0 to i-1 (if we use 0-indexed and pre1[i] for prefix up to i)
    # But we can use:
    #   Let A1[i] = 1 if S[i]=='1' else 0
    #   Then pre1[i] = prefix sum of A1 up to i.

    # Similarly for '2' and for '/'.

    # But we also need to consider the positions of '/'.

    # Actually, we can do:

    # Precompute:
    #   pre1[i] = number of '1's in S[0:i]
    #   pre2[i] = number of '2's in S[0:i]
    #   pre_slash[i] = the number of '/' in S[0:i]

    # But then for a query [L, R] (1-indexed), we can compute:
    #   total_ones = pre1[R] - pre1[L-1]
    #   total_twos = pre2[R] - pre2[L-1]

    # But that doesn't help directly because we need to know the counts on the left and right of a '/'.

    # Another idea:

    # We can precompute for each '/' the maximum a we can form with that '/' as the center. Then, the answer for the query is the maximum a (over all '/' in [L, R]) such that a <= (number of '1's to the left of the '/' in [L, R]) and a <= (number of '2's to the right of the '/' in [L, R]), and then the total length is 2*a+1.

    # But note: the left part is from L to the position of the '/' (exclusive) and the right part is from the position of the '/' (exclusive) to R.

    # So, for a given '/' at position i (0-indexed) in the entire string, the left part in the query [L, R] is from L-1 to i-1 (if we use 0-indexed indices) and the right part is from i+1 to R-1.

    # We can precompute:
    #   For each position i, let left_ones[i] = number of '1's in S[0:i] (from 0 to i-1)
    #   Similarly, right_twos[i] = number of '2's in S[i+1:n] (from i+1 to n-1)

    # But then, for a query [L, R] and a '/' at position i (0-indexed) that lies in [L-1, R-1] (if we consider 0-indexed indices for S), the left part is from L-1 to i-1 and the right part is from i+1 to R-1.

    # So, the number of