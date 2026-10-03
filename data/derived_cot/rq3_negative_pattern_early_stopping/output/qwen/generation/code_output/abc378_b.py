def main():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    index = 1
    garbage = []
    for _ in range(n):
        q = int(data[index]); r = int(data[index+1]); index += 2
        garbage.append((q, r))
    
    q_count = int(data[index]); index += 1
    queries = []
    for _ in range(q_count):
        t = int(data[index]); d = int(data[index+1]); index += 2
        queries.append((t, d))
    
    # We'll store the parameters for each garbage type (0-indexed)
    # For each query, we have (t, d) where t is the type index (1-indexed) so we use t-1.
    # Condition: d ≡ r (mod q)  => d % q == r? But note: if d % q == r, then d is a collection day.
    # However, if d % q != r, then we need to find the smallest day >= d such that day % q == r.

    # But note: the modulus condition: the day must be >= d. We can compute:
    # Let base = d
    # We want day = d + k (for k>=0) such that (d + k) % q == r.

    # Alternatively, we can compute the next day by:
    # Let remainder = (d % q) 
    # But note: the condition is (d + k) % q = r.
    # We can solve for k: (d + k) ≡ r (mod q)  => k ≡ (r - d) mod q, but we need the smallest non-negative k.

    # However, note: if d % q == r, then k=0 is a solution.

    # But wait: the modulus condition might not be linear because of negative? We can adjust:

    # Let rem = d % q
    # Then we require (rem + k) % q = r. But note: k must be chosen so that (rem + k) mod q = r.

    # Actually, we can compute:
    # Let diff = (r - rem) % q   but then we have to consider that if (rem + k) mod q = r, then k mod q = (r - rem) mod q?
    # However, note: (rem + k) mod q = (rem mod q + k mod q) mod q, but k is non-negative and we want the smallest k.

    # Alternatively, we can compute:
    # Let k0 = (r - rem) % q   but if (r - rem) is negative, then we adjust by adding q until positive.

    # Actually, we can do:
    # Let k = (r - rem) % q
    # But note: if (r - rem) is negative, then (r - rem) % q gives a positive value. However, we can also compute:
    #   k = (r - rem + q) % q   but then if (r - rem) is negative, then (r - rem + q) is positive and then mod q gives the same as (r - rem) mod q.

    # However, note: if (r - rem) is negative, then (r - rem) % q is the same as (r - rem + q) % q? Actually, in Python, the modulus operation for negative numbers gives a non-negative result.

    # But let's test: 
    #   Example: q=7, r=3, d=1 -> rem=1, then (3-1)=2, so k=2 -> day=3.
    #   Example: d=3: rem=3, then (3-3)=0, so k=0 -> day=3.
    #   Example: d=4: rem=4, then (3-4) = -1, then (-1)%7 = 6, so day=4+6=10.

    # However, wait: the condition for d=4: 
    #   We want the smallest day >=4 such that day %7 ==3.
    #   The next day after 4 that is 3 mod7: 3,10 -> but 3 is less than 4, so we need the next one: 10.

    # But note: the modulus condition: the day must be >= d. So we cannot use a day less than d.

    # Therefore, we need to compute the smallest k>=0 such that (d + k) % q == r and d+k >= d (which is always true).

    # We can compute:
    #   Let rem = d