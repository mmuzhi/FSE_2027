import sys
from collections import defaultdict

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    max_val = 20000000  # 20 million, since max sum is 20 million
    freq = [0] * (max_val+1)
    for a in A:
        if a <= max_val:
            freq[a] += 1
    
    # We'll consider sums from 2 to 2*max_val (but our freq array is only up to max_val, so we need to handle s up to 2*max_val)
    # But note: the array elements are up to 10^7, so the maximum sum is 20 million, which is 2e7, and our freq array is of size 20 million+1, so we can only index up to 20 million.
    # But the sum s can be up to 20 million, so we need to consider s from 2 to 20 million.
    # However, we cannot iterate over all s from 2 to 20 million and for each s iterate over all a from 0 to s (which is 20 million^2 operations). 

    # We need a better way.

    # Instead, we can use the following: 
    #   We want to compute for each s (from 2 to 2*max_val) the value T(s) = sum_{a} F[a] * F[s - a]
    # But note: s - a must be between 0 and max_val. 

    # But the maximum s is 20 million, and a is from 1 to 10 million (since A_i up to 10^7), so s - a can be from 0 to 20 million.

    # We can use a convolution with FFT, but that's too heavy in Python.

    # Alternatively, we can iterate over a and for each a, iterate over multiples of powers of 2? 

    # But the problem is to compute the sum_{s} f(s) * (number of pairs (i, j) with i<=j and A_i+A_j=s)

    # But note: f(s) is the odd part of s. 

    # We can also use the following: 
    #   For each s, f(s) = s / (2^k) where 2^k is the highest power dividing s.

    # But then, we can also express: s = d * 2^k, and d is odd.

    # Then, the contribution of s is f(s) * (number of pairs (i, j) with i<=j and A_i+A_j=s) = d * (number of pairs)

    # So, we can also iterate over d (odd) and k (power of 2) such that d * 2^k <= 2*max_val.

    # Then, for each d and k, let s = d * 2^k.
    # Then, the number of pairs (i, j) with i<=j and A_i+A_j=s is:
    #   if s is even: (T(s) + F[s//2]) // 2
    #   else: T(s) // 2

    # But wait, we don't have T(s) precomputed.

    # Alternatively, we can use the frequency array to compute T(s) for each s by iterating over a from 0 to s, but that is O(s) for each s, and s up to 20 million, so total operations 20 million^2, which is 400e12, too slow.

    # We need to compute T(s) for all s up to 20 million efficiently.

    # We can use a convolution via FFT, but that's complex and slow in Python.

    # Another idea: use the fact that the array A is given and we only have up to 200,000 elements. 

    # We can use a different approach: iterate over the array and for each element a, and for each power of 2, consider the sum s = a + b, but then group by the odd part.

    # But the problem is the number of pairs is too many.

    # Let me think differently.

    # We want to compute: Sum_{i<=j} f(A_i+A_j)

    # f(x) = x / (2^k) where 2^k is the highest power dividing x.

    # We can also write: f(x) = x / (2^{v_2(x)})

    # Then, the sum is: Sum_{i<=j} (A