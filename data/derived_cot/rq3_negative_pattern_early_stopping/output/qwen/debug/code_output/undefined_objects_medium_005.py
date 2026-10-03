from collections import Counter

class Solution:
    def minSteps(self, s: str, t: str) -> int:
        cnt1 = Counter(s)
        cnt2 = Counter(t)
        sm = 0
        for char in cnt2:
            if cnt1[char] < cnt2[char]:
                sm += (cnt2[char] - cnt1[char])
        return sm