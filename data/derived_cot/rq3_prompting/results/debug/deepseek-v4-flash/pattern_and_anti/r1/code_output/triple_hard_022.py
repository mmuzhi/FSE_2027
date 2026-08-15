class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        allowed = set(s2)
        if not allowed.issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in allowed)
        L = len(s1)
        limit = n1 * L

        pos = 0
        positions = [0]
        seen = {}
        matched = 0

        while True:
            for ch in s2:
                block = pos // L
                idx = s1.find(ch, pos % L)
                if idx == -1:
                    block += 1
                    idx = s1.find(ch, 0)
                pos = block * L + idx + 1

            matched += 1
            positions.append(pos)

            if pos > limit:
                return (matched - 1) // n2
            if pos == limit:
                return matched // n2

            offset = pos % L
            if offset in seen:
                start = seen[offset]
                cycle_copies = matched - start
                cycle_len = positions[matched] - positions[start]

                rest = limit - positions[start]
                full = rest // cycle_len
                rem = rest % cycle_len

                extra = 0
                for r in range(1, cycle_copies + 1):
                    if positions[start + r] - positions[start] <= rem:
                        extra = r
                    else:
                        break

                return (start + full * cycle_copies + extra) // n2
            else:
                seen[offset] = matched