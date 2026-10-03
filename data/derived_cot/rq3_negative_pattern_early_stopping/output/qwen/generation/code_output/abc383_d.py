import math

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.isqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def main():
    N = int(input().strip())
    count = 0

    # Type 1: p^8
    p = 2
    while True:
        power8 = p ** 8
        if power8 > N:
            break
        count += 1
        p += 1

    # Type 2: (p*q)^2, where p and q are distinct primes
    # We need to count pairs (p, q) with p < q (to avoid duplicates) such that (p*q)^2 <= N.
    # But note: the same number might be represented by different pairs? Actually, no, because the prime factorization is unique.
    # However, we must generate all pairs (p, q) with p < q and (p*q)^2 <= N.

    # We can do: iterate over primes p, then for each p, iterate over primes q (with q > p) until (p*q)^2 <= N.

    # But note: N can be up to 4e12, so (p*q) <= sqrt(N) which is 2e6. So the product p*q must be <= sqrt(N) (which is 2e6 for N=4e12).

    # We can generate all primes up to sqrt(N) (which is 2e6) and then count pairs.

    # However, generating primes up to 2e6 is feasible.

    # Alternatively, we can iterate p from 2 to sqrt(N) (but then q from p+1 to sqrt(N)/p) but we need to know primes.

    # Let's generate all primes up to sqrt(N) (which is 2e6 for N=4e12). But note: the product p*q must be <= sqrt(N). So the primes p and q must be <= sqrt(N). Actually, if p and q are both greater than sqrt(N), then p*q > N, but wait: we are taking square root of N for the condition (p*q)^2 <= N, so p*q <= sqrt(N). Therefore, both p and q must be <= sqrt(N).

    # Steps for Type 2:
    # 1. Generate all primes up to sqrt(N) (which is about 2e6 for N=4e12).
    # 2. For each prime p, we consider primes q (with q > p) such that p*q <= sqrt(N). Then (p*q)^2 <= N.

    # But note: the condition is (p*q)^2 <= N, so p*q <= sqrt(N). So we need to consider primes up to sqrt(N).

    # However, sqrt(N) can be as large as 2e6, which is acceptable to generate primes with a sieve.

    # But note: N can be as low as 1, so we must handle that.

    # Alternatively, we can use the is_prime function for numbers up to sqrt(N) (which is 2e6) but generating primes with a sieve is more efficient.

    # Since N can be up to 4e12, sqrt(N) is 2e6. We can generate primes up to 2e6.

    # Let's do:

    # If N < 4, then Type 2: (p*q)^2 <= N, but the smallest (p*q)^2 is (2*3)^2=36, so if N < 36, then Type 2 count is 0.

    # We'll generate primes up to int(math.isqrt(N)) + 1.

    # But note: the product p*q must be <= sqrt(N). So we need primes up to sqrt(N). However, if we generate primes up to sqrt(N) (which is about 2e6 for N=4e12) then we can use them.

    # However, note that the condition for Type 2 is (p*q)^2 <= N, so p*q <= sqrt(N). Therefore, we need primes up to sqrt(N).

    # But note: the primes p and q must be distinct and p < q, and p*q <= sqrt(N). So we can:

    #   Let M = int(math.isqrt(N))   [M = floor(sqrt(N))]

    #   Generate all primes up to M.

    #   Then, for each prime p (from the list) and for each prime q (from the list, with q > p