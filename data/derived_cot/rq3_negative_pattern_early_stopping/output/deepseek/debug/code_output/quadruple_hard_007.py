from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in set(s2))

        ptr_s1 = 0          # position in the current s1 string (0..len(s1)-1)
        count_s2 = 0        # number of complete s2's matched so far
        count_s1 = 0        # number of complete s1's consumed

        visited = dict()    # key: position in s2 (after finishing a s1 block)
        history = []       # list of (count_s1, count_s2) at the start of each s1 block

        while count_s1 < n1:
            state = (count_s2, count_s1)  # optional but we use s2_index differently

            for ch in s1:
                if ch == s2[ptr_s1]:
                    ptr_s1 += 1
                    if ptr_s1 == len(s2):
                        count_s2 += 1
                        ptr_s1 = 0
            count_s1 += 1

            key = ptr_s1
            if key in visited:
                prev_count_s1, prev_count_s2 = visited[key]
                cycle_s1 = count_s1 - prev_count_s1
                cycle_s2 = count_s2 - prev_count_s2
                break
            visited[key] = (count_s1, count_s2)
            history.append((count_s1, count_s2, ptr_s1))  # but we need at start of block? Actually we record after processing.




        if not set(s2).issubset(set(s1)):
            return 0
        s1_filtered = ''.join(c for c in s1 if c in set(s2))

        index_s2 = 0
        count_s2_total = 0
        count_s1_total = 0

        first_occurrence = {}
        start_states = []

        while count_s1_total < n1:
            if index_s2 in first_occurrence:
                prev_s1, prev_s2 = first_occurrence[index_s2]
                cycle_len_s1 = count_s1_total - prev_s1
                cycle_len_s2 = count_s2_total - prev_s2
                remaining_s1 = n1 - count_s1_total
                break