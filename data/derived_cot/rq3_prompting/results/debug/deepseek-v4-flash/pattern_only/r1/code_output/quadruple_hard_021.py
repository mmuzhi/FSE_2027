class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0:
            return 0

        allowed = set(s2)
        if not allowed.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in allowed)
        L = len(s1)
        total = L * n1

        rec = [0]
        track = {}
        pos = 0
        k = 0

        while True:
            for ch in s2:
                r = pos % L
                p = s1.find(ch, r)
                if p == -1:
                    p = s1.find(ch)
                    pos = (pos // L + 1) * L + p
                else:
                    pos = (pos // L) * L + p
                pos += 1

            k += 1
            rec.append(pos)

            if pos > total:
                return (k - 1) // n2
            if pos == total:
                return k // n2

            state = pos % L
            if state in track:
                prev_k = track[state]
                cycle_len = k - prev_k
                cycle_dist = rec[k] - rec[prev_k]
                remaining = total - rec[prev_k]

                full_cycles = remaining // cycle_dist
                rem_dist = remaining % cycle_dist

                extra = 0
                for i in range(prev_k + 1, k + 1):
                    if rec[i] - rec[prev_k] <= rem_dist:
                        extra += 1
                    else:
                        break

                return (prev_k + full_cycles * cycle_len + extra) // n2
            else:
                track[state] = k