from collections import Counter

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        d = Counter(arr)
        counts = list(d.values())
        return len(counts) == len(set(counts))