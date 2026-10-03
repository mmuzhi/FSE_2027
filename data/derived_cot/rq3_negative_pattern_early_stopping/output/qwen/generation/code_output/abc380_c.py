def main():
    import sys
    data = sys.stdin.read().splitlines()
    if not data:
        return
    parts = data[0].split()
    n = int(parts[0])
    k = int(parts[1])
    s = data[1].strip()
    
    # Identify all 1-blocks (0-indexed: each block is (start, end))
    blocks = []
    i = 0
    while i < n:
        if s[i] == '1':
            start = i
            while i < n and s[i] == '1':
                i += 1
            end = i - 1
            # This block is from start to end (inclusive)
            blocks.append((start, end))
        else:
            i += 1

    # We are guaranteed at least K blocks
    if len(blocks) < k:
        # But the problem guarantees at least K, so this should not happen.
        print(s)
        return

    # The (K-1)-th block and the K-th block (0-indexed: the (K-1)-th is the second block, so index K-2; the K-th is index K-1)
    prev_block = blocks[k-2]  # (l_prev, r_prev)
    curr_block = blocks[k-1]  # (l_curr, r_curr)

    # The part before the (K-1)-th block's end (i.e., up to r_prev) remains the same.
    # Then we insert the current block (which is from l_curr to r_curr) at the position after r_prev.

    # We are going to build a new string.

    # Part 1: from 0 to r_prev (inclusive) of the original string.
    part1 = s[:prev_block[1]+1]  # because prev_block[1] is the last index of the (K-1)-th block, and we want to include it.

    # Then we insert the current block (which is the substring from l_curr to r_curr) as ones.
    part2 = '1' * (curr_block[1] - curr_block[0] + 1)

    # Then we need to put zeros from (prev_block[1] + 1 + (curr_block[1] - curr_block[0] + 1) + 1) to the original end of the current block? 
    # But note: the problem says: T_i = 0 for r_{K-1} + (r_K - l_K) + 2 to r_K (in 1-indexed). 

    # In 0-indexed, the zeros should be from (prev_block[1] + 1 + (curr_block[1] - curr_block[0] + 1) + 1) to curr_block[1] (the original end of the current block) is not correct.

    # Actually, the zeros are inserted from the position after the inserted block (which is at prev_block[1]+1 to prev_block[1] + (curr_block[1]-curr_block[0]+1)) to the original end of the current block (curr_block[1])? 

    # But wait, the problem says: 
    #   T_i = 0 for r_{K-1} + (r_K - l_K) + 2 to r_K (in 1-indexed). 

    # In 0-indexed, the condition for zeros is from (prev_block[1] + 1 + (curr_block[1]-curr_block[0]+1) + 1) to curr_block[1] (if we consider 0-indexed indices) is not matching.

    # Let me re-map the problem's 1-indexed to 0-indexed:

    #   Let R_prev = prev_block[1] (0-indexed) -> in 1-indexed, the end of the (K-1)-th block is R_prev+1.
    #   The inserted block is of length L = (curr_block[1]-curr_block[0]+1). In 1-indexed, the inserted block goes from (R_prev+1+1) to (R_prev+1+L) (because the next position after the (K-1)-th block is R_prev+1 (0-indexed) which is R_prev+2 in 1-indexed? Actually, no: in 1-indexed, the next position after the (K-1)-th block (which ends at R_prev+1) is R_prev+2.

    #   The problem says: zeros from (R_prev + (r_K - l_K) + 2) to r_K (1-indexed). 
    #   Here, R_prev is the 1-indexed end of the (K-