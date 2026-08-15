class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        allowed = set(s2)
        if not allowed.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in allowed)

        repeat_count = [0]
        seen = {0: 0}
        j = 0
        count = 0

        for k in range(1, n1 + 1):
            for ch in s1:
                if ch == s2[j]:
                    j += 1
                    if j == len(s2):
                        j = 0
                        count += 1

            repeat_count.append(count)

            if j in seen:
                start = seen[j]
                cycle_len = k - start
                cycle_count = count - repeat_count[start]
                remaining = n1 - start

                total = repeat_count[start] + cycle_count * (remaining // cycle_len)
                total += repeat_count[start + remaining % cycle_len] - repeat_count[start]

                return total // n2

            seen[j] = k

        return repeat_count[n1] // n2