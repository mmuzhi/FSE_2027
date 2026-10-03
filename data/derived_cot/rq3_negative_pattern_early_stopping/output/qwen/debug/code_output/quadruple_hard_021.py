from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        s1 = ''.join(char for char in s1 if char in set(s2))
        
        rec = [0]
        track = defaultdict(int)
        ct = start = ptr1 = ptr2 = 0
        
        while True:
            found = False
            for char in s2:
                ptr = s1.find(char, start)
                if ptr == -1:
                    ct += 1
                    ptr = s1.find(char)
                    if ptr == -1:
                        break
                start = ptr + 1
                found = True
            if not found:
                break
            rec.append(ct + 1)
            if rec[-1] >= n1:
                return (len(rec) - 1) // n2
            if start == 0:
                break
            if start not in track:
                track[start] = len(rec) - 1
            else:
                cycle_start = track[start]
                cycle_length = len(rec) - cycle_start
                total_rec = rec[-1]
                full_cycles = (n1 - cycle_start) // cycle_length
                total_rec += full_cycles * cycle_length
                return (total_rec) // n2
        
        return 0