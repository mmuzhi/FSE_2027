import sys
from collections import defaultdict

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n]))
    
    # Precompute powers of 2 up to n (we need exponents up to n)
    max_exp = n
    pow2 = [1] * (max_exp + 1)
    for i in range(1, max_exp + 1):
        pow2[i] = (pow2[i-1] * 2) % MOD
        
    # We'll compute F(m) for m from 1 to n.
    # But note: the above formula for F(m) requires to sum over pairs (i, j) with i<j and j<m.
    # However, we cannot iterate for each m from 0 to n-1 and for each j from i+1 to m-1 because that is O(n^2).

    # Instead, we can change the order: for each j, we want to consider all i < j and then update F(m) for m from j+1 to n.

    # But note: the term for a pair (i, j) is gcd(A[i], A[j]) * 2^i * 2^(m - j - 1) = gcd(A[i], A[j]) * 2^(i + m - j - 1)

    # We can precompute the gcd contributions for each j and then for each m (>= j+1) add the contributions from all i < j.

    # However, we need to compute the sum_{i=0}^{j-1} gcd(A[i], A[j]) * 2^i for each j, and then for each m from j+1 to n, we multiply by 2^(m - j - 1) and add to F(m).

    # But note: the above formula for F(m) is:
    #   F(m) = sum_{j=0}^{m-1} [ (sum_{i=0}^{j-1} gcd(A[i], A[j]) * 2^i) * 2^(m - j - 1) ]

    # Let's define:
    #   S[j] = sum_{i=0}^{j-1} gcd(A[i], A[j]) * 2^i   (for j>=1, and S[0]=0)

    # Then F(m) = sum_{j=0}^{m-1} S[j] * pow2[m - j - 1]   (if m>=j+1, otherwise 0)

    # But note: the above formula for F(m) is correct.

    # However, the challenge is to compute S[j] for each j from 0 to n-1.

    # How to compute S[j] = sum_{i=0}^{j-1} gcd(A[i], A[j]) * 2^i ?

    # We can use a technique with divisors. For each j, we want to sum over i from 0 to j-1 the gcd(A[i], A[j]) * 2^i.

    # Let g = gcd(A[i], A[j]). Then we can group by g.

    # But note: the gcd can be any divisor of A[j]. We can iterate over divisors of A[j] and use a frequency array for the divisors.

    # However, the array A can have up to 500000 elements and each A[i] up to 100000.

    # We can use the following: for each divisor d of A[j], we want to sum_{i=0}^{j-1} [ d * (number of indices i in [0, j-1] such that gcd(A[i], A[j]) == d) * (but note: we have weights 2^i) ]

    # Actually, we need to weight by 2^i.

    # Alternatively, we can use the following identity:
    #   gcd(a, b) = sum_{d | a and d | b} phi(d)
    # But that is for counting the number of pairs with gcd=d, but here we have a weight 2^i.

    # Another idea: use the divisor technique and update a global array that stores for each divisor d, the sum of 2^i for all i (from 0 to j-1) such that d divides A[i].

    # Then, for a fixed j, let d run over divisors of A[j]. Then the contribution of divisor d to S[j] is d * (sum_{i: d divides A[i] and i<j} 2^i).

    # But note: the gcd