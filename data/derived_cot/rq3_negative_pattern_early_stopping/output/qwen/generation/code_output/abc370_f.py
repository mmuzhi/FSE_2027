import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    total = sum(A)
    # We'll use binary search for x
    lo, hi = 0, total
    while lo < hi:
        mid = (lo + hi + 1) // 2
        # Check if mid is achievable
        if check(n, k, A, mid):
            lo = mid
        else:
            hi = mid - 1
            
    x = lo
    # Now, we need to count the number of cut lines that are never cut in any valid division achieving x.
    # First, we need to find all valid divisions that achieve x. But note: there might be multiple.
    # However, we cannot iterate over all divisions because N and K can be up to 200,000.
    # Instead, we can use the following idea:
    #   In a valid division, the cuts are between pieces. We are to count the cut lines that are never cut in any valid division.
    #   A cut line i is never cut if in every valid division, pieces i and i+1 are given to the same person.
    #
    # How to approach?
    #   We can think: a cut line is never cut if the segment boundaries never occur at that cut line.
    #   But note: the problem says "the number of cut lines that are never cut in the divisions that satisfy the conditions".
    #   So, we need to find cut lines that are not used in any valid division achieving x.
    #
    # Observation:
    #   In any valid division, the cake is divided into K consecutive segments. The cut lines that are used are exactly the boundaries between segments. There are exactly K boundaries (because it's a circle, so K cuts to break into K segments). But note: the problem says "cut line i is considered cut if pieces i and i+1 are given to different people". So, the used cut lines are the ones that separate different segments.
    #
    #   Now, the total number of cut lines is N. The ones that are never cut are the ones that are not boundaries in any valid division achieving x.
    #
    #   We can reframe: a cut line i is never cut if in every valid division achieving x, the cut line i is not used. But note: the problem says "in the divisions that satisfy the conditions", meaning we are to count the cut lines that are not used in any of the divisions that achieve x.
    #
    #   However, counting over all divisions is hard. Instead, we can use the following:
    #   Consider that the cake is circular. We can break the circle at a fixed point (say between piece N and piece 1) and then consider the linear array. But then we have to account for circularity.
    #
    #   Alternatively, we can use the idea from the check function: we can find all the boundaries (cuts) that are used in a valid division. But note: there might be multiple valid divisions. We need to find the set of cut lines that are never used in any valid division.
    #
    #   Let's define:
    #   Let F be the set of cut lines that are used in at least one valid division achieving x.
    #   Then, the answer for y is N - |F|.
    #
    #   But how to compute F?
    #   We can use the following: in a valid division, the boundaries are the points where the cumulative sum (from a starting point) reaches a multiple of x (or more precisely, the boundaries are the points where the cumulative sum is exactly x, 2x, 3x, ... Kx). But note: the segments must be consecutive and the entire cake must be partitioned, so the boundaries are the points where the cumulative sum is a multiple of x (but not necessarily exactly, because the segments can be more than x, but the boundaries are the points where the cumulative sum is at least the next multiple of x? Actually, no: the boundaries are the points where the cumulative sum from the start of the segment is exactly the end of a segment (which is at least x). But the segments can be more than x, so the boundaries are not fixed.
    #
    #   Actually, the boundaries are the points where the cumulative sum (from a fixed starting point) is exactly the sum of the segments. But because the cake is circular, we can start anywhere.
    #
    #   Another idea: use the fact that the valid divisions are those that have K segments, each with sum >= x, and the entire cake is covered. The boundaries are the points where the cumulative sum (from a fixed start) is exactly the sum