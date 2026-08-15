class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        m = len(s2)
        next_idx = [0] * m
        count = [0] * m

        for start in range(m):
            idx = start
            c = 0
            for ch in s1:
                if ch == s2[idx]:
                    idx += 1
                    if idx == m:
                        c += 1
                        idx = 0
            count[start] = c
            next_idx[start] = idx

        total = 0
        idx = 0
        seen = {0: (0, 0)}

        for i in range(1, n1 + 1):
            total += count[idx]
            idx = next_idx[idx]

            if idx in seen:
                prev_i, prev_total = seen[idx]
                cycle_len = i - prev_i
                cycle_count = total - prev_total

                remaining = n1 - i
                total += (remaining // cycle_len) * cycle_count

                extra = remaining % cycle_len
                for _ in range(extra):
                    total += count[idx]
                    idx = next_idx[idx]

                return total // n2

            seen[idx] = (i, total)

        return total // n2