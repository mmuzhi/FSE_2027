class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        s2_set = set(s2)
        if not s2_set.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in s2_set)

        rec = [0]
        track = {}
        ct = 0
        start = 0

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

        i = track[ptr]
        j = len(rec) - 1

        cycle_copies = rec[j] - rec[i]
        cycle_s2 = j - i

        rest = n1 - rec[i]
        full_cycles = rest // cycle_copies
        rem_copies = rest % cycle_copies

        extra = 0
        while i + extra + 1 <= j and rec[i + extra + 1] - rec[i] <= rem_copies:
            extra += 1

        return (i + full_cycles * cycle_s2 + extra) // n2