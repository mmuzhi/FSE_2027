import sys
from collections import defaultdict
from math import isqrt

MOD = 998244353

def factorize(n):
    factors = defaultdict(int)
    temp = n
    while temp % 2 == 0:
        factors[2] += 1
        temp //= 2
    f = 3
    while f * f <= temp:
        if temp % f == 0:
            factors[f] += 1
            temp //= f
        else:
            f += 2
    if temp > 1:
        factors[temp] += 1
    return factors

def get_primes_up_to(n):
    sieve = [True] * (n+1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5)+1):
        if sieve[i]:
            for j in range(i*i, n+1, i):
                sieve[j] = False
    return [i for i, prime in enumerate(sieve) if prime]

def is_good(n):
    if n == 1:
        return False
    factors = factorize(n)
    # Condition: at least one prime factor (other than 3) satisfies:
    #   if p ≡ 1 mod 3, then (exponent+1) % 3 == 0
    #   if p ≡ 2 mod 3, then (exponent+1) % 2 == 0 (i.e., even)
    for p, exp in factors.items():
        if p == 3:
            continue
        if p % 3 == 1:
            if (exp + 1) % 3 == 0:
                return True
        else:  # p % 3 == 2
            if (exp + 1) % 2 == 0:
                return True
    return False