class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        idx = 0
        cnt = 0
        seen = {0: (0, 0)}
        m = len(s2)

        for i in range(1, n1 + 1):
            for ch in s1:
                if ch == s2[idx]:
                    idx += 1
                    if idx == m:
                        cnt += 1
                        idx = 0

            if idx in seen:
                start, start_cnt = seen[idx]
                cycle_len = i - start
                cycle_cnt = cnt - start_cnt

                total_cnt = start_cnt + ((n1 - start) // cycle_len) * cycle_cnt

                for _ in range((n1 - start) % cycle_len):
                    for ch in s1:
                        if ch == s2[idx]:
                            idx += 1
                            if idx == m:
                                total_cnt += 1
                                idx = 0

                return total_cnt // n2

            seen[idx] = (i, cnt)

        return cnt // n2