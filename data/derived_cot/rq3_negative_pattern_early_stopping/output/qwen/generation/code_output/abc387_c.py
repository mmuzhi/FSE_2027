def count_le(X):
    if int(X) < 10:
        return 0
    n = len(X)
    total = 0
    # Count numbers with digits less than n
    for d in range(2, n):
        # For each digit length d, the total Snake numbers is sum_{a=1}^{9} (a)^(d-1)
        s = 0
        for a in range(1, 10):
            s += a**(d-1)
        total += s

    # Count n-digit numbers <= X
    a0_max = min(9, int(X[0]))
    # Part 1: first_digit from 1 to a0_max-1
    for a0 in range(1, a0_max):
        total += a0**(n-1)

    # Part 2: first_digit = a0_max
    if a0_max > 0:
        remaining_str = X[1:]
        # If there's no remaining part, then n==1, but n>=2 so we don't need to worry.
        count_remaining = count_le_remaining(remaining_str, a0_max)
        total += count_remaining
    return total

def count_le_remaining(Y, a):
    # Y is a string of digits (the remaining part)
    # a is the maximum digit (0 to a-1)
    m = len(Y)
    from functools import lru_cache

    @lru_cache(maxsize=None)
    def dfs(i, tight):
        if i == m:
            return 1
        total = 0
        # Determine the upper bound for the current digit
        if tight:
            high_bound = int(Y[i])
        else:
            high_bound = a-1
        high_bound = min(high_bound, a-1)
        for d in range(0, high_bound+1):
            new_tight = tight and (d == int(Y[i]))
            total += dfs(i+1, new_tight)
        return total

    return dfs(0, True)

def main():
    import sys
    data = sys.stdin.read().split()
    L = data[0]
    R = data[1]
    # Count numbers <= R and subtract numbers < L (i.e., <= L-1)
    # But note: L and R are strings because they can be up to 10^18.
    # We need to compute count_le(R) - count_le(str(int(L)-1))
    # But L can be as small as 10, so int(L)-1 might be 9, which is a 1-digit number, and our count_le function handles that.

    # However, we must be cautious: if L is "10", then L-1 is "9", and count_le("9") returns 0 (since 9 is 1-digit and our count_le only counts numbers>=10).

    # But note: our count_le function: 
    #   if int(X) < 10: return 0
    #   Then, for X="9", it returns 0.

    # So we can do:

    L_minus = str(int(L) - 1)
    count_R = count_le(R)
    count_L_minus = count_le(L_minus)
    print(count_R - count_L_minus)

if __name__ == '__main__':
    main()