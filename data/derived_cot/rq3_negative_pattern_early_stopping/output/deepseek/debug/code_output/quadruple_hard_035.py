from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        rec, track = [0], defaultdict(int) 
        ct = start = 0

        if not set(s2).issubset(set(s1)):
            return 0

        s1 = ''.join(char for char in s1 if char in set(s2))
        
        while True:
            for char in s2:
                ptr = s1.find(char, start)
                if ptr == -1:
                    ct += 1
                    ptr = s1.find(char)
                start = ptr + 1
            rec.append(ct + 1)

            if rec[-1] > n1:
                return (len(rec) - 2) // n2

            if ptr not in track:
                track[ptr] = len(rec) - 1
            else:
                break
        
        cycle_start_index = track[ptr]
        cycle_start_s1 = rec[cycle_start_index]
        cycle_s1 = ct + 1 - cycle_start_s1
        cycle_s2 = len(rec) - 1 - cycle_start_index
        
        rest = n1 - cycle_start_s1
        full_cycles = rest // cycle_s1
        rem_s1 = rest - full_cycles * cycle_s1
        
        extra_s2 = 0
        for i in range(cycle_start_index, len(rec)):
            used_s1 = rec[i] - cycle_start_s1
            if used_s1 <= rem_s1:
                extra_s2 = i - cycle_start_index
            else:
                break
        
        total_s2 = cycle_start_index + full_cycles * cycle_s2 + extra_s2
        return total_s2 // n2