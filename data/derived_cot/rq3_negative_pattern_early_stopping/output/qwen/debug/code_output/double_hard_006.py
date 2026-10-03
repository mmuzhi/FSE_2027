class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not s2:
            return 0
        
        s1 = ''.join(char for char in s1 if char in set(s2))
        if not s1:
            return 0
        
        L1 = len(s1)
        L2 = len(s2)
        
        # If s2 is longer than s1, then we cannot form even one s2
        if L2 > L1:
            return 0
        
        # We'll use two pointers: one for s2 and one for the long string (s1 repeated n1 times)
        # But we cannot build the long string, so we simulate.
        count = 0
        pos = 0  # current position in s2
        total_chars = 0  # total characters consumed in s1 copies
        
        # We'll record the number of complete s2 found at each step
        rec = [0]
        # We'll record the first time we encountered a particular state (pos, total_chars % L1)
        track = {}
        
        # We are allowed to use n1 copies of s1, so total_chars can be up to n1 * L1
        # We'll simulate until we either complete n1 copies or find a cycle
        
        # The state is (pos, total_chars % L1) but we can also use just pos because the matching is deterministic given the current copy index and the current position in s1.
        # However, we are limited by n1 copies, so we need to know how many copies we have used.
        # Alternatively, we can record the state as (pos, copy_index) but copy_index = total_chars // L1, and total_chars can be large.
        # Instead, we record the state as (pos, total_chars % L1) and the first time we encountered this state.
        
        # But note: the matching is deterministic given the current state and the string s1.
        # We'll record the state as (pos, total_chars % L1) and the total_chars at that state.
        # However, the total_chars is not needed for the cycle, only the state (pos, total_chars % L1) matters.
        
        # But note: the matching might depend on the copy index because we are limited by n1 copies.
        # We'll record the state as (pos, total_chars % L1) and the number of complete copies used (total_chars // L1) is not needed for the cycle but for the limit.
        
        # We'll simulate until we either complete n1 copies or find a cycle.
        # We'll use a dictionary to record the first time we encountered a state (pos, total_chars % L1)
        # But note: the state (pos, total_chars % L1) might repeat even if the copy index is different, but the matching is the same.
        
        # However, the matching is deterministic given the current state and the string s1.
        # We'll record the state as (pos, total_chars % L1) and the first time we encountered it.
        
        # But note: the total_chars is the total characters consumed, and we are limited by n1 * L1.
        # We'll simulate until we have used n1 * L1 characters or we find a cycle.
        
        # We'll also record the number of complete s2 found at each state.
        # But note: the problem is to count the number of complete s2 found, not the state.
        
        # Let's change our approach: we'll use a dictionary to record the number of complete s2 found when we first encountered a state (pos, total_chars % L1)
        # But then we can use the cycle to compute the remaining part.
        
        # However, this is complex. Let me use a simpler method.
        
        # We'll simulate the matching of s2 in the long string until we either complete n1 copies or we find a cycle in the state (pos, total_chars % L1).
        # We'll record:
        #   state = (pos, total_chars % L1)
        #   first_occurrence[state] = (count_at_this_state, total_chars_at_this_state)
        
        # But note: the count_at_this_state is the number of complete s2 found so far.
        # However, we are only interested in the number of complete s2 found when we are at a particular state.
        
        # Alternatively, we can record the number of complete s2 found at each state.
        
        # Let's do:
        #   state = (pos, total_chars % L1)
        #   first_occurrence[state] = count (the number of complete s2 found so far)
        
        # But then if we