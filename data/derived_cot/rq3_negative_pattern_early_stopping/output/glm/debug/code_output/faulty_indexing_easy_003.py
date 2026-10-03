import collections
import math
from typing import List

class Solution:
    def hasGroupsSizeX(self, deck: List[int]) -> bool:
        count = collections.Counter(deck)
        val = count.values()
        m = math.gcd(*val)
        if m >= 2:
            return True 
        else:
            return False