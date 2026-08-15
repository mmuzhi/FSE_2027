class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        s2_set = set(s2)
        if not s2_set.issubset(s1):
            return 0

        s1 = ''.join(ch for ch in s1 if ch in s2_set)

        rec = [0]
        track = {}
        blocks = 0
        pos = 0
        matched = 0

        while True:
            for ch in s2:
                idx = s1.find(ch, pos)
                if idx == -1:
                    blocks += 1
                    idx = s1.find(ch)
                pos = idx + 1

            matched += 1
            rec.append(blocks + 1)

            if rec[-1] > n1:
                return (matched - 1) // n2

            if pos in track:
                start = track[pos]
                pre_blocks = rec[start]
                cycle_blocks = rec[matched] - pre_blocks
                cycle_copies = matched - start

                remaining = n1 - pre_blocks
                full_cycles = remaining // cycle_blocks
                extra_blocks = remaining % cycle_blocks

                r = 0
                while r < cycle_copies and rec[start + r] - pre_blocks <= extra_blocks:
                    r += 1
                r -= 1

                total = start + full_cycles * cycle_copies + r
                return total // n2

            track[pos] = matched