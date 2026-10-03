import sys
from math import gcd
from functools import lru_cache

MOD = 998244353

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1+n-1]))
    
    # Precompute for each A_i the list of (P, Q) such that P*Q = A_i and gcd(P, Q)==1.
    factors_list = []
    for a in A:
        pairs = []
        # Iterate over divisors of a
        for i in range(1, int(a**0.5)+1):
            if a % i == 0:
                j = a // i
                if gcd(i, j) == 1:
                    pairs.append((i, j))
                    if i != j:
                        pairs.append((j, i))
        factors_list.append(pairs)
    
    # We'll use DP: dp[i][state] = ... but state might be too big.
    # Alternatively, we can use a different approach: since the minimal g_1 must be 1 for the sequence to have gcd 1, and the sequence is determined by the choices of pairs, then the total product is the product of the sequence with g_1=1.
    # But note, the minimal g_1 is not necessarily 1. For example, if we choose pairs that have common factors in the denominators, then g_1 might be greater than 1. But then the gcd condition requires that the entire sequence has gcd 1, which might be achieved by having g_1=1 and the reduced sequence having gcd 1.
    # Actually, from the above, the condition is that the minimal g_1 (D) must be 1 and the gcd of the reduced sequence (without g_1) must be 1.
    # But note, the reduced sequence is integers only if the denominators are cleared by D. So if D=1, then the reduced sequence must be integers. But the reduced sequence is defined by the pairs and the consistency conditions. 
    # However, the consistency conditions ensure that the sequence is integers if D is chosen to clear the denominators. 
    # But the minimal D is the least common multiple of the denominators (the products of P_j's) that appear. 
    # But then, the condition for the entire sequence to have gcd 1 is that D * G0 = 1, which implies D=1 and G0=1.
    # So, we only consider choices of pairs that yield D=1 and G0=1.
    # But how to compute D and G0 for a given choice of pairs? 
    # Alternatively, we can use a different approach: since the problem is complex, we might need to use a state in the DP that represents the current product of the denominators (or the current gcd of the sequence so far) but that state might be too large.
    # Given the complexity and the constraints (N up to 1000, A_i up to 1000), we need to find a better way.
    # Another idea: use generating functions or matrix exponentiation, but the state space is too large.
    # After reading the sample inputs and outputs, I see that the sample input 2 has 2 good sequences, and sample input 6 has 16 good sequences.
    # The number of good sequences is the product over edges of the number of valid pairs, but only if the consistency conditions (the g_i's being integers) and the gcd condition hold.
    # But the consistency conditions are automatically satisfied if we choose the pairs arbitrarily? No, because the next edge's P_i must divide the previous edge's Q_{i-1} * g_{i-1}. 
    # Actually, the consistency conditions are built into the definition of g_i = (g_{i-1} * Q_{i-1}) / P_i, and g_i must be an integer. 
    # So, for a fixed choice of pairs, the g_i's are determined by the previous g_{i-1} and the pairs. 
    # We can use a DP that goes from left to right and for each edge, we keep track of the current g_i (or the current value of the denominator factor) but the numbers can be very large.
    # But note, the minimal g_1 is the least common multiple of the denominators that appear. 
    # However, the problem asks for the sum of the scores of all good sequences. 
    # The score is the product of the sequence elements. 
    # We can use a DP that iterates over the edges and keeps track of the current product of the sequence and the current gcd. But the product and gcd can be very large.
    # But we are working modulo 998