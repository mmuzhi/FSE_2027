from collections import Counter

class Solution:
    def minSteps(self, s: str, t: str) -> int:
        cnt1 = Counter(s)
        cnt2 = Counter(t)
        diff = cnt2 - cnt1  # characters in t that need to be changed
        return sum(diff.values())