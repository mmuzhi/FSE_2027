from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        s1 = ''.join(c for c in s1 if c in set(s2))
        
        ptr = 0               # current index in s1 (0-based)
        cnt_s1 = 0            # total number of s1 strings used so far
        cnt_s2 = 0            # total number of s2 strings fully matched
        
        track = {}            # ptr -> (cnt_s1, cnt_s2) at start of matching an s2
        rec = [0]             # rec[i] = cnt_s1 after i s2 matches (rec[0] = 0)
        
        while True:
            for ch in s2:
                pos = s1.find(ch, ptr)
                if pos == -1:
                    cnt_s1 += 1
                    pos = s1.find(ch)
                    if pos == -1:
                        return 0
                ptr = pos + 1
                if ptr == len(s1):
                    ptr = 0
                    cnt_s1 += 1
            
            cnt_s2 += 1
            rec.append(cnt_s1)
            
            if ptr in track:                # cycle found
                prev_cnt_s1, prev_cnt_s2 = track[ptr]
                cycle_s1 = cnt_s1 - prev_cnt_s1
                cycle_s2 = cnt_s2 - prev_cnt_s2
                before_cycle_s1 = prev_cnt_s1
                before_cycle_s2 = prev_cnt_s2
                
                if cnt_s1 >= n1:
                    total_s2 = 0
                    for i, v in enumerate(rec):
                        if v <= n1:
                            total_s2 = i
                        else:
                            break
                    return total_s2 // n2
                
                remain_s1 = n1 - before_cycle_s1
                full_cycles = remain_s1 // cycle_s1
                remainder_s1 = remain_s1 % cycle_s1
                
                target_s1 = before_cycle_s1 + remainder_s1
                s2_in_rem = 0
                for i, v in enumerate(rec):
                    if v <= target_s1:
                        s2_in_rem = i
                    else:
                        break
                total_s2 = before_cycle_s2 + full_cycles * cycle_s2 + (s2_in_rem - before_cycle_s2)
                return total_s2 // n2
            else:
                track[ptr] = (cnt_s1, cnt_s2)
            
            if cnt_s1 >= n1:
                total_s2 = 0
                for i, v in enumerate(rec):
                    if v <= n1:
                        total_s2 = i
                    else:
                        break
                return total_s2 // n2