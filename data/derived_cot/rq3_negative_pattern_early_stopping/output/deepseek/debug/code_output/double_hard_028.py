class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        from collections import defaultdict

        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(ch for ch in s1 if ch in set(s2))

        rec = [0]          # rec[i] = number of full s1 copies consumed after i-th s2
        track = {}         # start index -> rec index
        ct = 0             # number of full s1 copies consumed
        start = 0          # next search start index in current s1 copy
        s2_cnt = 0         # number of fully matched s2 sequences
        n = len(s1)

        while True:
            for ch in s2:
                pos = s1.find(ch, start)
                if pos == -1:
                    ct += 1
                    if ct > n1:          # not enough copies to complete this s2
                        return (s2_cnt) // n2
                    pos = s1.find(ch)
                    if pos == -1:        # should never happen after filtering
                        return 0
                start = pos + 1

            s2_cnt += 1
            rec.append(ct)

            if ct >= n1:                 # all copies used, no cycle possible
                return s2_cnt // n2

            state = start
            if state not in track:
                track[state] = len(rec) - 1
            else:
                break   # cycle found

        cycle_start_idx = track[state]          # index in rec where cycle starts
        pre_s1 = rec[cycle_start_idx]           # s1 copies before cycle
        pre_s2 = cycle_start_idx                # s2 matches before cycle
        cycle_s1 = rec[-1] - pre_s1             # s1 copies in one cycle
        cycle_s2 = s2_cnt - pre_s2              # s2 matches in one cycle

        rest = n1 - pre_s1                      # s1 copies left after pre-cycle
        full_cycles = rest // cycle_s1
        remainder = rest - full_cycles * cycle_s1

        total_s2 = pre_s2 + full_cycles * cycle_s2

        i = cycle_start_idx
        while i + 1 < len(rec) and rec[i + 1] - pre_s1 <= remainder:
            i += 1
            total_s2 += 1

        return total_s2 // n2