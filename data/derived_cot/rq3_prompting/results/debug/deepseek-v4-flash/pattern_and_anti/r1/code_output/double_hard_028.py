class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not s1 or not s2 or n1 == 0:
            return 0
        if not set(s2).issubset(set(s1)):
            return 0

        m = len(s2)
        nxt = [0] * m
        add = [0] * m

        for p in range(m):
            q = p
            cnt = 0
            for ch in s1:
                if ch == s2[q]:
                    q += 1
                    if q == m:
                        cnt += 1
                        q = 0
            nxt[p] = q
            add[p] = cnt

        p = 0
        total = 0
        seen = {}
        i = 0

        while i < n1:
            if p in seen:
                prev_i, prev_total = seen[p]
                cycle_len = i - prev_i
                cycle_count = total - prev_total
                cycles = (n1 - i) // cycle_len
                total += cycles * cycle_count
                i += cycles * cycle_len

                while i < n1:
                    total += add[p]
                    p = nxt[p]
                    i += 1
                break

            seen[p] = (i, total)
            total += add[p]
            p = nxt[p]
            i += 1

        return total // n2