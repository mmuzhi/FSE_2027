from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(ch for ch in s1 if ch in set(s2))

        rec = [0]                # rec[i] = total s1 consumed after i matches of s2
        track = defaultdict(int) # maps pointer in s1 -> index in rec
        ct = 0                   # number of full s1 consumed
        start = 0                # next position in current s1 to search from

        while True:
            for ch in s2:
                pos = s1.find(ch, start)
                if pos == -1:
                    ct += 1
                    pos = s1.find(ch)
                start = pos + 1
            rec.append(ct + 1)

            if rec[-1] >= n1:
                i = len(rec) - 1
                while rec[i] > n1:
                    i -= 1
                return i // n2

            ptr = pos  # last position used in s1
            if ptr not in track:
                track[ptr] = len(rec) - 1
            else:
                break

        cycle_start_idx = track[ptr]
        cycle_len_s1 = rec[-1] - rec[cycle_start_idx]  # s1 consumed per cycle
        cycle_len_s2 = len(rec) - 1 - cycle_start_idx  # matches per cycle

        pre_s1 = rec[cycle_start_idx]
        rem_s1 = n1 - pre_s1
        full_cycles = rem_s1 // cycle_len_s1
        post_s1 = rem_s1 % cycle_len_s1

        matches = cycle_start_idx
        matches += full_cycles * cycle_len_s2
        target = pre_s1 + post_s1
        idx = cycle_start_idx + 1
        while rec[idx] <= target:
            idx += 1
        matches += (idx - cycle_start_idx - 1)

        return matches // n2