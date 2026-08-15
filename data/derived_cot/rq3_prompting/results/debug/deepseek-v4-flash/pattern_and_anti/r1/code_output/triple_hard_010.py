class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0:
            return 0
        if not set(s2).issubset(set(s1)):
            return 0

        m = len(s2)
        if m == 0:
            return 0

        nxt = []
        for i in range(m):
            j = i
            cnt = 0
            for ch in s1:
                if ch == s2[j]:
                    j += 1
                    if j == m:
                        cnt += 1
                        j = 0
            nxt.append((j, cnt))

        idx = 0
        total = 0
        seen = {0: (0, 0)}
        counts = [0]

        for k in range(1, n1 + 1):
            idx, add = nxt[idx]
            total += add

            if idx in seen:
                start, start_total = seen[idx]
                cycle_len = k - start
                cycle_total = total - start_total
                remaining = n1 - start
                cycles = remaining // cycle_len
                rem = remaining % cycle_len
                total = counts[start + rem] + cycles * cycle_total
                return total // n2

            seen[idx] = (k, total)
            counts.append(total)

        return total // n2