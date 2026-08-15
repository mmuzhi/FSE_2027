class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 <= 0:
            return 0

        allowed = set(s2)
        if not allowed.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in allowed)

        rec = [0]
        track = {}
        ct = 0
        start = 0
        ptr2 = 0

        while True:
            for ch in s2:
                pos = s1.find(ch, start)
                if pos == -1:
                    ct += 1
                    pos = s1.find(ch)
                start = pos + 1

            rec.append(ct + 1)

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            if start not in track:
                track[start] = len(rec) - 1
            else:
                break

        cycleStart = rec[track[start]]
        cycle1 = rec[-1] - cycleStart
        cycle2 = len(rec) - 1 - track[start]
        rest = n1 - cycleStart

        rem = cycleStart + rest % cycle1

        while rec[ptr2] <= rem:
            ptr2 += 1

        return (cycle2 * (rest // cycle1) + ptr2 - 1) // n2