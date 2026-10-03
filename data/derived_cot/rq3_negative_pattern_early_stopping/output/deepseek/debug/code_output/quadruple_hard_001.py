from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        rec = [0]               # rec[i]: number of s1 repeats used to match s2 i times
        track = {}              # start position -> index in rec
        start = 0               # current index in the current s1 copy
        cnt = 0                 # number of complete s1 repeats consumed

        while True:
            for ch in s2:
                idx = s1.find(ch, start)
                if idx == -1:               # need to move to the next s1 copy
                    cnt += 1
                    idx = s1.find(ch)       # must succeed because set(s2) ⊆ set(s1)
                start = idx + 1

            rec.append(cnt + 1)             # cumulative repeats after this match

            if rec[-1] > n1:                # exceeded available repeats
                return (len(rec) - 2) // n2

            if start not in track:          # new state record
                track[start] = len(rec) - 1
            else:                           # cycle detected
                break

        cycle_start_idx = track[start]          # rec index where cycle begins
        cycle_start_val = rec[cycle_start_idx] # repeats at that point
        cycle_len = rec[-1] - cycle_start_val  # repeats per cycle
        cycle_matches = len(rec) - 1 - cycle_start_idx  # matches per cycle

        remaining = n1 - cycle_start_val
        cycles = remaining // cycle_len
        rest = remaining % cycle_len
        target = cycle_start_val + rest

        ptr = cycle_start_idx
        while ptr < len(rec) and rec[ptr] <= target:
            ptr += 1
        rest_matches = ptr - cycle_start_idx - 1

        total_matches = cycle_start_idx + cycles * cycle_matches + rest_matches
        return total_matches // n2