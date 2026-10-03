from collections import Counter
class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        d = Counter(arr)
        v = list(d.values())
        return len(v) == len(set(v))