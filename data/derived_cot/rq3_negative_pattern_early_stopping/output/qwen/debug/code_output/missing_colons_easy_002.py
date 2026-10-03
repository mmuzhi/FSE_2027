from collections import Counter

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        d = Counter(arr)
        l = list(d.values())
        return len(l) == len(set(l))