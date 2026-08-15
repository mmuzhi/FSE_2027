class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0 or n2 == 0 or not s2:
            return 0

        s1_set = set(s1)
        s2_set = set(s2)
        if not s2_set.issubset(s1_set):
            return 0

        s1 = [c for c in s1 if c in s2_set]
        n = len(s2)

        nxt = [0] * n
        cnt = [0] * n

        for start in range(n):
            p = start
            matched = 0
            for ch in s1:
                if ch == s2[p]:
                    p += 1
                    if p == n:
                        p = 0
                        matched += 1
            nxt[start] = p
            cnt[start] = matched

        total = 0
        p = 0
        seen = {}
        i = 0

        while i < n1:
            if p in seen:
                prev_i, prev_total = seen[p]
                cycle_len = i - prev_i
                cycle_total = total - prev_total
                if cycle_len > 0:
                    cycles = (n1 - i) // cycle_len
                    if cycles > 0:
                        total += cycles * cycle_total
                        i += cycles * cycle_len
                        if i == n1:
                            break
            seen[p] = (i, total)
            total += cnt[p]
            p = nxt[p]
            i += 1

        return total // n2