class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        allowed = set(s2)
        if not allowed.issubset(s1):
            return 0

        s1 = ''.join(c for c in s1 if c in allowed)

        cnt = 0
        idx = 0
        seen = {0: (0, 0)}
        k = 0

        while k < n1:
            for ch in s1:
                if ch == s2[idx]:
                    idx += 1
                    if idx == len(s2):
                        cnt += 1
                        idx = 0
            k += 1

            if idx in seen:
                prev_k, prev_cnt = seen[idx]
                cycle_len = k - prev_k
                cycle_cnt = cnt - prev_cnt

                remaining = n1 - k
                cnt += (remaining // cycle_len) * cycle_cnt

                for _ in range(remaining % cycle_len):
                    for ch in s1:
                        if ch == s2[idx]:
                            idx += 1
                            if idx == len(s2):
                                cnt += 1
                                idx = 0
                break

            seen[idx] = (k, cnt)

        return cnt // n2