class Solution:
    def shiftDistance(self, s: str, t: str, nextCost: List[int], previousCost: List[int]) -> int:
        n = len(s)
        # Precompute the total cost for a full cycle for next and previous
        full_cycle_next = sum(nextCost)
        full_cycle_prev = sum(previousCost)
        
        # Precompute prefix sums for nextCost and previousCost for quick range sum
        # For nextCost, we'll create a prefix sum array of length 27 (0 to 26)
        next_prefix = [0] * 27
        for i in range(1, 27):
            next_prefix[i] = next_prefix[i-1] + nextCost[i-1]
        
        prev_prefix = [0] * 27
        for i in range(1, 27):
            prev_prefix[i] = prev_prefix[i-1] + previousCost[i-1]
        
        total_cost = 0
        
        for i in range(n):
            a = ord(s[i]) - ord('a')
            b = ord(t[i]) - ord('a')
            # Calculate minimal forward steps
            d_forward = (b - a + 26) % 26
            # The forward steps cost is the sum of nextCost from a to a + d_forward - 1 (mod 26)
            # But note: if d_forward is 0, then no steps needed.
            # The sequence for forward: from a to a+d_forward-1 (if we don't wrap, but if we wrap, we need to break the sum into two parts? Actually, the minimal forward steps is d_forward, and the letters are consecutive in the circular alphabet. But we can use the prefix sum by considering the circular nature.
            # However, note: the minimal forward steps is d_forward, and the starting letter is a, then a+1, ..., a+d_forward-1 (all mod 26). But the prefix sum we built is for the linear array of 26 letters (0 to 25). 
            # But d_forward can be 0 to 25. We can compute the sum as:
            #   If d_forward == 0, then 0.
            #   Otherwise, we need to sum nextCost from a to a+d_forward-1 (if a+d_forward-1 < 26, then it's a contiguous segment). But if a+d_forward-1 >= 26, then we wrap around.
            # Actually, the minimal forward steps is d_forward, and the letters are consecutive. We can compute the sum by:
            #   Let start = a, end = a + d_forward - 1 (mod 26). But we can break the sum into two parts if it wraps.
            # Alternatively, we can use the prefix sum by duplicating the array? But that might be overkill.
            # Instead, we can compute the sum for the forward steps as:
            #   If d_forward == 0:
            #       forward_cost = 0
            #   Else:
            #       We need to sum nextCost from a to a+d_forward-1 (mod 26). But note, the nextCost array is for letters 0 to 25, and the steps are from letter a to a+1, a+2, ... until a+d_forward-1 (mod 26). 
            #       We can break the range [a, a+d_forward-1] (mod 26) into two parts if it crosses 26.
            # But there's a simpler way: the minimal forward steps is d_forward, and the cost is the sum of nextCost for the letters from a to a+d_forward-1 (without wrapping) if a+d_forward <= 26, but if it wraps, then we can use the prefix sum by:
            #   Let total_forward = 0
            #   Let current = a
            #   For _ in range(d_forward):
            #       total_forward += nextCost[current]
            #       current = (current + 1) % 26
            # But d_forward can be up to 25, and we have 10^5 indices, so doing a loop for each index is O(25 * 10^5) = 2.5e6, which is acceptable in Python? Maybe, but we can do better with prefix sums.

            # Alternatively, we can precompute a circular prefix sum for nextCost and previousCost. But given the constraints (26 letters), we can precompute the cost for any starting letter and any number of steps (up to 25) by having a 2D array, but that's 26*26=676 entries, which is acceptable. But we