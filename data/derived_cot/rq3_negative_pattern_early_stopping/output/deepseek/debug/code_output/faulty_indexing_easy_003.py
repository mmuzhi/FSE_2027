from typing import List
import collections
import math

class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        count = collections.Counter(deck)
        m = math.gcd(*count.values())
        return m >= 2