import math
from collections import defaultdict
import sys

def is_prime(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True

def factorize(n):
    factors = defaultdict(int)
    # Check for 2 separately
    while n % 2 == 0:
        factors[2] += 1
        n //= 2
    # Now n is odd
    f = 3
    while f * f <= n:
        if n % f == 0:
            factors[f] += 1
            n //= f
        else:
            f += 2
    if n > 1:
        factors[n] += 1
    return factors

def is_400_number(n):
    if n < 36:
        return False
    factors = factorize(n)
    if len(factors) != 2:
        return False
    for exp in factors.values():
        if exp % 2 != 0:
            return False
    return True

def main():
    data = sys.stdin.read().split()
    if not data:
        return
    Q = int(data[0])
    queries = [int(data[i+1]) for i in range(Q)]
    results = []