import math

def main():
    N = int(input().strip())
    # We are counting numbers X in [1, N] such that there exists a>=1 and b>=1 with X = 2^a * b^2.
    # Alternatively, we can count by iterating over b, but N can be up to 10^18 so we need a smarter way.

    # Another approach: note that X must be divisible by 2 and the quotient (after removing some 2's) must be a perfect square.
    # But we can also think: Let X = 2^a * b^2. Then X must be divisible by 2 and the rest (X/2^a) must be a perfect square.

    # We can also consider: Let X = 2^a * b^2. Then X is a perfect square multiplied by a power of two (at least 2^1).

    # But note: the same X might be represented in multiple ways. We want to count distinct X.

    # We can use the following: 
    #   Let S be the set of perfect squares up to N. Then the good integers are the numbers of the form 2^a * s, where s is a perfect square and a>=1, and 2^a * s <= N.

    # However, then we have to avoid double-counting. But note: the same X might be represented by two different pairs (a, s) and (a', s').

    # Alternatively, we can use inclusion-exclusion or iterate over the exponents of 2.

    # But note: the constraints (N up to 10^18) and the fact that the exponent a can be at most about 60 (because 2^60 is around 1e18) and the base b can be up to sqrt(N) (which is 1e9) is too high.

    # Another idea: 
    #   We can iterate over the exponent a (from 1 to about 60) and then for each a, we need to count the numbers of the form 2^a * b^2 <= N, but then subtract the overlaps.

    # But note: the same X might be represented by multiple a. We want to count each X only once.

    # We can use the inclusion-exclusion principle or use a sieve-like method? But N is too big.

    # Alternatively, we can use the following: 
    #   Let F(a) be the set of numbers of the form 2^a * b^2 <= N. Then the union over a from 1 to 60 of F(a) is the set of good integers.

    # Then by the inclusion-exclusion principle, we can count the union. But the sets are not disjoint and inclusion-exclusion for 60 sets is too heavy.

    # Another idea: 
    #   We can consider the minimal representation. Notice that if a number X is good, then there is a minimal a0 (>=1) such that X = 2^a0 * b^2 and b is odd? Not necessarily: because b can be even. But note: we can factor out all the 2's from b. 

    # Actually, we can write X as: 
    #   Let X = 2^k * m, with m odd. Then the condition is that there exists an a (1<=a<=k) such that (k - a) is even and m is a perfect square.

    # But note: the condition on m is independent of a. So for X to be good, m must be a perfect square and k - a must be even (for some a in [1, k]). 

    # But note: we can choose a arbitrarily (as long as 1<=a<=k). So the condition is that m is a perfect square and k is at least 1 (so X is even) and k must be at least 1 (which is given) and then we require that k - a is even. Since a can be chosen, we require that k is at least 1 and that k has the same parity as a (so we can choose a = k, k-2, k-4, ... until 1). 

    # Actually, we can choose a to be any number from 1 to k such that a ≡ k (mod 2). So if k is even, then we can choose a even (so that k-a is even) and if k is odd, then we can choose a odd (so that k-a is even). 

    # But note: the condition on m is that m is a perfect square. 

    # Therefore, the condition for X to be good is:
    #   X is even (so k>=1) and the odd part of