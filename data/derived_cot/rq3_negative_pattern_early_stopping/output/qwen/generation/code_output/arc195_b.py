def main():
    import sys
    data = sys.stdin.read().strip().split()
    if not data:
        return
    
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    B = list(map(int, data[1+n:1+2*n]))
    
    # Check fixed pairs: where both A[i] and B[i] are not -1
    fixed_s = None
    for i in range(n):
        if A[i] != -1 and B[i] != -1:
            s_val = A[i] + B[i]
            if fixed_s is None:
                fixed_s = s_val
            else:
                if fixed_s != s_val:
                    print("No")
                    return

    # If there are no fixed pairs, then we can choose s arbitrarily, but we have to choose one that works for all.
    # But note: we can set the free slots arbitrarily, so we can set s to be the minimum value that satisfies the constraints from the fixed ones and the free ones.

    # However, we must also consider the free slots: they must be non-negative.

    # Let's collect the constraints from the fixed pairs and the free slots.

    # We can set s to be at least the maximum of:
    #   For fixed pairs: s must be fixed_s (if there is at least one fixed pair)
    #   For free slots in A: at index i, if B[i] is fixed (not -1) then s must be >= B[i] (because A[i] (which we set) must be non-negative, so s = A[i] + B[i] >= B[i])
    #   Similarly, for free slots in B: at index i, if A[i] is fixed (not -1) then s must be >= A[i].

    # But note: we can rearrange A arbitrarily, so the free slots in A and B are independent? Actually, no: the entire multiset A_final must be assigned to the indices, and the condition is that for each index i, the A value assigned to i (from A_final) plus B[i] (which is fixed at that index) equals s.

    # However, we can choose the values for the free slots arbitrarily (non-negative). So we can set the free slots in A to any non-negative and similarly for B.

    # The key is: we must have a common s such that:
    #   For every index i:
    #       If A[i] is fixed, then s - B[i] must be equal to A[i] (and non-negative) and if B[i] is fixed, then s - A[i] must be equal to B[i] (and non-negative).
    #       If both are free, then we can set A[i] = s - B[i] (which must be non-negative) and B[i] = s - A[i] (which must be non-negative) but note: we are setting both arbitrarily, so we can set one and the other is determined.

    # But note: the problem allows us to set the free slots arbitrarily and then rearrange A arbitrarily. However, the condition is that the entire multiset A_final (after setting the free slots) must be such that when we assign one element of A_final to each index, then A_final[i] + B[i] = s.

    # Actually, the rearrangement is done after setting the free slots. So we can set the free slots arbitrarily and then assign the entire multiset A_final arbitrarily to the indices.

    # Therefore, the condition is: there exists an s and non-negative integers for the free slots in A and B (for the positions that are -1) such that:

    #   For every index i:
    #       Let a_i be the value in A_final at index i (if A[i] was fixed, then a_i is fixed; if free, then we set it to some non-negative integer).
    #       Then a_i + B[i] = s.

    # But note: we are allowed to set the free slots arbitrarily, so we can set the free slots in A to any non-negative and the free slots in B to any non-negative. However, the catch is that the entire multiset A_final must be consistent with the fixed values and the chosen s.

    # Actually, we can break the problem into:

    #   Let s be the common sum.

    #   Then, for each index i:
    #       If A[i] is fixed, then s must be A[i] + B[i] (if B[i] is fixed) or if B[i] is free then s must be at least A[i] (and we set B[i] = s - A[i] which must be non-negative) but wait, we can set B[i] arbitrarily so we can set it to s - A[i