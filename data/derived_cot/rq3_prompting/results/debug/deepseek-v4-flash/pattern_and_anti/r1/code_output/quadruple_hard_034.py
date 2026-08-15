from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0 or not s2:
            return 0

        need = set(s2)
        if not need.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in need)

        rec = [0]
        track = defaultdict(int)
        ct = 0
        start = 0
        ptr2 = 0

        while True:
            for ch in s2:
                ptr = s1.find(ch, start)
                if ptr == -1:
                    ct += 1
                    ptr = s1.find(ch)
                start = ptr + 1

            rec.append(ct + 1)

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            if ptr not in track:
                track[ptr] = len(rec) - 1
            else:
                break

        cycle_start = rec[track[ptr]]
        cycle_copies = rec[-1] - cycle_start
        cycle_matches = len(rec) - 1 - track[ptr]

        rest = n1 - cycle_start
        rem = cycle_start + rest % cycle_copies

        while rec[ptr2] <= rem:
            ptr2 += 1

        return (cycle_matches * (rest // cycle_copies) + ptr2 - 1) // n2