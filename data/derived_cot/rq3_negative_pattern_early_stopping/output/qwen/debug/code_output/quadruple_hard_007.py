class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        rec = [0]
        track = {}
        ct = 0
        start = 0
        
        while True:
            for char in s2:
                pos = s1.find(char, start)
                if pos == -1:
                    pos = s1.find(char)
                    if pos == -1:
                        ct += 1
                        break
                    start = pos + 1
                else:
                    start = pos + 1
            else:
                # This else corresponds to the for loop finishing without break
                rec.append(ct + 1)
                if rec[-1] > n1:
                    return (len(rec)-2) // n2
                if start not in track:
                    track[start] = len(rec)-1
                else:
                    break
            break
        
        # Cycle detection part
        cycle_start = rec[track[start]]
        cycle_length = len(rec) - track[start]
        cycle_count = (n1 * len(s1) - cycle_start) // (len(s1) * cycle_length) + 1
        total = cycle_count * cycle_length + (len(rec) - track[start] - 1)
        return total // n2