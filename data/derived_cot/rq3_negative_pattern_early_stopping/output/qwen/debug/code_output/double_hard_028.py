class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not s2:
            return 0
        
        s1_filtered = ''.join(filter(lambda c: c in set(s2), s1))
        if not s1_filtered:
            return 0
        
        rec = [0]
        track = {}
        start = 0
        ct = 0
        
        while True:
            found = True
            for char in s2:
                while True:
                    pos = s1_filtered.find(char, start)
                    if pos != -1:
                        start = pos + 1
                        break
                    else:
                        ct += 1
                        if ct >= n1:
                            return (len(rec) - 2) // n2
                        start = 0
                        pos = s1_filtered.find(char)
                        if pos == -1:
                            return 0
                        start = pos + 1
            rec.append(ct + 1)
            if ct >= n1:
                return (len(rec) - 2) // n2
            
            if start in track:
                cycle_start_index = track[start]
                cycle_s2 = len(rec) - cycle_start_index - 1
                cycle_copy = ct - rec[cycle_start_index]
                remaining = n1 - rec[cycle_start_index]
                full_cycles = remaining // cycle_copy
                remainder = remaining % cycle_copy
                
                total_s2 = rec[cycle_start_index] + full_cycles * cycle_s2
                temp = rec[cycle_start_index]
                temp_start = start
                temp_ct = rec[cycle_start_index]
                for _ in range(remainder):
                    for char in s2:
                        while True:
                            pos = s1_filtered.find(char, temp_start)
                            if pos != -1:
                                temp_start = pos + 1
                                break
                            else:
                                temp_ct += 1
                                if temp_ct >= n1:
                                    break
                                temp_start = 0
                                pos = s1_filtered.find(char)
                                if pos == -1:
                                    break
                                temp_start = pos + 1
                    if temp_start > 0:
                        total_s2 += 1
                return total_s2 // n2
            else:
                track[start] = len(rec) - 1