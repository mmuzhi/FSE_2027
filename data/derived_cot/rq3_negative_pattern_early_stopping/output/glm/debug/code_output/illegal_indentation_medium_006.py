import operator
from functools import reduce
from collections import Counter
from typing import List

class Solution:
    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        w2 = reduce(operator.or_, map(Counter, words2), Counter())
        return [w1 for w1 in words1 if Counter(w1) >= w2]