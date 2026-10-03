from collections import Counter
from typing import List

class Solution:
    def uniqueOccurrences(self, arr: List[int]) -> bool:
        d = Counter(arr)
        l = d.values()
        if len(l) == len(set(l)):
            return True
        else:
            return False