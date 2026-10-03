from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(c for c in s1 if c in set(s2))
        len_s1 = len(s1)

        pointer = 0
        consumed_s1 = 0  # number of full s1 strings consumed

        rec = [0]
        track = defaultdict(int)  # maps pointer (position in s1) to index in rec

        while True:
            for c in s2:
                pos = s1.find(c, pointer)
                if pos == -1:
                    consumed_s1 += 1
                    pos = s1.find(c)
                    if pos == -1:
                        return 0
                pointer = pos + 1

            rec.append(consumed_s1 + 1)  # +1 because we count the s1 we are currently using?

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            if pointer not in track:
                track[pointer] = len(rec) - 1
            else:
                cycle_start_index = track[pointer]
                s1_before_cycle = rec[cycle_start_index]
                s1_in_cycle = consumed_s1 + 1 - s1_before_cycle
                s2_in_cycle = len(rec) - 1 - cycle_start_index

                remaining_s1 = n1 - s1_before_cycle

                full_cycles = remaining_s1 // s1_in_cycle
                s2_from_cycles = full_cycles * s2_in_cycle

                rest_s1 = remaining_s1 % s1_in_cycle

                extra_s2 = 0
                i = cycle_start_index + 1
                while i < len(rec) and rec[i] - s1_before_cycle <= rest_s1:
                    extra_s2 += 1
                    i += 1

                total_s2_matched = cycle_start_index + s2_from_cycles + extra_s2
                return total_s2_matched // n2

        return 0