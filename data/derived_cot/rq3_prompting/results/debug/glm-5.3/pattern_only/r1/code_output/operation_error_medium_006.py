from collections import Counter
from functools import reduce
from typing import List


class Solution:
    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        w2 = reduce(lambda a, b: a | b, map(Counter, words2))
        return [w1 for w1 in words1 if Counter(w1) >= w2]