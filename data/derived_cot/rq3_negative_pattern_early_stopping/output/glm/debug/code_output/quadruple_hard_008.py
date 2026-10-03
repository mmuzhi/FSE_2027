class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        from collections import defaultdict
        
        if not set(s2).issubset(set(s1)): 
            return 0
            
        s1 = ''.join(char for char in s1 if char in set(s2))
        
        rec, track = [0], defaultdict(int) 
        ct = start = 0
        
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
                
            if start not in track: 
                track[start] = len(rec) - 1
            else: 
                break
        
        cycleStartIdx = track[start]
        cycleStartVal = rec[cycleStartIdx]
        cycle1 = rec[-1] - cycleStartVal
        cycle2 = len(rec) - 1 - cycleStartIdx
        rest = n1 - cycleStartVal
        
        rem = cycleStartVal + rest % cycle1
        
        ptr2 = cycleStartIdx
        while ptr2 < len(rec) and rec[ptr2] <= rem: 
            ptr2 += 1
            
        return (cycle2 * (rest // cycle1) + ptr2 - 1) // n2