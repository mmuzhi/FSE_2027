def main():
    import sys
    data = sys.stdin.read().split()
    if not data:
        return
    
    n = int(data[0])
    m = int(data[1])
    pieces = []
    R_set = set()
    B_set = set()
    S_set = set()
    T_set = set()
    
    index = 2
    for i in range(m):
        a = int(data[index]); b = int(data[index+1]); index += 2
        pieces.append((a, b))
        R_set.add(a)
        B_set.add(b)
        S_set.add(a+b)
        T_set.add(a-b)
    
    # Compute |A|, |B|, |C|, |D|
    A_size = len(R_set) * n
    B_size = len(B_set) * n
    
    def diag_length(s, N):
        if s < 2 or s > 2*N:
            return 0
        if s <= N+1:
            return s-1
        else:
            return 2*N+1 - s

    C_size = 0
    for s in S_set:
        C_size += diag_length(s, n)
    
    def anti_diag_length(d, N):
        low = max(1, d+1)
        high = min(N, N+d)
        if high < low:
            return 0
        return high - low + 1

    D_size = 0
    for d in T_set:
        D_size += anti_diag_length(d, n)
    
    # Two-way intersections
    AB_size = len(R_set) * len(B_set)
    
    AC_size = 0
    for i in R_set:
        for s in S_set:
            j = s - i
            if 1 <= j <= n:
                AC_size += 1
                
    AD_size = 0
    for i in R_set:
        for d in T_set:
            j = i - d
            if 1 <= j <= n:
                AD_size += 1
                
    BC_size = 0
    for j in B_set:
        for s in S_set:
            i = s - j
            if 1 <= i <= n:
                BC_size += 1
                
    BD_size = 0
    for j in B_set:
        for d in T_set:
            i = j + d
            if 1 <= i <= n:
                BD_size += 1
                
    CD_size = 0
    for s in S_set:
        for d in T_set:
            # Solve: i+j = s, i-j = d -> i = (s+d)/2, j = (s-d)/2
            if (s+d) % 2 != 0 or (s-d) % 2 != 0:
                continue
            i_val = (s+d)//2
            j_val = (s-d)//2
            if 1 <= i_val <= n and 1 <= j_val <= n:
                CD_size += 1
                
    # Three-way intersections
    ABC_size = 0
    for i in R_set:
        for j in B_set:
            s_val = i+j
            if s_val in S_set:
                ABC_size += 1
                
    ABD_size = 0
    for i in R_set:
        for j in B_set:
            d_val = i-j
            if d_val in T_set:
                ABD_size += 1
                
    ACD_size = 0
    for i in R_set:
        for s in S_set:
            j_val = s - i
            if 1 <= j_val <= n:
                d_val = i - j_val
                if d_val in T_set:
                    ACD_size += 1
                    
    BCD_size = 0
    for j in B_set:
        for s in S_set:
            i_val = s - j
            if 1 <= i_val <= n:
                d_val = i_val - j
                if d_val in T_set:
                    BCD_size += 1
                    
    # Four-way intersection
    ABCD_size = 0
    for i in R_set:
        for j in B_set:
            s_val = i+j
            d_val = i-j
            if s_val in S_set and d_val in T_set:
                ABCD_size += 1
                
    # Inclusion-exclusion
    total_forbidden = (A_size + B_size + C_size + D_size) - (AB_size + AC_size + AD_size + BC_size + BD_size + CD_size) + (ABC_size + ABD_size + ACD_size + BCD_size) - ABCD_size
    
    total_squares = n * n
    safe_squares = total_squares - total_for