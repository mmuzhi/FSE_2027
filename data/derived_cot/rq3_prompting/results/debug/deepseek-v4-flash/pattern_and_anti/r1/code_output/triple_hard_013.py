class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        rec = [0]
        track = {}
        ct = 0
        start = 0

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

            state = start
            if state not in track:
                track[state] = len(rec) - 1
            else:
                break

        cycle_start = track[state]
        cycle_end = len(rec) - 1

        cycle_s1 = rec[cycle_end] - rec[cycle_start]
        cycle_s2 = cycle_end - cycle_start

        rest = n1 - rec[cycle_start]
        full_cycles = rest // cycle_s1
        remaining_s1 = rest % cycle_s1

        extra = 0
        while extra < cycle_s2 and rec[cycle_start + extra + 1] - rec[cycle_start] <= remaining_s1:
            extra += 1

        total_s2 = cycle_start + full_cycles * cycle_s2 + extra
        return total_s2 // n2