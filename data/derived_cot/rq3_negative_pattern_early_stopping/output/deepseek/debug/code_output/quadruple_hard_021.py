from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        rec, track = [0], defaultdict(int) 
        ct = start = ptr2 = 0

        if not set(s2).issubset(set(s1)): 
            return 0

        s1 = ''.join(char for char in s1 if char in set(s2))
        s1_len = len(s1)
        
        while True:
            for char in s2:
                ptr = s1.find(char, start)
                if ptr == -1:
                    ct += 1
                    ptr = s1.find(char)
                start = ptr + 1
            rec.append(ct + 1)

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            if start not in track:
                track[start] = len(rec) - 1
            else:
                break

        cycleStartIdx = track[start]
        cycleStart = rec[cycleStartIdx]
        cycle1 = ct + 1 - cycleStart
        cycle2 = len(rec) - 1 - cycleStartIdx
        rest = n1 - cycleStart

        fullCycles = rest // cycle1
        remain = rest - fullCycles * cycle1

        remCount1 = cycleStart + remain
        while rec[ptr2] <= remCount1:
            ptr2 += 1
        totalMatches = cycleStartIdx + cycle2 * fullCycles + (ptr2 - cycleStartIdx - 1)
        return totalMatches // n2