class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0:
            return 0

        allowed = set(s2)
        if not allowed.issubset(s1):
            return 0

        s1 = ''.join(ch for ch in s1 if ch in allowed)

        rec = [0]
        track = {}
        ct = 0
        start = 0
        ptr = 0

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

            if ptr in track:
                break
            track[ptr] = len(rec) - 1

        cycle_start = rec[track[ptr]]
        cycle_blocks = ct + 1 - cycle_start
        cycle_matches = len(rec) - 1 - track[ptr]

        rest = n1 - cycle_start
        rem = cycle_start + (rest % cycle_blocks)

        ptr2 = 0
        while rec[ptr2] <= rem:
            ptr2 += 1

        return (cycle_matches * (rest // cycle_blocks) + ptr2 - 1) // n2