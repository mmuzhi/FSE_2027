import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # Precompute left distinct counts: left[i] = distinct numbers in A[0:i] (i elements, from 0 to i-1)
    left = [0] * (n+1)
    freq_left = [0] * (n+1)  # since A_i between 1 and n, we can use index up to n
    distinct_left = 0
    for i in range(1, n+1):
        # left[i] is the distinct count for A[0:i-1] (if i>=1)
        # But we are building left for i from 0 to n: left[0]=0, then for i>=1, we update with A[i-1]
        if i > 1:
            # We are at the i-th step, and we are going to update for the i-th element (index i-1)
            # But we want left[i] to be the distinct count for the prefix ending at i-1.
            # So we can compute left[i] from left[i-1] and the new element A[i-1]
            # But note: we are iterating i from 1 to n, and we want left[i] = distinct count for A[0:i-1]
            # Actually, we can compute left[i] by updating from left[i-1] and A[i-1]
            if freq_left[A[i-1]] == 0:
                distinct_left += 1
            freq_left[A[i-1]] += 1
            left[i] = distinct_left
        else:
            # i==1: then left[1] = distinct count for A[0:1] = [A[0]]
            if i == 1:
                freq_left[A[0]] = 1
                distinct_left = 1
                left[i] = distinct_left
            # But we already handled i>1 and i==1 separately. Actually, we can do without the if-else for i==1 by starting the loop from i=1 and then for i=1, we do the same as i>1 but then we need to initialize for i=1.
            # Let's restructure: we'll compute left[0]=0, then for i from 1 to n, left[i] = distinct count for A[0:i]
            # But the problem: left[i] should be for the prefix of length i (0-indexed, indices 0 to i-1). 
            # We can do:
            #   left[0] = 0
            #   for i from 1 to n:
            #       if freq_left[A[i-1]] == 0:
            #           distinct_left += 1
            #       freq_left[A[i-1]] += 1
            #       left[i] = distinct_left
            # But then left[i] is the distinct count for A[0:i] (i elements). However, in our split, the left part is [0, i-1] (i elements). So that matches.
            # But then our left[i] is defined for the prefix of length i (0-indexed, i elements). And in the split, the left part is [0, i-1] (i elements). So we are good.
            # However, in the above code, we did an if-else for i==1 separately. We can remove that and do a unified loop.
            # Let's recompute left properly.
            pass

    # Let's recompute left properly in a unified way.
    left = [0] * (n+1)
    freq_left = [0] * (n+1)
    distinct_left = 0
    # left[0] = 0
    for i in range(1, n+1):
        # We are considering the prefix of length i (indices 0 to i-1)
        if freq_left[A[i-1]] == 0:
            distinct_left += 1
        freq_left[A[i-1]] += 1
        left[i] = distinct_left

    # Precompute right distinct counts: right[i] = distinct numbers in A[i:N]
    right = [0] * (n+1)
    freq_right = [0] * (n+1)
    distinct_right = 0
    # right[n] = 0
    # We'll do from the end.
    for i in range(n-1, -1, -1):
        if freq_right[A[i]] == 0:
            distinct_right += 1
        freq_right[A[i]] += 1
        right[i] = distinct_right

    # Now