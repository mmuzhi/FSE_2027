import operator
from collections import Counter
from functools import reduce
from typing import List

class Solution:
    def wordSubsets(self, words1: List[str], words2: List[str]) -> List[str]:
        w2 = reduce(operator.or_, map(Counter, words2), Counter())
        return [w1 for w1 in words1 if not (w2 - Counter(w1))]