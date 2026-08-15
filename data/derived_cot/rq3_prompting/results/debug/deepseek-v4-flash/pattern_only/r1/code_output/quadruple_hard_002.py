class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        m = len(s2)
        cnt = [0] * m
        nxt = [0] * m

        for i in range(m):
            j = i
            c = 0
            for ch in s1:
                if ch == s2[j]:
                    j += 1
                    if j == m:
                        c += 1
                        j = 0
            cnt[i] = c
            nxt[i] = j

        total = 0
        pos = 0
        copies = 0
        seen = {}

        while copies < n1:
            if pos in seen:
                prev_copies, prev_total = seen[pos]
                cycle_len = copies - prev_copies
                cycle_total = total - prev_total
                cycles = (n1 - copies) // cycle_len

                total += cycles * cycle_total
                copies += cycles * cycle_len

                if copies == n1:
                    break

                while copies < n1:
                    total += cnt[pos]
                    pos = nxt[pos]
                    copies += 1
                break

            seen[pos] = (copies, total)
            total += cnt[pos]
            pos = nxt[pos]
            copies += 1

        return total // n2