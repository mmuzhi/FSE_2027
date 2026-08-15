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

            if start not in track:
                track[start] = len(rec) - 1
            else:
                break

        cycle_start_s2 = track[start]
        cycle_start_s1 = rec[cycle_start_s2]
        cycle_s1 = rec[-1] - cycle_start_s1
        cycle_s2 = len(rec) - 1 - cycle_start_s2

        remaining_s1 = n1 - cycle_start_s1
        ans = cycle_start_s2 + (remaining_s1 // cycle_s1) * cycle_s2

        rem_s1 = remaining_s1 % cycle_s1
        j = 0
        while j < cycle_s2 and rec[cycle_start_s2 + j + 1] - cycle_start_s1 <= rem_s1:
            j += 1
        ans += j

        return ans // n2