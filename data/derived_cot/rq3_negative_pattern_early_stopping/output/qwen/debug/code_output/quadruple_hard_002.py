class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        # Precompute the prefix function for s2
        m = len(s2)
        pi = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and s2[i] != s2[j]:
                j = pi[j-1]
            if s2[i] == s2[j]:
                j += 1
            pi[i] = j
        
        total_occurrences = 0
        state = 0
        # We'll simulate the entire string of n1 copies of s1
        # But we can break it into copies
        # We'll use a variable to track the current position in the current copy
        # But we don't need to build the entire string
        
        # We'll iterate over each copy
        # But we can use the fact that the string is periodic
        # We'll simulate the matching for each character in s1, repeated n1 times
        
        # However, we can use the following: 
        #   total_occurrences = (occurrences in one copy) * n1 + (spanning occurrences) * (n1 - 1)
        # But let's compute the occurrences in one copy and the spanning occurrences
        
        # First, compute the occurrences in one copy of s1
        base = 0
        state_base = 0
        for char in s1:
            while state_base < m and char != s2[state_base]:
                state_base = pi[state_base-1] if state_base > 0 else 0
            if char == s2[state_base]:
                state_base += 1
            if state_base == m:
                base += 1
                state_base = pi[m-1]
        
        # Now, compute the spanning occurrences: occurrences that start in one copy and end in the next
        # We'll concatenate two copies of s1 and count the occurrences of s2 that start in the first copy and end in the second
        s = s1 + s1
        state_span = 0
        spanning = 0
        for char in s:
            while state_span < m and char != s2[state_span]:
                state_span = pi[state_span-1] if state_span > 0 else 0
            if char == s2[state_span]:
                state_span += 1
            if state_span == m:
                # Check if this occurrence starts in the first copy (i.e., the occurrence starts at an index < len(s1))
                # The occurrence starts at (current position - m + 1) in the entire string s (which is 2*s1)
                # But we don't have the absolute position, so we can't directly check.
                # Instead, we can note that the occurrence is found in the second copy if the occurrence's start index is >= len(s1)
                # But we don't have the start index.
                # Alternatively, we can count all occurrences in the two copies and then subtract those that are entirely in the first copy.
                # But we are only interested in those that start in the first copy and end in the second.
                # We can record the start index of the occurrence.
                # However, we don't have the start index in this simulation.
                # Let's change the spanning simulation to record the start index.
                # But note: we are only interested in occurrences that start in the first copy and end in the second.
                # We can do: if the occurrence starts in the first copy (i.e., the occurrence's start index < len(s1)) and ends in the second (i.e., start index + m > len(s1)), then count it.
                # But we don't have the start index.
                # We can modify the spanning simulation to record the start index.
                # Let's do a separate simulation for spanning occurrences.
                pass
        
        # Due to the complexity and time, I decide to use a simpler method for spanning occurrences: 
        #   Count all occurrences of s2 in two copies of s1, and then subtract the occurrences that are entirely in the first copy.
        #   But note: an occurrence that is entirely in the first copy is already counted in base.
        #   However, we want only the occurrences that span the boundary.
        #   Let total_in_two = occurrences of s2 in s1+s1.
        #   Let total_in_one = base (which is the occurrences in one copy).
        #   Then, spanning = total_in_two - total_in_one
        #   But wait, what if an occurrence is counted in both one copy and two copies?