from collections import defaultdict

class Solution:
    def getMaxRepetitions(self, s1: str, n1: int, s2: str, n2: int) -> int:
        if not set(s2).issubset(set(s1)):
            return 0
        
        len1, len2 = len(s1), len(s2)
        count1 = 0          # number of full s1 repetitions consumed
        count2 = 0          # number of full s2 repetitions completed
        i = 0               # current index in s1
        record = {}         # i -> (count1, count2) after a complete s2 repetition
        
        while count1 < n1:
            for ch in s2:
                pos = s1.find(ch, i)
                if pos == -1:
                    count1 += 1
                    if count1 >= n1:
                        return count2 // n2
                    i = 0
                    pos = s1.find(ch)
                    if pos == -1:   # should not happen because of subset check
                        return 0
                i = pos + 1
                if i == len1:
                    i = 0
                    count1 += 1
            count2 += 1
            
            if i in record:
                prev_count1, prev_count2 = record[i]
                cycle_s1 = count1 - prev_count1
                cycle_s2 = count2 - prev_count2
                if cycle_s1 == 0:
                    continue
                remaining_s1 = n1 - prev_count1
                cycles = remaining_s1 // cycle_s1
                count1 += cycles * cycle_s1
                count2 += cycles * cycle_s2
                break
            else:
                record[i] = (count1, count2)
        
        while count1 < n1:
            for ch in s2:
                pos = s1.find(ch, i)
                if pos == -1:
                    count1 += 1
                    if count1 >= n1:
                        return count2 // n2
                    i = 0
                    pos = s1.find(ch)
                    if pos == -1:
                        return 0
                i = pos + 1
                if i == len1:
                    i = 0
                    count1 += 1
            count2 += 1
        
        return count2 // n2