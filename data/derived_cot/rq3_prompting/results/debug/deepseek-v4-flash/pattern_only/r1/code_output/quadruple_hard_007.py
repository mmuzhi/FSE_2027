class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        s2_set = set(s2)
        if not s2_set.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in s2_set)

        rec = [0]
        track = {}
        cnt = 0
        start = 0

        while True:
            for ch in s2:
                pos = s1.find(ch, start)
                if pos == -1:
                    cnt += 1
                    pos = s1.find(ch)
                start = pos + 1

            rec.append(cnt + 1)

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            if start in track:
                break
            track[start] = len(rec) - 1

        cycle_start = rec[track[start]]
        cycle_len = rec[-1] - cycle_start
        cycle_cnt = len(rec) - 1 - track[start]

        rest = n1 - cycle_start
        full_cycles = rest // cycle_len
        rem = rest % cycle_len

        limit = cycle_start + rem
        p = 0
        while rec[p] <= limit:
            p += 1

        return (full_cycles * cycle_cnt + p - 1) // n2