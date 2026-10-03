from collections import Counter
from typing import List

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        d = Counter(arr)
        l = list(d.values())
        return len(l) == len(set(l))