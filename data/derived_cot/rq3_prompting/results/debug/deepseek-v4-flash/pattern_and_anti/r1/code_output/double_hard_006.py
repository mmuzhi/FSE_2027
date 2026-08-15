class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0:
            return 0

        rec, track = [0], {}
        ct = start = ptr2 = 0

        if not set(s2).issubset(set(s1)):
            return 0

        s2_set = set(s2)
        s1 = ''.join(ch for ch in s1 if ch in s2_set)

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

        cycleStart = rec[track[ptr]]
        cycle1 = ct + 1 - cycleStart
        cycle2 = len(rec) - 1 - track[ptr]
        rest = n1 - cycleStart

        rem = cycleStart + rest % cycle1

        while rec[ptr2] <= rem:
            ptr2 += 1

        return (cycle2 * (rest // cycle1) + ptr2 - 1) // n2