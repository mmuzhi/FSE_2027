class Solution:
    def areAlmostEqual(self, s1: str, s2: str) -> bool:
        if len(s1) != len(s2):
            return False
        if s1 == s2:
            return True
        
        diff = []
        for i in range(len(s1)):
            if s1[i] != s2[i]:
                diff.append((s1[i], s2[i]))
                if len(diff) > 4:
                    return False
        
        if len(diff) == 0:
            return True
        if len(diff) == 2:
            return diff[0] == diff[1][::-1]
        if len(diff) == 4:
            # Check if the four differences can be split into two swaps
            # We have two independent swaps: (a, b) and (c, d) but note: the two swaps must be disjoint and the characters must match.
            # Actually, the two swaps must be such that the first swap is (a, b) and the second swap is (b, a) or (c, d) and (d, c) but also the characters must be the same in both swaps? 
            # But note: the entire string must become equal. So the two swaps must be disjoint and the characters must be the same in both swaps? 
            # Example: s1 = "abcd", s2 = "cdab": 
            #   diff = [('a','c'), ('b','d'), ('c','a'), ('d','b')]
            #   We need to check if we can split the four differences into two pairs that are reverses.
            #   But note: the order in the string is fixed. We cannot arbitrarily reorder the differences.

            # Actually, the condition for four mismatches is that the multiset of characters in the mismatches must be the same, and the mismatches must form two independent swaps.

            # However, note: the two swaps must be disjoint and the characters must be the same in both swaps? 

            # Let me try: 
            #   s1 = "abcd", s2 = "cdab": 
            #       diff = [('a','c'), ('b','d'), ('c','a'), ('d','b')]
            #       We can split into two pairs: 
            #           pair1: ('a','c') and ('c','a') -> but note: the indices are fixed. 
            #           pair2: ('b','d') and ('d','b')

            # But wait, the condition in the code for two mismatches is that the first difference is the reverse of the last. 
            # For four mismatches, we cannot rely on the order.

            # Actually, we can check: 
            #   The set of characters in the mismatches must be the same in s1 and s2, and the mismatches must be two independent swaps.

            # But note: the entire string must be the same after swapping. 

            # Alternatively, we can count the frequency of characters in the mismatches. 

            # However, note: the problem is that the mismatches must be exactly two swaps. 

            # We can do: 
            #   Let the two swaps be (i, j) and (k, l). Then the mismatches at i and j must be a swap, and at k and l must be a swap.

            # But the code currently only checks the first and last. 

            # We need to check if the four differences can be split into two pairs, each pair being a swap.

            # We have four differences: [d0, d1, d2, d3] (each di is (char1, char2))

            # We need to find two pairs (i, j) and (k, l) such that:
            #   d_i = (a, b) and d_j = (b, a)
            #   d_k = (c, d) and d_l = (d, c)

            # But note: the indices are fixed. The mismatches are at specific positions.

            # However, the condition for the entire string to be fixed by two swaps is that the multiset of characters in s1 and s2 are the same, and the mismatches are exactly two swaps.

            # But note: the code already checks that the lengths are the same and the mismatches are collected.

            # We can try to check: 
            #   The set of characters in the mismatches from s1 must equal the set of characters in the mismatches from s2.

            # But wait, in the example s1="abcd", s2="cdab":
            #   s1 mismatches: ['a','b','c','d'] -> set: {'a','b','c','d'}
            #   s2 mismatches: ['c','d','a','b