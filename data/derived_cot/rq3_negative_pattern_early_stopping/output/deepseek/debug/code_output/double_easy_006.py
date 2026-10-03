from collections import Counter
from typing import List

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        freq = Counter(arr)
        occurrences = list(freq.values())
        return len(occurrences) == len(set(occurrences))