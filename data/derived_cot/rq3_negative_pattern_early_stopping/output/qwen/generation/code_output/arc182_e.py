import math
import bisect

def main():
    import sys
    data = sys.stdin.read().split()
    it = iter(data)
    n = int(next(it)); M_val = int(next(it)); C_val = int(next(it)); K_val = int(next(it))
    A = [int(next(it)) for _ in range(n)]
    
    # If K_val is 0, then sum is 0.
    if K_val == 0:
        print(0)
        return
        
    # Compute g = gcd(C_val, M_val)
    g = math.gcd(C_val, M_val)
    T_val = M_val // g  # period
    
    # If C_val is 0, then the shift is 0 for all k.
    if C_val == 0:
        # Then s = 0 for all k.
        s_val = 0
        x = M_val - s_val
        min_A = min(A)
        # Find R(s_val): smallest a >= x
        # Sort A for binary search
        A_sorted = sorted(A)
        # For L(s_val): if min_A < x, then L = min_A, else undefined.
        if min_A < x:
            term1 = s_val + min_A
        else:
            term1 = float('inf')
        # For R(s_val): find the smallest a >= x
        idx = bisect.bisect_left(A_sorted, x)
        if idx < len(A_sorted):
            R_val = A_sorted[idx]
            term2 = s_val + R_val - M_val
        else:
            term2 = float('inf')
        F_s = min(term1, term2)
        # But note: the problem asks for sum_{k=0}^{K_val-1} F(k)
        # Since C_val==0, s_val=0 for all k, so F(k)=F_s for all k.
        total = F_s * K_val
        print(total)
        return

    # Compute the set of critical s (multiples of g) that are in the set { M_val - a - 1, M_val - a for a in A }
    # But we need to consider s in [0, T_val * g) (which is [0, M_val))
    # We'll collect all candidate s from each a: floor((M_val - a - 1)/g)*g, ceil((M_val - a - 1)/g)*g, floor((M_val - a)/g)*g, ceil((M_val - a)/g)*g
    # But also include 0 and T_val*g - g (if necessary) but T_val*g = M_val, so s < M_val.
    critical_s = set()
    # Add boundaries
    critical_s.add(0)
    # critical_s.add(T_val * g)  # but T_val*g = M_val, and s < M_val, so we don't include M_val.
    # For each a in A, consider M_val - a - 1 and M_val - a
    for a in A:
        # For M_val - a - 1
        val1 = M_val - a - 1
        # Floor and ceil to multiples of g
        s1_floor = (val1 // g) * g
        s1_ceil = s1_floor + g if val1 % g != 0 else s1_floor
        # Ensure s1_floor and s1_ceil are in [0, M_val)
        s1_floor = max(0, s1_floor)
        s1_ceil = min(M_val - 1, s1_ceil)  # s1_ceil might be >= M_val, so clamp to M_val-1
        critical_s.add(s1_floor)
        critical_s.add(s1_ceil)
        # For M_val - a
        val2 = M_val - a
        s2_floor = (val2 // g) * g
        s2_ceil = s2_floor + g if val2 % g != 0 else s2_floor
        s2_floor = max(0, s2_floor)
        s2_ceil = min(M_val - 1, s2_ceil)
        critical_s.add(s2_floor)
        critical_s.add(s2_ceil)
    
    # Convert to list and sort
    critical_s = sorted([s for s in critical_s if s % g == 0 and 0 <= s < M_val])
    # Also, we need to include 0 and the last one (T_val*g - g) if not already included.
    # But T_val*g = M_val, so we don't include M_val.
    # Now, the critical_s are the points where L(s) or R(s) might change.
    # But