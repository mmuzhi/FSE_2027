class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        allowed = set(s2)
        s1 = ''.join(ch for ch in s1 if ch in allowed)

        rec = [0]
        track = {}
        cnt = 0
        start = 0
        k = 0

        while True:
            for ch in s2:
                pos = s1.find(ch, start)
                if pos == -1:
                    cnt += 1
                    pos = s1.find(ch)
                start = pos + 1

            k += 1
            rec.append(cnt + 1)

            if rec[k] > n1:
                return (k - 1) // n2

            ptr = start - 1
            if ptr in track:
                h = track[ptr]
                cycle_copies = k - h
                cycle_reps = rec[k] - rec[h]
                rest = n1 - rec[h]

                full_cycles = rest // cycle_reps
                rem_reps = rest % cycle_reps

                extra = 0
                while extra < cycle_copies and rec[h + extra + 1] - rec[h] <= rem_reps:
                    extra += 1

                return (h + full_cycles * cycle_copies + extra) // n2

            track[ptr] = k