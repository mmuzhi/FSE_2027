class Solution:
    def partitionLabels(self, s: str) -> List[int]:
        last_occurrence = {}
        for i in range(len(s)-1, -1, -1):
            if s[i] not in last_occurrence:
                last_occurrence[s[i]] = i
        
        i = 0
        start = 0
        max_last = 0
        ans = []
        while i < len(s):
            max_last = max(max_last, last_occurrence[s[i]])
            if i == max_last:
                ans.append(i - start + 1)
                start = i + 1
            i += 1
        
        return ans