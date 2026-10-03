import math
from functools import reduce
import sys

def factorize(n):
    factors = {}
    d = 2
    while d * d <= n:
        while n % d == 0:
            factors[d] = factors.get(d, 0) + 1
            n //= d
        d += 1
    if n > 1:
        factors[n] = factors.get(n, 0) + 1
    return factors

def get_divisors_from_factors(factors):
    divisors = [1]
    for prime, exp in factors.items():
        new_divisors = []
        for power in range(1, exp+1):
            factor_power = prime ** power
            for d in divisors:
                new_divisors.append(d * factor_power)
        divisors += new_divisors
    return sorted(set(divisors))

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    
    # If N is 0, then we need to find x,y such that x^3-y^3=0, but positive integers, so no solution. But N>=1.
    # Factorize N
    if N == 1:
        print(-1)
        return

    # Factorize N
    factors = factorize(N)
    divisors = get_divisors_from_factors(factors)
    
    # We'll iterate over divisors d (which are factors of N)
    found = False