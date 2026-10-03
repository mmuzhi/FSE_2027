from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        filtered = [c for c in s1 if c in set(s2)]
        s1_len = len(filtered)
        s2_len = len(s2)

        next_state = {}
        for start in range(s1_len):
            i = start
            cnt = 0
            for ch in s2:
                while filtered[i] != ch:
                    i += 1
                    if i == s1_len:
                        i = 0
                        cnt += 1
                i += 1
                if i == s1_len:
                    i = 0
                    cnt += 1
            next_state[start] = (i, cnt + 1)  # +1 for the first copy

        total_s1 = n1
        total_s2 = 0
        cur_start = 0
        s1_used = 0
        s2_matched = 0

        seen = {}
        while s1_used < total_s1:
            if cur_start in seen:
                prev_s1, prev_s2 = seen[cur_start]
                cycle_s1 = s1_used - prev_s1
                cycle_s2 = s2_matched - prev_s2
                remaining_s1 = total_s1 - s1_used
                cycles = remaining_s1 // cycle_s1
                s1_used += cycles * cycle_s1
                s2_matched += cycles * cycle_s2
                break
            seen[cur_start] = (s1_used, s2_matched)
            next_start, add_s1 = next_state[cur_start]
            if s1_used + add_s1 > total_s1:
                break
            s1_used += add_s1
            s2_matched += 1
            cur_start = next_start

        while s1_used < total_s1:
            next_start, add_s1 = next_state[cur_start]
            if s1_used + add_s1 > total_s1:
                break
            s1_used += add_s1
            s2_matched += 1
            cur_start = next_start

        return s2_matched // n2