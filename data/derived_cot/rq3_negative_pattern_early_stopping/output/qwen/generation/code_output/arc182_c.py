def main():
    import sys
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    
    # Primes up to 16: [2, 3, 5, 7, 11, 13]
    primes = [2, 3, 5, 7, 11, 13]
    # Precompute the exponent vector for each number from 1 to M
    # There are M numbers, each represented as a tuple of exponents for the primes
    exp_vectors = []
    for num in range(1, M + 1):
        exp_vec = []
        temp = num
        for p in primes:
            cnt = 0
            while temp % p == 0:
                cnt += 1
                temp //= p
            exp_vec.append(cnt)
        exp_vectors.append(tuple(exp_vec))
    
    # We have 6 primes. We need to compute for each prime p, the generating function for the exponent in sequences of length 1 to N.
    # But note: the sequences are of variable length from 1 to N. So, we have to consider sequences of length 1, 2, ..., N.
    # For each prime p, we can compute the generating function for the exponent in a sequence of fixed length L, and then sum over L from 1 to N.
    # However, note that the exponent for prime p in a sequence of length L is the sum of the exponents from each element in the sequence.
    # Each element is chosen independently from 1 to M, and the exponent for p in an element is given by the precomputed exp_vectors.
    #
    # Let F_p(x) = (for each element, the generating function for the exponent of p) raised to the power of L, then summed over L from 1 to N.
    # But note: the generating function for a single element for prime p is: 
    #   g_p(x) = (number of elements with exponent 0) * x^0 + (number with exponent 1) * x^1 + ... 
    # Then, for a sequence of length L, the generating function is g_p(x)^L.
    # Then, the sum for sequences of length from 1 to N is: Sum_{L=1}^{N} g_p(x)^L.
    #
    # But we don't need the entire generating function, we need the sum of (exponent + 1) for each sequence. 
    # Actually, we need the sum over sequences (of all lengths) of (exponent_p + 1). 
    # But note: the divisor function is the product of (exponent_p + 1) for all primes. And we want the sum over sequences of the divisor function.
    #
    # However, we can use the following: the divisor function is multiplicative, so the entire sum is the product (over primes) of (sum_{sequences} (exponent_p + 1))? 
    # But that is not true because the divisor function is the product of the (exponent_p + 1) for each prime, and the sequences are independent. Actually, the entire sum is:
    #   Sum_{sequences} [ ∏_{p} (exponent_p + 1) ]
    # But note that the sequences are independent, and the divisor function is multiplicative. However, the exponents for different primes are not independent (same sequence). 
    #
    # But we can use the linearity of the product and the independence of the primes? Actually, no, because the same sequence is used for all primes.
    #
    # Alternate approach: use the fact that the divisor function is multiplicative and use the generating function for the entire product. But note that the divisor function is multiplicative, so we can use the Dirichlet generating function, but that might be too complex.
    #
    # Another idea: use the multiplicative property and the fact that the divisor function is the product of (exponent_p + 1). Then, the entire sum is the product (over primes) of the sum_{sequences} (exponent_p + 1) for that prime? 
    # Let me check with a small example: N=1, M=2, primes=[2] (since 2 is the only prime <=2). 
    # Numbers: 1 and 2.
    # For prime 2: 
    #   exponent in 1: 0, in 2: 1.
    # Then, the divisor function for sequences of length 1: 
    #   (0+1)=1 for 1, (1+1)=2 for 2.
    # Total sum = 1+2 =