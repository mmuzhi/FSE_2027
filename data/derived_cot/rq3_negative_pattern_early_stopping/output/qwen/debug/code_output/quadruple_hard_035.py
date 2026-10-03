from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        s1 = ''.join(char for char in s1 if char in set(s2))
        
        if not s1:
            return 0
        
        rec = [0]
        track = {}
        ptr1 = 0
        ptr2 = 0
        ct = 0
        
        while True:
            for char in s2:
                pos = s1.find(char, ptr1)
                if pos == -1:
                    ct += 1
                    pos = s1.find(char)
                ptr1 = pos + 1
            rec.append(ct + 1)
            
            if rec[-1] > n1 * len(s1):
                return (len(rec) - 2) // n2
            
            if ptr1 not in track:
                track[ptr1] = len(rec) - 1
            else:
                break
        
        cycle_start = rec[track[ptr1]]
        cycle_length = ct + 1 - cycle_start
        cycle_count = len(rec) - 1 - track[ptr1]
        
        remaining = n1 * len(s1) - cycle_start
        remainder = cycle_start + (remaining // cycle_length) * cycle_length
        
        while rec[ptr2] <= remainder:
            ptr2 += 1
        
        return (cycle_count * (remaining // cycle_length) + ptr2 - 1) // n2