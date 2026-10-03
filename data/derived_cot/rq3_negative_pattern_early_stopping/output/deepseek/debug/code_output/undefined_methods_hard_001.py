from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        rec = [0]
        track = defaultdict(int)
        ct = 0
        start = 0
        ptr = 0

        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(ch for ch in s1 if ch in set(s2))

        while True:
            for ch in s2:
                idx = s1.find(ch, start)
                if idx == -1:
                    ct += 1
                    idx = s1.find(ch)
                start = idx + 1
            rec.append(ct + 1)

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            if ptr not in track:
                track[ptr] = len(rec) - 1
            else:
                break

        cycle_start = rec[track[ptr]]
        cycle_len_s1 = (ct + 1) - cycle_start
        cycle_len_s2 = len(rec) - 1 - track[ptr]
        remaining = n1 - cycle_start
        cycles = remaining // cycle_len_s1
        remainder_s1 = remaining % cycle_len_s1

        ptr2 = 0
        rem_s1_for_remainder = cycle_start
        idx_remainder = 0
        for i in range(cycle_len_s2):
            if i > 0:
                rem_s1_for_remainder += rec[track[ptr] + i] - rec[track[ptr] + i - 1]
            if rem_s1_for_remainder <= cycle_start + remainder_s1:
                idx_remainder = i + 1

        total_s2 = track[ptr] + cycles * cycle_len_s2 + idx_remainder
        return total_s2 // n2