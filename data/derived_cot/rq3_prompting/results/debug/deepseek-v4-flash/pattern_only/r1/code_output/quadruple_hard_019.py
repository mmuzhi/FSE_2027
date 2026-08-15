class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if n1 == 0:
            return 0

        s2_set = set(s2)
        if not s2_set.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in s2_set)

        idx = 0
        s1_count = 0
        s2_count = 0
        seen = {}

        while s1_count < n1:
            s1_count += 1
            for ch in s1:
                if ch == s2[idx]:
                    idx += 1
                    if idx == len(s2):
                        s2_count += 1
                        idx = 0

            if s1_count == n1:
                return s2_count // n2

            if idx in seen:
                prev_s1, prev_s2 = seen[idx]
                cycle_s1 = s1_count - prev_s1
                cycle_s2 = s2_count - prev_s2
                k = (n1 - s1_count) // cycle_s1
                s2_count += k * cycle_s2
                s1_count += k * cycle_s1
                break

            seen[idx] = (s1_count, s2_count)

        while s1_count < n1:
            s1_count += 1
            for ch in s1:
                if ch == s2[idx]:
                    idx += 1
                    if idx == len(s2):
                        s2_count += 1
                        idx = 0

        return s2_count // n2