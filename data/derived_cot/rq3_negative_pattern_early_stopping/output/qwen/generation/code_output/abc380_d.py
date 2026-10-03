def main():
    S = input().strip()
    Q = int(input())
    queries = list(map(int, input().split()))
    n = len(S)
    # Precompute d_min for each query? But note: d_min depends on n and K.
    # But K can be up to 10^18, and n is at most 200000.
    # We need to find the smallest d_min such that (2^d_min)*n >= K.
    # We can do: d_min = ceil(log2(K / n)) if K>n else 0, but if K<=n then d_min=0.
    # But note: if n==0, but n>=1.

    # We'll write a helper function to compute the character for a given d and K (with d being the number of operations, and K the position)
    # But we are only going to use d_min (which is at most about 60) so we can do recursion.

    # However, we can also do iterative (non-recursive) to avoid recursion limits.

    # We'll create a function that given d and K, returns the character.
    # But note: d_min is the number of operations we need to consider. We can compute d_min for each query.

    # But note: the same S is used for all queries.

    # We'll compute d_min for each query K_i: the smallest d_min (non-negative integer) such that (2^d_min)*n >= K_i.

    # Then, we can use a loop (iterative) to compute the character for F(d_min) at position K_i.

    # Steps for a given K and n:
    #   d_min = 0
    #   current = n   (current length = n * (2^d_min))
    #   while current < K:
    #       d_min += 1
    #       current *= 2
    #   Then, we have d_min and current = (2^d_min)*n.

    # Then, we can simulate from d_min down to 0, but we can also simulate from 0 to d_min (but we need to go from the top).

    # Alternatively, we can use a loop that goes from d_min down to 0, but we can also go from 0 to d_min and store the path? 

    # We'll do:

    #   Let d = d_min
    #   Let pos = K
    #   Let case_inverted = 0   (0 means no inversion, 1 means inversion at the last operation)

    #   But wait, the inversion is applied at each operation if the character is in the second half.

    #   Actually, we can do:

    #       while d > 0:
    #           half = (2**(d-1)) * n
    #           if pos <= half:
    #               # In the first half, so no inversion at this operation
    #               d -= 1
    #           else:
    #               # In the second half, so we will invert the character from the previous operation
    #               pos -= half
    #               d -= 1
    #               # But we cannot determine the character until d=0, so we just mark that we need to invert at the end.

    #   But then at d=0, we return S[pos-1] and then if there was an odd number of inversions, we invert it.

    # However, we are not counting the number of inversions, but the inversion is applied at each operation in the second half.

    # Actually, we can do:

    #   Let d = d_min
    #   Let pos = K
    #   Let inv_count = 0   (number of times the character was in the second half)

    #   while d > 0:
    #       half = (2**(d-1)) * n
    #       if pos <= half:
    #           d -= 1
    #       else:
    #           inv_count += 1
    #           pos -= half
    #           d -= 1

    #   Then, the base character is S[pos-1] (if we consider d=0, the string is S, and the position is pos, which is between 1 and n).

    #   Then, we invert the base character inv_count times. But note: inverting twice gives the original. So we only care about inv_count mod 2.

    #   Then, if inv_count % 2 == 1, invert the base character.

    # But wait, is that correct?

    # Example: S0 = "aB", n=2, K=16, d_min=3.

    #   d=3, half =