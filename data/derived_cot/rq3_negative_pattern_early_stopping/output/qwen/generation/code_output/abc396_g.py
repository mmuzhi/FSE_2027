import sys

def main():
    data = sys.stdin.read().splitlines()
    if not data: 
        print(0)
        return
    H, W = map(int, data[0].split())
    grid = []
    for i in range(1, 1+H):
        grid.append(data[i].strip())
    
    # Precompute row0 and row1 for each row
    # row0[i] is the integer representation of the row string (as a binary number, most significant first)
    # row1[i] is the bitwise complement of row0[i] within W bits (i.e., (1<<W)-1 XOR row0[i])
    row0 = []
    row1 = []
    full_mask = (1 << W) - 1
    for s in grid:
        num = 0
        for char in s:
            num = (num << 1) | (1 if char == '1' else 0)
        row0.append(num)
        row1.append(full_mask ^ num)
    
    n = 1 << W
    # Precompute popcount for all numbers from 0 to n-1
    # But note: we need to compute popcount for numbers up to n-1 (which is 2^W - 1)
    # We can use bit_count() if using Python 3.10+
    # Alternatively, we can precompute an array popcounts for numbers from 0 to n-1.
    # But W is at most 18, so n is 262144, which is acceptable.
    # However, we can compute on the fly with bin(x).count("1") but that is slow.
    # Let's precompute a list: popcount[x] = bin(x).count("1") for x in range(n)
    # But note: n is 262144, so we can do:
    popcount_arr = [0] * n
    for x in range(n):
        # Using bit_count() is faster, but if we are in an environment without it, use bin(x).count("1")
        # But note: W is small, so we can use bin(x).count("1")
        # Alternatively, use dynamic programming for popcount for numbers up to n-1.
        # Since n is 262144, we can do:
        #   popcount_arr[x] = bin(x).count("1")
        # But bin(x).count("1") is O(W) and W is 18, so it's acceptable.
        popcount_arr[x] = bin(x).count("1")
    
    # Now, for each candidate x (from 0 to n-1), we want to compute:
    #   total = 0
    #   for i in range(H):
    #       d0 = popcount_arr[x ^ row0[i]]
    #       d1 = popcount_arr[x ^ row1[i]]
    #       total += min(d0, d1)
    # Then update the minimum total.
    #
    # But H can be 200000 and n is 262144, so the total operations is 200000 * 262144 which is about 52.4e9, which is too slow in Python.
    #
    # We need to optimize.
    #
    # Alternate approach: use the fact that the function is separable by rows and use a different representation.
    #
    # We can precompute for each row i the two masks and then use a lookup table for the entire grid? 
    #
    # But note: the grid has H rows, and we cannot avoid iterating over rows for each candidate x.
    #
    # However, we can try to use the structure of the problem. Notice that the function for each row i is:
    #   f_i(x) = min(popcount(x ^ a), popcount(x ^ b))
    # where a = row0[i], b = row1[i].
    #
    # We can precompute for each row i the two masks and then use a convolution-like approach? 
    #
    # Another idea: use the fact that the grid is given and the operations are linear. But note the min function.
    #
    # We can try to use the following: 
    #   Let F(x) = sum_i min(popcount(x ^ a_i), popcount(x ^ b_i))
    #   We can change the order of summation and use the linearity of the popcount? But the min is not linear.
    #
    # We can use the inclusion-exclusion for the min? 
    #   min(d0, d1) = (d0 + d1 - |d0-d1|)