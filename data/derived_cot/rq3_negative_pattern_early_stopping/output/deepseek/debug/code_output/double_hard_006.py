from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in set(s2))

        rec = [0]  # 0 s2 matched -> 0 s1 used
        track = {}
        ct = 0       # number of full s1 strings completely used
        start = 0    # current search start in s1 (a single s1 instance, not repeated)
        ptr2 = 0     # will be used later as a pointer into rec

        while True:
            for ch in s2:
                pos = s1.find(ch, start)
                if pos == -1:
                    ct += 1
                    pos = s1.find(ch)
                    if pos == -1:
                        return 0
                start = pos + 1

            rec.append(ct + 1)

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            state = start  
            if state not in track:
                track[state] = len(rec) - 1
            else:
                break

        cycleStartRec = track[state]          # rec index where the cycle started
        cycleStartVal = rec[cycleStartRec]    # s1 units at start of cycle
        cycleLen = len(rec) - 1 - cycleStartRec   # number of s2 matches in the cycle
        cycleS1 = ct + 1 - cycleStartVal          # s1 units consumed in the cycle

        remainingS1 = n1 - cycleStartVal          # s1 units left after we exit the cycle start
        cycles = remainingS1 // cycleS1            # full cycles we can take
        leftoverS1 = remainingS1 % cycleS1        # s1 units after cycling

        totalS2 = cycleStartRec + cycles * cycleLen

        rem = cycleStartVal + leftoverS1
        while rec[ptr2] <= rem:
            ptr2 += 1
        totalS2 += ptr2 - 1 - cycleStartRec

        return totalS2 // n2