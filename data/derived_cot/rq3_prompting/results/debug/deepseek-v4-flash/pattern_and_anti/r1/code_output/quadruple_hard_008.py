class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0:
            return 0
        if not set(s2).issubset(set(s1)):
            return 0

        m = len(s2)
        nxt = [0] * m
        cnt = [0] * m

        for i in range(m):
            idx = i
            c = 0
            for ch in s1:
                if ch == s2[idx]:
                    idx += 1
                    if idx == m:
                        c += 1
                        idx = 0
            nxt[i] = idx
            cnt[i] = c

        seen = {}
        total = 0
        idx = 0
        i = 0

        while i < n1:
            if idx in seen:
                prev_i, prev_total = seen[idx]
                cycle_len = i - prev_i
                cycle_total = total - prev_total
                cycles = (n1 - i) // cycle_len

                if cycles > 0:
                    total += cycles * cycle_total
                    i += cycles * cycle_len

                while i < n1:
                    total += cnt[idx]
                    idx = nxt[idx]
                    i += 1
                break

            seen[idx] = (i, total)
            total += cnt[idx]
            idx = nxt[idx]
            i += 1

        return total // n2